import os
import re
from openai import AsyncOpenAI
from sqlmodel import Session, select

def apply_reasoning_level(kwargs: dict, level: str):
    if not level or level.lower() in ("default", ""):
        return
    level = level.lower()
    
    if level == "none":
        kwargs["reasoning"] = {"type": "none"}
        return

    kwargs["reasoning"] = {"effort": level}
    
    mapping = {
        "minimal": 1024,
        "low": 2048,
        "medium": 4096,
        "high": 8192,
        "xhigh": 16384,
        "max": 32000
    }
    budget = mapping.get(level, 4096)
    if "provider" not in kwargs:
        kwargs["provider"] = {}
    kwargs["provider"]["anthropic"] = {"thinking": {"type": "enabled", "budget_tokens": budget}}

def apply_reasoning(kwargs: dict, session, model_key: str):
    level = get_model(session, model_key.replace("MODEL", "REASONING"))
    apply_reasoning_level(kwargs, level)

from .config import settings
from .db import AppSetting


def get_model(session: Session, key: str) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == key)).first()
    if setting and setting.value:
        return setting.value
    return ""

def get_api_key(session: Session) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == "OPENROUTER_API_KEY")).first()
    if setting and setting.value:
        return setting.value
    return settings.openrouter_api_key

def get_main_model(session: Session) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == "MAIN_MODEL")).first()
    if setting and setting.value:
        return setting.value
    return settings.default_model

def get_chat_model(session: Session) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == "CHAT_MODEL")).first()
    if setting and setting.value:
        return setting.value
    return settings.chat_model

def get_compare_model(session: Session) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == "COMPARE_MODEL")).first()
    if setting and setting.value:
        return setting.value
    return settings.compare_model

def get_system_prompt(session: Session) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == "DICT_PROMPT")).first()
    if setting and setting.value:
        return setting.value
    prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "You are a multilingual language explainer designed for one-shot use."


def get_explain_prompt(session: Session) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == "EXPLAIN_PROMPT")).first()
    if setting and setting.value:
        return setting.value
    return """You are a multilingual language explainer designed for comprehensive sentence and paragraph analysis.
When the user provides a sentence or paragraph, break it down and explain it in detail.
Focus on:
1. The overall meaning and nuance.
2. Important vocabulary words and their specific definitions in this context.
3. Grammar and syntax structures used.
4. Idioms, cultural references, or expressions.
Use clear Markdown formatting with headings and bullet points."""

async def explain_word(word: str, session: Session, explicit_model: str = None, target_language: str = None, source_language: str = None) -> str:
    api_key = get_api_key(session)
    if not api_key:
        raise ValueError("OpenRouter API Key is missing. Please set it in Settings.")
    
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    system_prompt = get_system_prompt(session)
    model = explicit_model if explicit_model else get_main_model(session)
    
    # We pass the word directly to the LLM
    user_content = word
    instructions = []
    if source_language and source_language != "Auto Detect":
        instructions.append(f"Assume the original word/phrase is in {source_language}.")
    if target_language and target_language != "Auto Detect":
        instructions.append(f"Write your explanation in {target_language}.")
        
    if instructions:
        user_content = f"[{word}]\n\n" + " ".join(instructions)
        
    kwargs = {"model": model, "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]}
    apply_reasoning(kwargs, session, "MAIN_MODEL")
    response = await client.chat.completions.create(**kwargs)
    
    return response.choices[0].message.content

async def chat_with_word(messages: list[dict], session: Session) -> str:
    api_key = get_api_key(session)
    if not api_key:
        raise ValueError("OpenRouter API Key is missing.")
        
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    model = get_chat_model(session)
    kwargs = {"model": model, "messages": messages}
    apply_reasoning(kwargs, session, "CHAT_MODEL")
    response = await client.chat.completions.create(**kwargs)
    return response.choices[0].message.content

def extract_language_and_lemma(markdown_content: str):
    # Try to extract Language and Lemma from the markdown
    # Based on the system prompt structure
    language_match = re.search(r'\*\*Language:?\*\*:?\s*([^\n]+)', markdown_content, re.IGNORECASE)
    lemma_match = re.search(r'\*\*Base form \(lemma\):?\*\*:?\s*([^\n]+)', markdown_content, re.IGNORECASE)
    
    language = language_match.group(1).strip() if language_match else None
    lemma = lemma_match.group(1).strip() if lemma_match else None
    return language, lemma

def get_comparison_prompt(session: Session) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == "COMPARE_PROMPT")).first()
    if setting and setting.value:
        return setting.value
    return """You are a multilingual language explainer designed for exhaustive and practical comparisons.
When given a list of words separated by commas or semicolons, your task is to compare them in detail.
Focus on:
1. Core definitions and nuances of each word.
2. The specific differences in meaning, tone, register, and contexts of use.
3. Explicitly state when the words can be used interchangeably and when they cannot.
4. Clear, practical examples demonstrating when to use which word.
5. Common collocations or set phrases for each.
Structure your response clearly with Markdown headings and bullet points.
Aim for an exhaustive and practical explanation."""

async def compare_words(terms: str, session: Session, explicit_model: str = None) -> str:
    api_key = get_api_key(session)
    if not api_key:
        raise ValueError("OpenRouter API Key is missing. Please set it in Settings.")
    
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    system_prompt = get_comparison_prompt(session)
    model = explicit_model if explicit_model else get_compare_model(session)
    
    kwargs = {"model": model, "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Compare these words: {terms}"}
        ]}
    apply_reasoning(kwargs, session, "COMPARE_MODEL")
    response = await client.chat.completions.create(**kwargs)
    
    return response.choices[0].message.content

async def chat_with_comparison(messages: list[dict], session: Session) -> str:
    api_key = get_api_key(session)
    if not api_key:
        raise ValueError("OpenRouter API Key is missing.")
        
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    model = get_chat_model(session)
    kwargs = {"model": model, "messages": messages}
    apply_reasoning(kwargs, session, "CHAT_MODEL")
    response = await client.chat.completions.create(**kwargs)
    return response.choices[0].message.content

async def explain_text(text: str, session: Session, explicit_model: str = None) -> str:
    api_key = get_api_key(session)
    if not api_key:
        raise ValueError("OpenRouter API Key is missing. Please set it in Settings.")
    
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    system_prompt = get_explain_prompt(session)
    model = explicit_model if explicit_model else get_main_model(session)
    
    kwargs = {"model": model, "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please explain this sentence/paragraph:\n{text}"}
        ]}
    apply_reasoning(kwargs, session, "MAIN_MODEL")
    response = await client.chat.completions.create(**kwargs)
    
    return response.choices[0].message.content

async def chat_with_explain(messages: list[dict], session: Session) -> str:
    api_key = get_api_key(session)
    if not api_key:
        raise ValueError("OpenRouter API Key is missing.")
        
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    model = get_chat_model(session)
    kwargs = {"model": model, "messages": messages}
    apply_reasoning(kwargs, session, "CHAT_MODEL")
    response = await client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


def get_translation_prompt(session: Session) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == "TRANSLATE_PROMPT")).first()
    if setting and setting.value:
        return setting.value
    return """You are a highly advanced multilingual "reverse dictionary" and language explainer. The user will provide a concept or phrase in the Source language and wants to know how to express it in the Target language.

Structure your response with clear Markdown headings and bullet points. Please provide:

1. **Core Expressions**: All the common and accurate ways to translate or express this concept in the Target language.
2. **Detailed Comparison**: Compare these expressions exhaustively (nuances, tone, formality, register, and regional usage). Explicitly state when they can be used interchangeably and when they cannot.
3. **Common Combinations & Collocations**: Provide common combinations, collocations, set phrases, or idioms that use these translated words.
4. **Practical Examples**: Clear sentence examples demonstrating the context and usage of each expression.

Aim to combine the exhaustive depth of a comprehensive dictionary with the nuanced practical analysis of a comparative guide."""

async def translate_concept(text: str, source_lang: str, target_lang: str, session: Session, explicit_model: str = None) -> str:
    api_key = get_api_key(session)
    if not api_key:
        raise ValueError("OpenRouter API Key is missing. Please set it in Settings.")
    
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    system_prompt = get_translation_prompt(session)
    model = explicit_model if explicit_model else get_main_model(session)
    
    kwargs = {"model": model, "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Source language: {source_lang}\nTarget language: {target_lang}\nConcept: {text}"}
        ]}
    apply_reasoning(kwargs, session, "TRANSLATION_MODEL")
    response = await client.chat.completions.create(**kwargs)
    
    return response.choices[0].message.content

async def chat_with_translation(messages: list[dict], session: Session) -> str:
    api_key = get_api_key(session)
    if not api_key:
        raise ValueError("OpenRouter API Key is missing.")
        
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    model = get_chat_model(session)
    kwargs = {"model": model, "messages": messages}
    apply_reasoning(kwargs, session, "CHAT_MODEL")
    response = await client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


def get_conversation_prompt(session: Session) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == "CONVERSATION_PROMPT")).first()
    if setting and setting.value:
        return setting.value
    return "You are a helpful conversational AI assistant. You engage in free-form conversation, provide advice, answer questions, and assist the user with whatever they need. Use Markdown formatting."

async def chat_conversation(topic: str, session: Session, explicit_model: str = None, memory_limit: int = 20, conv=None) -> str:
    api_key = get_api_key(session)
    if not api_key:
        raise ValueError("OpenRouter API Key is missing. Please set it in Settings.")
    
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    prompt = get_conversation_prompt(session)
    if conv and conv.system_prompt:
        prompt = conv.system_prompt
        
    model = explicit_model or get_model(session, "CONVERSATION_MODEL") or get_model(session, "MAIN_MODEL") or "inclusionai/ling-3.0-flash"
    if conv and conv.model:
        model = conv.model
        
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic}
        ]
    }
    if conv:
        apply_reasoning_level(kwargs, conv.thinking)
        
    try:
        response = await client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"OpenRouter API Error: {str(e)}")

def get_correction_prompt(session: Session) -> str:
    setting = session.exec(select(AppSetting).where(AppSetting.key == "CORRECTION_PROMPT")).first()
    if setting and setting.value:
        return setting.value
    return '''You are an expert editor and writing coach. The user will provide a text to be corrected and improved.
Please provide:
1. **Corrected Version**: The text with grammar, spelling, and basic flow issues fixed.
2. **Key Improvements**: Bullet points explaining the major corrections made and why.
3. **Stylistic Advice**: Suggestions for improving tone, vocabulary, or structure.
4. **Enhanced Version**: An alternative, highly polished version of the text if appropriate.
Use Markdown formatting.'''

async def correct_text(text: str, session: Session, explicit_model: str = None, system_prompt: str = None, corr = None) -> str:
    api_key = get_api_key(session)
    if not api_key:
        raise ValueError("OpenRouter API Key is missing. Please set it in Settings.")
    
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    prompt = system_prompt if system_prompt else get_correction_prompt(session)
    model = explicit_model or get_model(session, "CORRECTION_MODEL") or get_model(session, "MAIN_MODEL") or "inclusionai/ling-3.0-flash"
    
    kwargs = {"model": model, "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]}
    apply_reasoning_level(kwargs, corr.thinking) if corr else apply_reasoning(kwargs, session, "CORRECTION_MODEL")
    try:
        response = await client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"OpenRouter API Error: {str(e)}")


async def generate_title(text: str, session: Session) -> str:
    api_key = get_api_key(session)
    if not api_key: return "Untitled"
    client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    prompt = "You are a helpful assistant. Generate a very short, concise title (max 5 words) that summarizes the core topic of the following text. Do not use quotes, punctuation, or generic prefixes like 'Title:'."
    try:
        response = await client.chat.completions.create(
            model="inclusionai/ling-3.0-flash",
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": text}]
        )
        title = response.choices[0].message.content.strip(' "''\n')
        return title
    except:
        return "Untitled"
