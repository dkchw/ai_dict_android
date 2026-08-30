import zipfile
import io
import os
import shutil
from fastapi import UploadFile, File
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List, Optional

from .db import init_db, get_session, Word, ChatMessage, AppSetting, ExternalLinkTemplate, Comparison, ComparisonChat, Explain, ExplainChat, Translation, TranslationChat, Profile
from .ai import chat_conversation, correct_text, generate_title, explain_word, extract_language_and_lemma, chat_with_word, compare_words, chat_with_comparison, explain_text, chat_with_explain

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# --- Schemas ---
class SearchRequest(BaseModel):
    term: str
    session_id: Optional[str] = None
    profile_id: int = 1
    target_language: Optional[str] = None
    source_language: Optional[str] = None

class ChatRequest(BaseModel):
    word_id: int
    content: str

class ComparisonSearchRequest(BaseModel):
    terms: str
    session_id: Optional[str] = None
    profile_id: int = 1

class ComparisonChatRequest(BaseModel):
    comparison_id: int
    content: str

class ExplainSearchRequest(BaseModel):
    text: str
    session_id: Optional[str] = None
    profile_id: int = 1

class ExplainChatRequest(BaseModel):
    explain_id: int
    content: str

class UpdateColorRequest(BaseModel):
    color: str | None

class AppSettingItem(BaseModel):
    key: str
    value: str

class LinkTemplateModel(BaseModel):
    name: str = "Dict"
    language: str
    url_template: str
    icon_url: str

class RegenerateRequest(BaseModel):
    model: str

# --- API Endpoints ---

@app.post("/api/words/{word_id}/regenerate")
async def regenerate_word(word_id: int, req: RegenerateRequest, session: Session = Depends(get_session)):
    word = session.get(Word, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
        
    try:
        explanation = await explain_word(word.term, session, explicit_model=req.model)
        language, lemma = extract_language_and_lemma(explanation)
        
        word.language = language
        word.lemma = lemma
        session.add(word)
        
        # Replace the first assistant chat (which is the explanation)
        first_chat = session.exec(select(ChatMessage).where(ChatMessage.word_id == word.id).order_by(ChatMessage.created_at)).first()
        if first_chat:
            first_chat.content = explanation
            session.add(first_chat)
        else:
            first_chat = ChatMessage(word_id=word.id, role="assistant", content=explanation)
            session.add(first_chat)
            
        session.commit()
        session.refresh(word)
        session.refresh(first_chat)
        
        chats = session.exec(select(ChatMessage).where(ChatMessage.word_id == word.id).order_by(ChatMessage.created_at)).all()
        return {"word": word.model_dump(), "chats": [c.model_dump() for c in chats]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/search")
async def search(req: SearchRequest, session: Session = Depends(get_session)):
    # Check if word already exists
    existing = session.exec(select(Word).where(Word.term == req.term)).first()
    if existing:
        existing.search_count += 1
        if req.session_id:
            existing.session_id = req.session_id
        session.add(existing)
        session.commit()
        session.refresh(existing)
        chats = session.exec(select(ChatMessage).where(ChatMessage.word_id == existing.id).order_by(ChatMessage.created_at)).all()
        return {"word": existing.model_dump(), "chats": [c.model_dump() for c in chats]}

    # Fetch from OpenRouter
    try:
        explanation = await explain_word(req.term, session, target_language=req.target_language, source_language=req.source_language)
        language, lemma = extract_language_and_lemma(explanation)
        
        new_word = Word(term=req.term, language=language, lemma=lemma, search_count=1, session_id=req.session_id, profile_id=req.profile_id)
        session.add(new_word)
        session.commit()
        session.refresh(new_word)
        
        system_msg = ChatMessage(word_id=new_word.id, role="assistant", content=explanation)
        session.add(system_msg)
        session.commit()
        session.refresh(system_msg)
        session.refresh(new_word)
        return {"word": new_word.model_dump(), "chats": [system_msg.model_dump()]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/chat")
async def follow_up_chat(req: ChatRequest, session: Session = Depends(get_session)):
    word = session.get(Word, req.word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
        
    user_msg = ChatMessage(word_id=word.id, role="user", content=req.content)
    session.add(user_msg)
    session.commit()
    
    # Load past chats
    chats = session.exec(select(ChatMessage).where(ChatMessage.word_id == word.id).order_by(ChatMessage.created_at)).all()
    messages = [{"role": "system", "content": "You are a helpful language assistant. Continue the conversation."}]
    for c in chats:
        messages.append({"role": c.role, "content": c.content})
        
    try:
        response_content = await chat_with_word(messages, session)
        reply_msg = ChatMessage(word_id=word.id, role="assistant", content=response_content)
        session.add(reply_msg)
        session.commit()
        session.refresh(reply_msg)
        return reply_msg.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class ChatUpdateRequest(BaseModel):
    content: str

@app.patch("/api/chats/{chat_id}")
def update_chat(chat_id: int, req: ChatUpdateRequest, session: Session = Depends(get_session)):
    chat = session.get(ChatMessage, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat.content = req.content
    session.add(chat)
    session.commit()
    return chat.model_dump()

@app.patch("/api/comparisons/chats/{chat_id}")
def update_comparison_chat(chat_id: int, req: ChatUpdateRequest, session: Session = Depends(get_session)):
    chat = session.get(ComparisonChat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat.content = req.content
    session.add(chat)
    session.commit()
    return chat.model_dump()

@app.post("/api/comparisons/search")
async def search_comparison(req: ComparisonSearchRequest, session: Session = Depends(get_session)):
    # Check if existing
    terms_list = [t.strip().lower() for t in req.terms.replace(';', ',').split(',') if t.strip()]
    terms_list.sort()
    normalized_terms = ", ".join(terms_list)
    
    existing = session.exec(select(Comparison).where(Comparison.terms == normalized_terms)).first()
    if existing:
        existing.search_count += 1
        if req.session_id:
            existing.session_id = req.session_id
        session.add(existing)
        session.commit()
        session.refresh(existing)
        chats = session.exec(select(ComparisonChat).where(ComparisonChat.comparison_id == existing.id).order_by(ComparisonChat.created_at)).all()
        return {"comparison": existing.model_dump(), "chats": [c.model_dump() for c in chats]}

    try:
        explanation = await compare_words(normalized_terms, session)
        
        new_comp = Comparison(terms=normalized_terms, search_count=1, session_id=req.session_id, profile_id=req.profile_id)
        session.add(new_comp)
        session.commit()
        session.refresh(new_comp)
        
        system_msg = ComparisonChat(comparison_id=new_comp.id, role="assistant", content=explanation)
        session.add(system_msg)
        session.commit()
        session.refresh(system_msg)
        session.refresh(new_comp)
        return {"comparison": new_comp.model_dump(), "chats": [system_msg.model_dump()]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/comparisons/{comparison_id}/regenerate")
async def regenerate_comparison(comparison_id: int, req: RegenerateRequest, session: Session = Depends(get_session)):
    comp = session.get(Comparison, comparison_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Comparison not found")
        
    try:
        explanation = await compare_words(comp.terms, session, explicit_model=req.model)
        
        first_chat = session.exec(select(ComparisonChat).where(ComparisonChat.comparison_id == comp.id).order_by(ComparisonChat.created_at)).first()
        if first_chat:
            first_chat.content = explanation
            session.add(first_chat)
        else:
            first_chat = ComparisonChat(comparison_id=comp.id, role="assistant", content=explanation)
            session.add(first_chat)
            
        session.commit()
        session.refresh(comp)
        session.refresh(first_chat)
        
        chats = session.exec(select(ComparisonChat).where(ComparisonChat.comparison_id == comp.id).order_by(ComparisonChat.created_at)).all()
        return {"comparison": comp.model_dump(), "chats": [c.model_dump() for c in chats]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/comparisons/chat")
async def follow_up_comparison_chat(req: ComparisonChatRequest, session: Session = Depends(get_session)):
    comp = session.get(Comparison, req.comparison_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Comparison not found")
        
    user_msg = ComparisonChat(comparison_id=comp.id, role="user", content=req.content)
    session.add(user_msg)
    session.commit()
    chats = session.exec(select(ComparisonChat).where(ComparisonChat.comparison_id == comp.id).order_by(ComparisonChat.created_at)).all()
    messages = [{"role": "system", "content": "You are a helpful language assistant. Continue the conversation regarding the word comparison."}]
    for c in chats:
        messages.append({"role": c.role, "content": c.content})
        
    try:
        response_content = await chat_with_comparison(messages, session)
        reply_msg = ComparisonChat(comparison_id=comp.id, role="assistant", content=response_content)
        session.add(reply_msg)
        session.commit()
        session.refresh(reply_msg)
        return reply_msg.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/comparisons")
def get_comparisons(profile_id: int = 1, session: Session = Depends(get_session)):
    comps = session.exec(select(Comparison).order_by(Comparison.updated_at.desc())).all()
    return comps

@app.delete("/api/comparisons/{comparison_id}")
def delete_comparison(comparison_id: int, session: Session = Depends(get_session)):
    comp = session.get(Comparison, comparison_id)
    if comp:
        chats = session.exec(select(ComparisonChat).where(ComparisonChat.comparison_id == comp.id)).all()
        for chat in chats:
            session.delete(chat)
        session.delete(comp)
        session.commit()
    return {"status": "ok"}

@app.patch("/api/explains/chats/{chat_id}")
def update_explain_chat(chat_id: int, req: ChatUpdateRequest, session: Session = Depends(get_session)):
    chat = session.get(ExplainChat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat.content = req.content
    session.add(chat)
    session.commit()
    return chat.model_dump()

@app.post("/api/explains/search")
async def search_explain(req: ExplainSearchRequest, session: Session = Depends(get_session)):
    normalized_text = req.text.strip()
    
    existing = session.exec(select(Explain).where(Explain.text == normalized_text)).first()
    if existing:
        existing.search_count += 1
        if req.session_id:
            existing.session_id = req.session_id
        session.add(existing)
        session.commit()
        session.refresh(existing)
        chats = session.exec(select(ExplainChat).where(ExplainChat.explain_id == existing.id).order_by(ExplainChat.created_at)).all()
        return {"explain": existing.model_dump(), "chats": [c.model_dump() for c in chats]}

    try:
        explanation = await explain_text(normalized_text, session)
        
        new_exp = Explain(text=normalized_text, search_count=1, session_id=req.session_id, profile_id=req.profile_id)
        session.add(new_exp)
        session.commit()
        session.refresh(new_exp)
        
        system_msg = ExplainChat(explain_id=new_exp.id, role="assistant", content=explanation)
        session.add(system_msg)
        session.commit()
        session.refresh(system_msg)
        session.refresh(new_exp)
        return {"explain": new_exp.model_dump(), "chats": [system_msg.model_dump()]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/explains/{explain_id}/regenerate")
async def regenerate_explain(explain_id: int, req: RegenerateRequest, session: Session = Depends(get_session)):
    exp = session.get(Explain, explain_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Explain not found")
        
    try:
        explanation = await explain_text(exp.text, session, explicit_model=req.model)
        
        first_chat = session.exec(select(ExplainChat).where(ExplainChat.explain_id == exp.id).order_by(ExplainChat.created_at)).first()
        if first_chat:
            first_chat.content = explanation
            session.add(first_chat)
        else:
            first_chat = ExplainChat(explain_id=exp.id, role="assistant", content=explanation)
            session.add(first_chat)
            
        session.commit()
        session.refresh(exp)
        session.refresh(first_chat)
        
        chats = session.exec(select(ExplainChat).where(ExplainChat.explain_id == exp.id).order_by(ExplainChat.created_at)).all()
        return {"explain": exp.model_dump(), "chats": [c.model_dump() for c in chats]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/explains/chat")
async def follow_up_explain_chat(req: ExplainChatRequest, session: Session = Depends(get_session)):
    exp = session.get(Explain, req.explain_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Explain not found")
        
    user_msg = ExplainChat(explain_id=exp.id, role="user", content=req.content)
    session.add(user_msg)
    session.commit()
    chats = session.exec(select(ExplainChat).where(ExplainChat.explain_id == exp.id).order_by(ExplainChat.created_at)).all()
    messages = [{"role": "system", "content": "You are a helpful language assistant. Continue the conversation regarding the explanation."}]
    for c in chats:
        messages.append({"role": c.role, "content": c.content})
        
    try:
        response_content = await chat_with_explain(messages, session)
        reply_msg = ExplainChat(explain_id=exp.id, role="assistant", content=response_content)
        session.add(reply_msg)
        session.commit()
        session.refresh(reply_msg)
        return reply_msg.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/explains")
def get_explains(profile_id: int = 1, session: Session = Depends(get_session)):
    exps = session.exec(select(Explain).order_by(Explain.updated_at.desc())).all()
    return exps

@app.delete("/api/explains/{explain_id}")
def delete_explain(explain_id: int, session: Session = Depends(get_session)):
    exp = session.get(Explain, explain_id)
    if exp:
        chats = session.exec(select(ExplainChat).where(ExplainChat.explain_id == exp.id)).all()
        for chat in chats:
            session.delete(chat)
        session.delete(exp)
        session.commit()
    return {"status": "ok"}


@app.get("/api/words")
def get_words(profile_id: int = 1, session: Session = Depends(get_session)):
    words = session.exec(select(Word).where(Word.profile_id == profile_id).order_by(Word.updated_at.desc())).all()
    return words

@app.delete("/api/words/{word_id}")
def delete_word(word_id: int, session: Session = Depends(get_session)):
    word = session.get(Word, word_id)
    if word:
        # Delete related chats
        chats = session.exec(select(ChatMessage).where(ChatMessage.word_id == word.id)).all()
        for chat in chats:
            session.delete(chat)
        session.delete(word)
        session.commit()
    return {"status": "ok"}

@app.get("/api/words/{word_id}/related")
def get_related_words(word_id: int, session: Session = Depends(get_session)):
    word = session.get(Word, word_id)
    if not word:
        return []
    
    if word.language:
        related = session.exec(
            select(Word)
            .where(Word.language == word.language)
            .where(Word.id != word.id)
            .order_by(Word.updated_at.desc())
            .limit(5)
        ).all()
        return [r.model_dump() for r in related]
    else:
        related = session.exec(
            select(Word)
            .where(Word.id != word.id)
            .order_by(Word.updated_at.desc())
            .limit(5)
        ).all()
        return [r.model_dump() for r in related]

@app.patch("/api/words/{word_id}/color")
def update_word_color(word_id: int, req: UpdateColorRequest, session: Session = Depends(get_session)):
    word = session.get(Word, word_id)
    if word:
        word.color = req.color
        session.add(word)
        session.commit()
        session.refresh(word)
        return word.model_dump()
    raise HTTPException(status_code=404)


class UpdateTermRequest(BaseModel):
    term: str

@app.patch("/api/words/{word_id}/rename")
def rename_word(word_id: int, req: UpdateTermRequest, session: Session = Depends(get_session)):
    word = session.get(Word, word_id)
    if word:
        word.term = req.term
        session.add(word)
        session.commit()
        session.refresh(word)
        return word.model_dump()
    raise HTTPException(status_code=404)

class UpdateTagRequest(BaseModel):
    tag: str | None

@app.patch("/api/words/{word_id}/tag")
def update_word_tag(word_id: int, req: UpdateTagRequest, session: Session = Depends(get_session)):
    word = session.get(Word, word_id)
    if word:
        word.tag = req.tag
        session.add(word)
        session.commit()
        session.refresh(word)
        return word.model_dump()
    raise HTTPException(status_code=404)

@app.patch("/api/comparisons/{comparison_id}/rename")
def rename_comparison(comparison_id: int, req: UpdateTermRequest, session: Session = Depends(get_session)):
    comp = session.get(Comparison, comparison_id)
    if comp:
        comp.terms = req.term
        session.add(comp)
        session.commit()
        session.refresh(comp)
        return comp.model_dump()
    raise HTTPException(status_code=404)

@app.patch("/api/comparisons/{comparison_id}/color")
def update_comparison_color(comparison_id: int, req: UpdateColorRequest, session: Session = Depends(get_session)):
    comp = session.get(Comparison, comparison_id)
    if comp:
        comp.color = req.color
        session.add(comp)
        session.commit()
        session.refresh(comp)
        return comp.model_dump()
    raise HTTPException(status_code=404)

@app.patch("/api/comparisons/{comparison_id}/tag")
def update_comparison_tag(comparison_id: int, req: UpdateTagRequest, session: Session = Depends(get_session)):
    comp = session.get(Comparison, comparison_id)
    if comp:
        comp.tag = req.tag
        session.add(comp)
        session.commit()
        session.refresh(comp)
        return comp.model_dump()
    raise HTTPException(status_code=404)

@app.patch("/api/explains/{explain_id}/rename")
def rename_explain(explain_id: int, req: UpdateTermRequest, session: Session = Depends(get_session)):
    exp = session.get(Explain, explain_id)
    if exp:
        exp.text = req.term
        session.add(exp)
        session.commit()
        session.refresh(exp)
        return exp.model_dump()
    raise HTTPException(status_code=404)

@app.patch("/api/explains/{explain_id}/color")
def update_explain_color(explain_id: int, req: UpdateColorRequest, session: Session = Depends(get_session)):
    exp = session.get(Explain, explain_id)
    if exp:
        exp.color = req.color
        session.add(exp)
        session.commit()
        session.refresh(exp)
        return exp.model_dump()
    raise HTTPException(status_code=404)

@app.patch("/api/explains/{explain_id}/tag")
def update_explain_tag(explain_id: int, req: UpdateTagRequest, session: Session = Depends(get_session)):
    exp = session.get(Explain, explain_id)
    if exp:
        exp.tag = req.tag
        session.add(exp)
        session.commit()
        session.refresh(exp)
        return exp.model_dump()
    raise HTTPException(status_code=404)

class UpdateLanguageRequest(BaseModel):
    language: str | None

@app.patch("/api/words/{word_id}/language")
def update_word_language(word_id: int, req: UpdateLanguageRequest, session: Session = Depends(get_session)):
    word = session.get(Word, word_id)
    if word:
        word.language = req.language
        session.add(word)
        session.commit()
        session.refresh(word)
        return word.model_dump()
    raise HTTPException(status_code=404)

# --- Settings & Templates ---


@app.post("/api/translations/search")
async def search_translation(request: Request, session: Session = Depends(get_session)):
    data = await request.json()
    text = data.get("text", "").strip()
    source_lang = data.get("source_lang", "").strip()
    target_lang = data.get("target_lang", "").strip()
    profile_id = int(data.get("profile_id", 1))
    session_id = data.get("session_id", None)
    model = data.get("model", None)
    
    # If it's a history fetch, they might not send source/target
    existing = session.exec(select(Translation).where(Translation.text == text)).first()
    if existing:
        existing.search_count += 1
        if session_id:
            existing.session_id = session_id
        session.add(existing)
        session.commit()
        session.refresh(existing)
        chats = session.exec(select(TranslationChat).where(TranslationChat.translation_id == existing.id).order_by(TranslationChat.created_at)).all()
        return {"translation": existing.model_dump(), "chats": [c.model_dump() for c in chats]}

    if not text or not source_lang or not target_lang:
        raise HTTPException(status_code=400, detail="Text, source, and target language are required")
        
    from .ai import chat_conversation, correct_text, generate_title, translate_concept
    try:
        explanation = await translate_concept(text, source_lang, target_lang, session, explicit_model=model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    translation = Translation(text=text, source_lang=source_lang, target_lang=target_lang, session_id=session_id, profile_id=profile_id)
    session.add(translation)
    session.commit()
    session.refresh(translation)
    
    chat = TranslationChat(translation_id=translation.id, role="assistant", content=explanation, session_id=session_id)
    session.add(chat)
    session.commit()
    session.refresh(chat)
    
    return {"translation": translation.model_dump(), "chats": [chat.model_dump()]}

@app.post("/api/translations/{translation_id}/regenerate")
async def regenerate_translation(translation_id: int, request: Request, session: Session = Depends(get_session)):
    translation = session.get(Translation, translation_id)
    if not translation:
        raise HTTPException(status_code=404)
        
    data = await request.json()
    model = data.get("model", None)
    
    from .ai import chat_conversation, correct_text, generate_title, translate_concept
    try:
        explanation = await translate_concept(translation.text, translation.source_lang, translation.target_lang, session, explicit_model=model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    translation.search_count += 1
    session.add(translation)
    
    chat = TranslationChat(translation_id=translation.id, role="assistant", content=explanation, session_id=translation.session_id)
    session.add(chat)
    session.commit()
    session.refresh(chat)
    chats = session.exec(select(TranslationChat).where(TranslationChat.translation_id == translation.id).order_by(TranslationChat.created_at)).all()
    return {"translation": translation.model_dump(), "chats": [c.model_dump() for c in chats]}

@app.post("/api/translations/chat")
async def chat_translation(request: Request, session: Session = Depends(get_session)):
    data = await request.json()
    translation_id = data.get("translation_id")
    content = data.get("content")
    
    if not translation_id or not content:
        raise HTTPException(status_code=400)
        
    translation = session.get(Translation, translation_id)
    if not translation:
        raise HTTPException(status_code=404)
        
    user_chat = TranslationChat(translation_id=translation.id, role="user", content=content, session_id=translation.session_id)
    session.add(user_chat)
    session.commit()
    
    past_chats = session.exec(select(TranslationChat).where(TranslationChat.translation_id == translation_id).order_by(TranslationChat.created_at)).all()
    
    messages = [{"role": "system", "content": "You are a helpful linguistic assistant."}]
    messages.append({"role": "user", "content": f"Source Language: {translation.source_lang}\nTarget Language: {translation.target_lang}\nConcept: {translation.text}"})
    for c in past_chats:
        messages.append({"role": c.role, "content": c.content})
        
    from .ai import chat_conversation, correct_text, generate_title, chat_with_translation
    try:
        response = await chat_with_translation(messages, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    asst_chat = TranslationChat(translation_id=translation.id, role="assistant", content=response, session_id=translation.session_id)
    session.add(asst_chat)
    session.commit()
    
    return {"response": response, "chat_id": asst_chat.id}

@app.get("/api/translations")
async def get_translations(profile_id: int = 1, session: Session = Depends(get_session)):
    translations = session.exec(select(Translation).where(Translation.profile_id == profile_id).order_by(Translation.updated_at.desc())).all()
    results = []
    for t in translations:
        chats = session.exec(select(TranslationChat).where(TranslationChat.translation_id == t.id).order_by(TranslationChat.created_at)).all()
        results.append({
            "id": t.id,
            "text": t.text,
            "source_lang": t.source_lang,
            "target_lang": t.target_lang,
            "search_count": t.search_count,
            "color": t.color,
            "tag": t.tag,
            "session_id": t.session_id,
            "created_at": t.created_at,
            "updated_at": t.updated_at,
            "chats": [{"id": c.id, "role": c.role, "content": c.content, "created_at": c.created_at} for c in chats]
        })
    return results

@app.delete("/api/translations/{translation_id}")
async def delete_translation(translation_id: int, session: Session = Depends(get_session)):
    translation = session.get(Translation, translation_id)
    if translation:
        chats = session.exec(select(TranslationChat).where(TranslationChat.translation_id == translation_id)).all()
        for c in chats:
            session.delete(c)
        session.delete(translation)
        session.commit()
    return {"status": "ok"}

@app.patch("/api/translations/{translation_id}/rename")
async def rename_translation(translation_id: int, request: Request, session: Session = Depends(get_session)):
    translation = session.get(Translation, translation_id)
    if not translation:
        raise HTTPException(status_code=404)
    data = await request.json()
    if 'term' in data:
        translation.text = data['term']
        session.add(translation)
        session.commit()
        session.refresh(translation)
    return {"text": translation.text}

@app.patch("/api/translations/{translation_id}/color")
async def color_translation(translation_id: int, request: Request, session: Session = Depends(get_session)):
    translation = session.get(Translation, translation_id)
    if not translation:
        raise HTTPException(status_code=404)
    data = await request.json()
    if 'color' in data:
        translation.color = data['color']
        session.add(translation)
        session.commit()
        session.refresh(translation)
    return {"color": translation.color}

@app.patch("/api/translations/{translation_id}/tag")
async def tag_translation(translation_id: int, request: Request, session: Session = Depends(get_session)):
    translation = session.get(Translation, translation_id)
    if not translation:
        raise HTTPException(status_code=404)
    data = await request.json()
    if 'tag' in data:
        translation.tag = data['tag']
        session.add(translation)
        session.commit()
        session.refresh(translation)
    return {"tag": translation.tag}

@app.patch("/api/translations/chats/{chat_id}")
async def edit_translation_chat(chat_id: int, request: Request, session: Session = Depends(get_session)):
    data = await request.json()
    content = data.get("content")
    if not content:
        raise HTTPException(status_code=400)
    chat = session.get(TranslationChat, chat_id)
    if not chat:
        raise HTTPException(status_code=404)
    chat.content = content
    session.add(chat)
    session.commit()
    return {"status": "ok"}

@app.get("/api/translations/{translation_id}/preview")
async def get_translation_preview(translation_id: int, session: Session = Depends(get_session)):
    chat = session.exec(select(TranslationChat).where(TranslationChat.translation_id == translation_id, TranslationChat.role == "assistant").order_by(TranslationChat.created_at)).first()
    if chat:
        return {"content": chat.content}
    return {"content": ""}



from .ai import get_system_prompt, get_comparison_prompt, get_explain_prompt, get_translation_prompt

@app.get("/api/settings/defaults")
def get_settings_defaults(session: Session = Depends(get_session)):
    # Create a temporary session or pass None if they don't require session for defaults
    # Wait, the get_*_prompt functions take a session to check DB first.
    # To get the raw default, we can just read the fallbacks.
    # Actually, let's just hardcode the fallbacks here or return the get_*_prompt results if they are not in DB.
    # Wait, if they ARE in DB, get_*_prompt returns the DB version!
    # So we should just read the hardcoded strings.
    import os
    prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        dict_prompt = f.read()
    
    return {
        "DICT_PROMPT": dict_prompt,
        "COMPARE_PROMPT": """You are a multilingual language explainer designed for exhaustive and practical comparisons.
When given a list of words separated by commas or semicolons, your task is to compare them in detail.
Focus on:
1. Core definitions and nuances of each word.
2. The specific differences in meaning, tone, register, and contexts of use.
3. Explicitly state when the words can be used interchangeably and when they cannot.
4. Clear, practical examples demonstrating when to use which word.
5. Common collocations or set phrases for each.
Structure your response clearly with Markdown headings and bullet points.
Aim for an exhaustive and practical explanation.""",
        "EXPLAIN_PROMPT": """You are a multilingual language explainer designed for comprehensive sentence and paragraph analysis.
When the user provides a sentence or paragraph, break it down and explain it in detail.
Focus on:
1. The overall meaning and nuance.
2. Important vocabulary words and their specific definitions in this context.
3. Grammar and syntax structures used.
4. Idioms, cultural references, or expressions.
Use clear Markdown formatting with headings and bullet points.""",
        "TRANSLATE_PROMPT": """You are a highly advanced multilingual "reverse dictionary" and language explainer. The user will provide a concept or phrase in the Source language and wants to know how to express it in the Target language.

Structure your response with clear Markdown headings and bullet points. Please provide:

1. **Core Expressions**: All the common and accurate ways to translate or express this concept in the Target language.
2. **Detailed Comparison**: Compare these expressions exhaustively (nuances, tone, formality, register, and regional usage). Explicitly state when they can be used interchangeably and when they cannot.
3. **Examples**: Provide natural, everyday examples for each expression.
4. **Cultural/Contextual Notes**: Mention any important cultural context or idioms if relevant."""
    }

@app.get("/api/settings")
def get_settings(session: Session = Depends(get_session)):
    settings_db = session.exec(select(AppSetting)).all()
    templates = session.exec(select(ExternalLinkTemplate)).all()
    return {
        "settings": {s.key: s.value for s in settings_db},
        "templates": [t.model_dump() for t in templates]
    }

@app.post("/api/settings")
def save_setting(req: AppSettingItem, session: Session = Depends(get_session)):
    setting = session.get(AppSetting, req.key)
    if setting:
        setting.value = req.value
    else:
        setting = AppSetting(key=req.key, value=req.value)
    session.add(setting)
    session.commit()
    return {"status": "ok"}

@app.post("/api/templates")
def add_template(req: LinkTemplateModel, session: Session = Depends(get_session)):
    t = ExternalLinkTemplate(name=req.name, language=req.language, url_template=req.url_template, icon_url=req.icon_url)
    session.add(t)
    session.commit()
    session.refresh(t)
    return t.model_dump()

@app.delete("/api/templates/{tid}")
def delete_template(tid: int, session: Session = Depends(get_session)):
    t = session.get(ExternalLinkTemplate, tid)
    if t:
        session.delete(t)
        session.commit()
    return {"status": "ok"}

@app.put("/api/templates/{tid}")
def update_template(tid: int, req: LinkTemplateModel, session: Session = Depends(get_session)):
    t = session.get(ExternalLinkTemplate, tid)
    if not t:
        raise HTTPException(status_code=404, detail="Template not found")
    t.name = req.name
    t.language = req.language
    t.url_template = req.url_template
    t.icon_url = req.icon_url
    session.add(t)
    session.commit()
    session.refresh(t)
    return t.model_dump()

class ImportSettingsRequest(BaseModel):
    settings: dict
    templates: list[LinkTemplateModel]

@app.get("/api/settings/export")
def export_settings(session: Session = Depends(get_session)):
    settings_db = session.exec(select(AppSetting)).all()
    templates = session.exec(select(ExternalLinkTemplate)).all()
    return {
        "settings": {s.key: s.value for s in settings_db},
        "templates": [{"name": t.name, "language": t.language, "url_template": t.url_template, "icon_url": t.icon_url} for t in templates]
    }

@app.post("/api/settings/import")
def import_settings(req: ImportSettingsRequest, session: Session = Depends(get_session)):
    for k, v in req.settings.items():
        setting = session.get(AppSetting, k)
        if setting:
            setting.value = v
        else:
            setting = AppSetting(key=k, value=v)
        session.add(setting)
    
    existing_templates = session.exec(select(ExternalLinkTemplate)).all()
    for t in existing_templates:
        session.delete(t)
    
    for t in req.templates:
        session.add(ExternalLinkTemplate(name=t.name, language=t.language, url_template=t.url_template, icon_url=t.icon_url))
        
    session.commit()
    return {"status": "ok"}

@app.get("/api/words/{word_id}/preview")
def preview_word(word_id: int, session: Session = Depends(get_session)):
    chat = session.exec(select(ChatMessage).where(ChatMessage.word_id == word_id).order_by(ChatMessage.created_at)).first()
    return {"content": chat.content if chat else "No explanation found."}

@app.get("/api/comparisons/{comparison_id}/preview")
def preview_comparison(comparison_id: int, session: Session = Depends(get_session)):
    chat = session.exec(select(ComparisonChat).where(ComparisonChat.comparison_id == comparison_id).order_by(ComparisonChat.created_at)).first()
    return {"content": chat.content if chat else "No explanation found."}

@app.get("/api/explains/{explain_id}/preview")
def preview_explain(explain_id: int, session: Session = Depends(get_session)):
    chat = session.exec(select(ExplainChat).where(ExplainChat.explain_id == explain_id).order_by(ExplainChat.created_at)).first()
    return {"content": chat.content if chat else "No explanation found."}


@app.get("/api/data/export")
def export_data(type: str = "all", session: Session = Depends(get_session)):
    data = {}
    if type in ["all", "words"]:
        data["words"] = [w.model_dump() for w in session.exec(select(Word)).all()]
        data["chat_messages"] = [c.model_dump() for c in session.exec(select(ChatMessage)).all()]
    if type in ["all", "comparisons"]:
        data["comparisons"] = [c.model_dump() for c in session.exec(select(Comparison)).all()]
        data["comparison_chats"] = [c.model_dump() for c in session.exec(select(ComparisonChat)).all()]
    if type in ["all", "explains"]:
        data["explains"] = [c.model_dump() for c in session.exec(select(Explain)).all()]
        data["explain_chats"] = [c.model_dump() for c in session.exec(select(ExplainChat)).all()]
    
    # Dates are converted to strings automatically by FastAPI/Pydantic
    return data


@app.get("/api/data/export_zip")
def export_data_zip():
    from .config import db_path
    
    # Create an in-memory zip file containing the db file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        if os.path.exists(db_path):
            zip_file.write(db_path, "ai_dict.db")
            
    zip_buffer.seek(0)
    
    # Write to a temporary file to serve via FileResponse, since FileResponse needs a path
    # Or we can return StreamingResponse
    from fastapi.responses import StreamingResponse
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"ai_dict_backup_{timestamp}.zip"
    return StreamingResponse(
        iter([zip_buffer.getvalue()]), 
        media_type="application/zip", 
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/data/import_zip")
async def import_data_zip(file: UploadFile = File(...)):
    from .config import db_path
    
    content = await file.read()
    zip_buffer = io.BytesIO(content)
    
    try:
        with zipfile.ZipFile(zip_buffer, "r") as zip_ref:
            if "ai_dict.db" not in zip_ref.namelist():
                raise HTTPException(status_code=400, detail="Invalid backup file: ai_dict.db not found in zip.")
            
            # Dispose engine connections so we can overwrite safely
            engine.dispose()
            
            # Extract and replace
            temp_extract_dir = os.path.dirname(db_path)
            zip_ref.extract("ai_dict.db", path=temp_extract_dir)
            
            # Engine will automatically reconnect on next query
            return {"status": "ok"}
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid zip file.")

@app.delete("/api/data/clear")
def clear_data(type: str = "all", session: Session = Depends(get_session)):
    if type in ["all", "words"]:
        for c in session.exec(select(ChatMessage)).all(): session.delete(c)
        for w in session.exec(select(Word)).all(): session.delete(w)
    if type in ["all", "comparisons"]:
        for c in session.exec(select(ComparisonChat)).all(): session.delete(c)
        for c in session.exec(select(Comparison)).all(): session.delete(c)
    if type in ["all", "explains"]:
        for c in session.exec(select(ExplainChat)).all(): session.delete(c)
        for c in session.exec(select(Explain)).all(): session.delete(c)
    session.commit()
    return {"status": "ok"}

@app.post("/api/data/import")
async def import_data(request: Request, type: str = "all", session: Session = Depends(get_session)):
    data = await request.json()
    
    # First clear existing data of that type
    if type in ["all", "words"] and "words" in data:
        for c in session.exec(select(ChatMessage)).all(): session.delete(c)
        for w in session.exec(select(Word)).all(): session.delete(w)
    if type in ["all", "comparisons"] and "comparisons" in data:
        for c in session.exec(select(ComparisonChat)).all(): session.delete(c)
        for c in session.exec(select(Comparison)).all(): session.delete(c)
    if type in ["all", "explains"] and "explains" in data:
        for c in session.exec(select(ExplainChat)).all(): session.delete(c)
        for c in session.exec(select(Explain)).all(): session.delete(c)
    
    session.commit()
    
    # Insert new data
    from datetime import datetime
    
    def parse_dt(dt_str):
        if not dt_str: return datetime.utcnow()
        if isinstance(dt_str, datetime): return dt_str
        try:
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except:
            return datetime.utcnow()
            
    if type in ["all", "words"] and "words" in data:
        for w in data.get("words", []):
            session.add(Word(id=w["id"], term=w["term"], language=w.get("language"), lemma=w.get("lemma"), search_count=w.get("search_count", 1), color=w.get("color"), created_at=parse_dt(w.get("created_at")), updated_at=parse_dt(w.get("updated_at"))))
        for c in data.get("chat_messages", []):
            session.add(ChatMessage(id=c["id"], word_id=c["word_id"], role=c["role"], content=c["content"], created_at=parse_dt(c.get("created_at"))))
            
    if type in ["all", "comparisons"] and "comparisons" in data:
        for c in data.get("comparisons", []):
            session.add(Comparison(id=c["id"], terms=c["terms"], search_count=c.get("search_count", 1), created_at=parse_dt(c.get("created_at")), updated_at=parse_dt(c.get("updated_at"))))
        for c in data.get("comparison_chats", []):
            session.add(ComparisonChat(id=c["id"], comparison_id=c["comparison_id"], role=c["role"], content=c["content"], created_at=parse_dt(c.get("created_at"))))
            
    if type in ["all", "explains"] and "explains" in data:
        for c in data.get("explains", []):
            session.add(Explain(id=c["id"], text=c["text"], search_count=c.get("search_count", 1), created_at=parse_dt(c.get("created_at")), updated_at=parse_dt(c.get("updated_at"))))
        for c in data.get("explain_chats", []):
            session.add(ExplainChat(id=c["id"], explain_id=c["explain_id"], role=c["role"], content=c["content"], created_at=parse_dt(c.get("created_at"))))
            
    session.commit()
    return {"status": "ok"}

# --- Profiles API ---
class ProfileCreate(BaseModel):
    name: str

@app.get("/api/profiles")
def get_profiles(session: Session = Depends(get_session)):
    return session.exec(select(Profile).order_by(Profile.rank, Profile.id)).all()


class ProfileReorder(BaseModel):
    profile_ids: List[int]

@app.post("/api/profiles/reorder")
def reorder_profiles(req: ProfileReorder, session: Session = Depends(get_session)):
    for idx, pid in enumerate(req.profile_ids):
        p = session.get(Profile, pid)
        if p:
            p.rank = idx
            session.add(p)
    session.commit()
    return {"status": "ok"}

@app.post("/api/profiles")
def create_profile(req: ProfileCreate, session: Session = Depends(get_session)):
    p = Profile(name=req.name)
    session.add(p)
    session.commit()
    session.refresh(p)
    return p


class ProfileRename(BaseModel):
    name: str

@app.patch("/api/profiles/{profile_id}/rename")
def rename_profile(profile_id: int, req: ProfileRename, session: Session = Depends(get_session)):
    p = session.get(Profile, profile_id)
    if not p:
        raise HTTPException(status_code=404, detail="Not found")
    p.name = req.name
    session.add(p)
    session.commit()
    session.refresh(p)
    return p


@app.patch("/api/profiles/{profile_id}/set_default")
def set_default_profile(profile_id: int, session: Session = Depends(get_session)):
    p = session.get(Profile, profile_id)
    if not p:
        raise HTTPException(status_code=404, detail="Not found")
        
    # Remove default from others
    for other in session.exec(select(Profile).where(Profile.is_default == True)).all():
        other.is_default = False
        session.add(other)
        
    p.is_default = True
    session.add(p)
    session.commit()
    return {"status": "ok"}

@app.delete("/api/profiles/{profile_id}")
def delete_profile(profile_id: int, session: Session = Depends(get_session)):
    p = session.get(Profile, profile_id)
    if not p:
        raise HTTPException(status_code=404, detail="Not found")
    if p.is_default:
        raise HTTPException(status_code=400, detail="Cannot delete the default profile")
    if not p:
        raise HTTPException(status_code=404, detail="Not found")
    
    # cascade delete history
    for w in session.exec(select(Word).where(Word.profile_id == profile_id)).all():
        session.delete(w)
    for c in session.exec(select(Comparison).where(Comparison.profile_id == profile_id)).all():
        session.delete(c)
    for t in session.exec(select(Translation).where(Translation.profile_id == profile_id)).all():
        session.delete(t)
    for e in session.exec(select(Explain).where(Explain.profile_id == profile_id)).all():
        session.delete(e)
        
    session.delete(p)
    session.commit()
    return {"status": "deleted"}




class RenameSessionReq(BaseModel):
    new_name: str

@app.patch("/api/sessions/{session_id}")
def rename_session(session_id: str, req: RenameSessionReq, session: Session = Depends(get_session)):
    new_name = req.new_name.strip()
    if not new_name:
        raise HTTPException(status_code=400, detail="New name cannot be empty")
        
    for table in [Word, Comparison, Explain, Conversation, Correction, Translation]:
        items = session.exec(select(table).where(table.session_id == session_id)).all()
        for item in items:
            item.session_id = new_name
            session.add(item)
            
    session.commit()
    return {"status": "ok", "new_name": new_name}

@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str, session: Session = Depends(get_session)):
    words = session.exec(select(Word).where(Word.session_id == session_id)).all()
    for w in words:
        chats = session.exec(select(ChatMessage).where(ChatMessage.word_id == w.id)).all()
        for c in chats: session.delete(c)
        session.delete(w)
        
    comps = session.exec(select(Comparison).where(Comparison.session_id == session_id)).all()
    for c in comps:
        chats = session.exec(select(ComparisonChat).where(ComparisonChat.comparison_id == c.id)).all()
        for chat in chats: session.delete(chat)
        session.delete(c)
        
    exps = session.exec(select(Explain).where(Explain.session_id == session_id)).all()
    for e in exps:
        chats = session.exec(select(ExplainChat).where(ExplainChat.explain_id == e.id)).all()
        for chat in chats: session.delete(chat)
        session.delete(e)
        
    session.commit()
    return {"status": "ok"}

# --- Conversations ---

# --- Static Frontend Serving ---
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_path, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        index_file = os.path.join(static_path, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
        return "Frontend not built yet. Run npm run build in frontend."
else:
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        return "Frontend static files not found."

