import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Copy, Loader2, RefreshCw, BookOpen, Pencil, Check, X, Trash2, Settings, ChevronDown, ChevronUp } from "lucide-react";
import { COLORS } from "./SearchTab";

export default function TranslationTab({ tabId, fetchTranslations, settings, defaultSettings, models, onUpdateTab, initialTranslation, translationSourceLang, setTranslationSourceLang, translationTargetLang, setTranslationTargetLang, translationLangs, setTranslationLangs , profileId}) {
  const [currentTranslation, setCurrentTranslation] = useState(initialTranslation || null)
  const [translationChats, setTranslationChats] = useState([])
  const [translationSearchTerm, setTranslationSearchTerm] = useState(initialTranslation?.text || '')
  const [translationChatInput, setTranslationChatInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [editingChatId, setEditingChatId] = useState(null)
  const [editingContent, setEditingContent] = useState('')

  const handleSaveEdit = async (chatId) => {
    if (!editingContent.trim()) return
    try {
      const res = await fetch(`/api/translations/chats/${chatId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: editingContent })
      })
      if (!res.ok) throw new Error(await res.text())
      const updated = await res.json()
      setTranslationChats(prev => prev.map(c => c.id === chatId ? updated : c))
      setEditingChatId(null)
    } catch (err) {
      alert(err.message)
    }
  }


  // If initialTranslation is provided, fetch its chats
  useEffect(() => {
    if (initialTranslation && !initialTranslation.isTemp && initialTranslation.id && translationChats.length === 0) {
      setLoading(true);
      fetch(`/api/translations/search`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text: initialTranslation.text}) })
        .then(r => r.json())
        .then(d => { setTranslationChats(d.chats); setCurrentTranslation(d.translation); })
        .catch(e => console.error(e))
        .finally(() => setLoading(false))
    }
  }, [initialTranslation]);

  // Update parent tab state for ticks and titles
  useEffect(() => {
    let title = 'New Translation';
    if (translationSearchTerm) title = translationSearchTerm;
    if (currentTranslation && !currentTranslation.isTemp && currentTranslation.content) title = currentTranslation.content.substring(0, 30) + '...';
    onUpdateTab(tabId, { title, loading, hasData: !!currentTranslation && !currentTranslation.isTemp });
  }, [translationSearchTerm, currentTranslation, loading]);

  const handleTranslationSearch = async (e) => {
    e?.preventDefault()
    if (!translationSearchTerm.trim()) return
    setLoading(true)
    setCurrentTranslation({ text: translationSearchTerm, isTemp: true })
    setTranslationChats([])
    try {
      const res = await fetch('/api/translations/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: translationSearchTerm, source_lang: translationSourceLang, target_lang: translationTargetLang, session_id: localStorage.getItem('active_session_id') || undefined, model: settings.TRANSLATION_MODEL || 'inclusionai/ling-3.0-flash' })
      })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setCurrentTranslation(data)
      setTranslationChats(data.chats)
      fetchTranslations()
    } catch (err) {
      alert(err.message)
      setCurrentTranslation(null)
    } finally {
      setLoading(false)
    }
  }

  const handleTranslationRegenerate = async (model) => {
    if (!currentTranslation || currentTranslation.isTemp) return
    setLoading(true)
    try {
      const res = await fetch(`/api/translations/${currentTranslation.id}/regenerate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model })
      })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setCurrentTranslation(data)
      setTranslationChats(data.chats)
    } catch (err) {
      alert(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleTranslationChat = async (e) => {
    e?.preventDefault()
    if (!translationChatInput.trim() || !currentTranslation || currentTranslation.isTemp) return
    const newChat = { role: 'user', content: translationChatInput, id: 'temp' }
    setTranslationChats([...translationChats, newChat])
    setTranslationChatInput('')
    setLoading(true)
    try {
      const res = await fetch('/api/translations/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ translation_id: currentTranslation.id, content: newChat.content })
      })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setTranslationChats(prev => [...prev.filter(c => c.id !== 'temp'), newChat, data])
    } catch (err) {
      alert(err.message)
      setTranslationChats(prev => prev.filter(c => c.id !== 'temp'))
    } finally {
      setLoading(false)
    }
  }

  
  const updateColor = async (colorId) => {
    if (!currentTranslation || currentTranslation.isTemp) return
    const res = await fetch(`/api/translations/${currentTranslation.id}/color`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ color: colorId === currentTranslation.color ? null : colorId })
    })
    if (res.ok) {
      const updated = await res.json()
      setCurrentTranslation(updated)
      fetchTranslations()
    }
  }

  const [copied, setCopied] = useState(false)
  const [showConfig, setShowConfig] = useState(false)
  const [localPrompt, setLocalPrompt] = useState(settings.TRANSLATE_PROMPT || '')
  const activePrompt = localPrompt || (defaultSettings ? defaultSettings.TRANSLATE_PROMPT : '') || ''


  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="h-full flex flex-col p-4 dark:text-gray-100">
      <form onSubmit={handleTranslationSearch} className="flex gap-2 mb-4">
        <input 
          type="text" 
          value={translationSearchTerm}
          onChange={e => setTranslationSearchTerm(e.target.value)}
          placeholder="Text to translate"
          className="flex-1 border dark:border-gray-600 dark:bg-gray-800 rounded-lg p-3 text-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
        <button disabled={loading} type="submit" className="bg-blue-600 hover:bg-blue-700 transition-colors text-white px-6 rounded-lg font-medium flex items-center gap-2 disabled:opacity-50">
          {loading ? <Loader2 className="animate-spin" size={20} /> : <BookOpen size={20} />}
          <span>Translate</span>
        </button>
      </form>

          <div className="flex items-center gap-4 mb-6 mt-[-0.5rem]">
            <select 
              value={translationSourceLang} 
              onChange={(e) => setTranslationSourceLang(e.target.value)}
              className="p-1.5 border dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 shadow-sm text-sm"
            >
              {translationLangs.map(l => <option key={l} value={l}>{l}</option>)}
            </select>
            <button 
              onClick={(e) => {
                e.preventDefault();
                const temp = translationSourceLang;
                setTranslationSourceLang(translationTargetLang);
                setTranslationTargetLang(temp);
              }}
              className="p-1.5 bg-gray-200 dark:bg-gray-700 rounded-full hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors shrink-0"
              title="Swap Languages"
            >
              <RefreshCw size={14} />
            </button>
            <select 
              value={translationTargetLang} 
              onChange={(e) => setTranslationTargetLang(e.target.value)}
              className="p-1.5 border dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 shadow-sm text-sm"
            >
              {translationLangs.map(l => <option key={l} value={l}>{l}</option>)}
            </select>
            <button 
              onClick={(e) => {
                e.preventDefault();
                const newLang = prompt('Add a new language to the list:');
                if (newLang && !translationLangs.includes(newLang)) {
                  setTranslationLangs([...translationLangs, newLang]);
                  setTranslationTargetLang(newLang);
                }
              }}
              className="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs font-medium rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors shrink-0 whitespace-nowrap"
            >
              + New
            </button>
          </div>


      {currentTranslation ? (
        <div className="flex-1 flex flex-col overflow-hidden bg-white dark:bg-gray-900 border dark:border-gray-700 rounded-xl shadow-sm">
          <div className="p-4 border-b dark:border-gray-700 bg-gray-50 dark:bg-gray-800 flex justify-between items-center">
            <div>
              <div className="text-lg font-bold block group resize-y overflow-auto min-h-[4rem] max-h-[50vh] pr-2 w-full custom-scrollbar">
                {currentTranslation.isEditing ? (
                  <textarea 
                    defaultValue={currentTranslation.text} 
                    onBlur={async (e) => {
                      const newTerm = e.target.value;
                      if (newTerm && newTerm !== currentTranslation.text) {
                        const res = await fetch(`/api/translations/${currentTranslation.id}/rename`, {
                          method: 'PATCH',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ term: newTerm })
                        });
                        if (res.ok) {
                          const updated = await res.json();
                          setCurrentTranslation({...currentTranslation, text: updated.text, isEditing: false});
                          fetchTranslations();
                        } else {
                          setCurrentTranslation({...currentTranslation, isEditing: false});
                        }
                      } else {
                        setCurrentTranslation({...currentTranslation, isEditing: false});
                      }
                    }}
                    autoFocus
                    className="border dark:border-gray-600 bg-white dark:bg-gray-800 rounded px-2 py-1 text-lg font-medium w-full h-full min-h-[5rem] custom-scrollbar"
                  />
                ) : (
                  <div className="flex-1 flex gap-2">
                    <span className="whitespace-pre-wrap">{currentTranslation.text}</span>
                    {!currentTranslation.isTemp && (
                      <button 
                        onClick={() => setCurrentTranslation({...currentTranslation, isEditing: true})} 
                        className="flex items-center gap-1 px-2 py-1 bg-gray-200 dark:bg-gray-800 hover:bg-blue-100 dark:hover:bg-blue-900/40 text-gray-700 dark:text-gray-300 hover:text-blue-600 rounded text-sm transition-colors shadow-sm ml-2 shrink-0 h-fit"
                        title="Rename"
                      >
                        <Pencil size={14} /> <span className="text-xs font-medium">Rename</span>
                      </button>
                    )}
                  </div>
                )}
                {currentTranslation.isTemp && <Loader2 className="animate-spin text-blue-500 shrink-0" size={20} />}
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400 mt-1 flex flex-wrap gap-2 items-center">
                {!currentTranslation.isTemp && <span className="bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300 px-2 py-0.5 rounded text-xs font-semibold">{currentTranslation.source_lang} ➔ {currentTranslation.target_lang}</span>}
                {!currentTranslation.isTemp && `• Translated ${currentTranslation.search_count} times`} 
                {!currentTranslation.isTemp && (
                  <span 
                    className="bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 px-2 py-0.5 rounded cursor-pointer hover:bg-purple-200 dark:hover:bg-purple-900/50 transition-colors border border-purple-200 dark:border-purple-800 ml-2"
                    title="Click to edit tag"
                    onClick={async () => {
                      const newTag = prompt('Enter a tag:', currentTranslation.tag || '');
                      if (newTag !== null) {
                        const res = await fetch(`/api/translations/${currentTranslation.id}/tag`, {
                          method: 'PATCH',
                          headers: {'Content-Type': 'application/json'},
                          body: JSON.stringify({ tag: newTag || null })
                        });
                        if (res.ok) {
                          setCurrentTranslation({...currentTranslation, tag: newTag || null});
                          fetchTranslations();
                        }
                      }
                    }}
                  >
                    {currentTranslation.tag ? `#${currentTranslation.tag}` : '+ Add Tag'}
                  </span>
                )}

              </div>
            </div>
            {!currentTranslation.isTemp && (
              <div className="flex gap-2 items-center">
                <div className="relative group">
                  <button className="p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition-colors flex items-center gap-1" title="Regenerate translation">
                    <RefreshCw size={20} />
                  </button>
                  <div className="absolute right-0 top-full pt-1 w-48 hidden group-hover:block z-10">
                    <div className="bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-md shadow-lg overflow-hidden py-1">
                      <div className="px-4 py-2 text-xs text-gray-500 font-bold uppercase tracking-wider">Regenerate with:</div>
                      <button onClick={() => handleTranslationRegenerate(settings.MAIN_MODEL)} className="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">
                        Default Model
                      </button>
                      {(settings.FALLBACK_MODELS || '').split(',').filter(m => m.trim()).map(m => (
                        <button key={m} onClick={() => handleTranslationRegenerate(m.trim())} className="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 truncate" title={m.trim()}>
                          {m.trim()}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
                <button onClick={() => copyToClipboard(translationChats[0]?.content)} className="p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition-colors" title="Copy initial explanation">
                  {copied ? <Check size={20} className="text-green-500" /> : <Copy size={20} />}
                </button>
                <button 
                  onClick={async () => {
                    if (!confirm('Are you sure you want to delete this explanation?')) return;
                    await fetch(`/api/translations/${currentTranslation.id}`, { method: 'DELETE' });
                    fetchTranslations();
                    setCurrentTranslation(null);
                    setTranslationChats([]);
                    setTranslationSearchTerm('');
                  }} 
                  className="p-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors" 
                  title="Delete this translation"
                >
                  <Trash2 size={20} />
                </button>
                <div className="flex gap-1 bg-gray-200 dark:bg-gray-700 p-1 rounded ml-2">
                  {COLORS.map(c => (
                    <button 
                      key={c.id} 
                      onClick={() => updateColor(c.id)}
                      className={`w-6 h-6 rounded-full border-2 border-white dark:border-gray-800 transition-transform ${currentTranslation?.color === c.id ? 'scale-125' : 'hover:scale-110'}`}
                      style={{ backgroundColor: c.hex }}
                      title={c.label}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {translationChats.map((chat, idx) => (
              <div key={chat.id || idx} className={`flex ${chat.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[85%] rounded-xl p-4 relative group ${chat.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-50 dark:bg-gray-800 border dark:border-gray-700 shadow-sm markdown-body dark:text-gray-200'}`}>
                  {editingChatId === chat.id ? (
                    <div className="flex flex-col gap-2">
                      <textarea 
                        value={editingContent}
                        onChange={e => setEditingContent(e.target.value)}
                        className="w-full bg-white dark:bg-gray-900 border dark:border-gray-600 rounded p-2 text-sm min-h-[200px]"
                      />
                      <div className="flex justify-end gap-2">
                        <button onClick={() => setEditingChatId(null)} className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"><X size={16}/></button>
                        <button onClick={() => handleSaveEdit(chat.id)} className="p-1 hover:bg-green-100 dark:hover:bg-green-900/30 text-green-600 rounded"><Check size={16}/></button>
                      </div>
                    </div>
                  ) : (
                    <>
                      {chat.role === 'user' ? chat.content : <ReactMarkdown remarkPlugins={[remarkGfm]}>{chat.content}</ReactMarkdown>}
                      {chat.role !== 'user' && chat.id !== 'temp' && (
                        <button 
                          onClick={() => { setEditingChatId(chat.id); setEditingContent(chat.content); }}
                          className="absolute top-2 right-2 p-1.5 bg-gray-100 dark:bg-gray-700 rounded text-gray-400 hover:text-blue-500 transition-opacity hover:bg-gray-200 dark:hover:bg-gray-600"
                          title="Edit response"
                        >
                          <Pencil size={14} />
                        </button>
                      )}
                    </>
                  )}
                </div>
              </div>
            ))}
            {loading && translationChats.length > 0 && <div className="text-gray-500 dark:text-gray-400 flex items-center gap-2"><Loader2 className="animate-spin" size={16} /> Thinking...</div>}
            {currentTranslation.isTemp && translationChats.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-gray-500 dark:text-gray-400">
                <Loader2 className="animate-spin mb-4" size={32} />
                <p>Generating translation...</p>
              </div>
            )}
          </div>

          {!currentTranslation.isTemp && (
            <form onSubmit={handleTranslationChat} className="p-3 border-t dark:border-gray-700 bg-gray-50 dark:bg-gray-800 flex gap-2">
              <input 
                type="text" 
                value={translationChatInput}
                onChange={e => setTranslationChatInput(e.target.value)}
                placeholder="Ask a follow up question..."
                className="flex-1 border dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              />
              <button disabled={loading} type="submit" className="bg-gray-800 hover:bg-gray-900 dark:bg-gray-700 dark:hover:bg-gray-600 transition-colors text-white px-4 rounded font-medium disabled:opacity-50">Send</button>
            </form>
          )}
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center text-gray-400">
          Enter a concept to translate
        </div>
      )}
    </div>
  )
}
