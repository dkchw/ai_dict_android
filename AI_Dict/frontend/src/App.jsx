import React, { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import SearchTab from './components/SearchTab'
import CompareTab from './components/CompareTab'
import SettingsTab from './components/SettingsTab'
import ExplainTab from './components/ExplainTab'
import TranslationTab from './components/TranslationTab'
import { Search, Globe, History, Settings as SettingsIcon, BookOpen, Share2, Trash2, ExternalLink, Moon, Sun, Loader2, RefreshCw, Library, GitCompare, List , Menu, MessageSquare, ScanLine, Palette, Edit, ChevronUp, ChevronDown } from 'lucide-react'

// Colors for bookmarking: Red (Forgot), Orange (Hard), Yellow (Medium), Green (Easy), Blue (Research)
const COLORS = [
  { id: 'red', hex: '#ef4444', label: 'Forgot' },
  { id: 'orange', hex: '#f97316', label: 'Hard' },
  { id: 'yellow', hex: '#eab308', label: 'Medium' },
  { id: 'green', hex: '#22c55e', label: 'Easy' },
  { id: 'blue', hex: '#3b82f6', label: 'Research' }
]

function HoverReviewPopup({ content, popupSize, setPopupSize }) {
  const popupRef = useRef(null);
  const containerRef = useRef(null);
  const [position, setPosition] = useState({ top: 0, left: 0, isAbove: false });
  

  useEffect(() => {
    if (containerRef.current && popupRef.current) {
      const parentRect = containerRef.current.parentElement.getBoundingClientRect();
      const windowHeight = window.innerHeight;
      const windowWidth = window.innerWidth;
      const popupHeight = popupRef.current.offsetHeight || 300;
      const popupWidth = popupRef.current.offsetWidth || 600;
      
      let newTop = 0;
      let isAbove = false;
      if (parentRect.bottom + popupHeight > windowHeight && parentRect.top > popupHeight) {
        // Place above
        newTop = parentRect.top - popupHeight - 8;
        isAbove = true;
      } else {
        // Place below
        newTop = parentRect.bottom;
        isAbove = false;
      }

      let newLeft = parentRect.left;
      const overflowRight = (parentRect.left + popupWidth) - (windowWidth - 20);
      if (overflowRight > 0) {
        newLeft -= overflowRight;
      }
      
      // Prevent overflow on left
      if (newLeft < 20) {
          newLeft = 20;
      }

      setPosition({ top: newTop, left: newLeft, isAbove });
    }
  }, [content, popupSize]);

  const handleMouseUp = () => {
    if (popupRef.current) {
      const w = popupRef.current.style.width;
      const h = popupRef.current.style.height;
      if (w || h) {
        setPopupSize({ w, h });
        localStorage.setItem('hoverPopupSize', JSON.stringify({ w, h }));
      }
    }
  };

  return (
    <div ref={containerRef} className={`fixed z-[100] ${position.isAbove ? "pb-2" : "pt-2"}`} style={{ top: position.top, left: position.left }}>
      <div 
        ref={popupRef}
        onMouseUp={handleMouseUp}
        style={{ width: popupSize?.w || 'min(600px, 90vw)', height: popupSize?.h || 'auto' }}
        className="p-5 bg-white dark:bg-gray-900 border dark:border-gray-700 rounded-xl shadow-2xl text-sm overflow-auto custom-scrollbar cursor-auto resize min-w-[300px] min-h-[150px] max-w-[90vw] max-h-[80vh]" 
        onClick={e => e.stopPropagation()}
      >
        {content ? (
          <div className="markdown-body">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
          </div>
        ) : (
          <div className="flex justify-center p-4"><Loader2 className="animate-spin text-gray-400" /></div>
        )}
      </div>
    </div>
  );
}

function App() {
  
  const getInitialTab = () => {
    const path = window.location.pathname.replace('/', '')
    const validTabs = ['search', 'compare', 'explain', 'translation', 'flashcards', 'settings']
    if (validTabs.includes(path)) return path
    return 'search'
  }
  const [activeTab, setActiveTab] = useState(getInitialTab())

  useEffect(() => {
    const newPath = `/${activeTab}`
    if (window.location.pathname !== newPath) {
      window.history.pushState(null, '', newPath)
    }
  }, [activeTab])

  useEffect(() => {
    const handlePopState = () => {
      const path = window.location.pathname.replace('/', '')
      const validTabs = ['search', 'compare', 'explain', 'translation', 'flashcards', 'settings']
      if (validTabs.includes(path)) {
        setActiveTab(path)
      }
    }
    window.addEventListener('popstate', handlePopState)
    return () => window.removeEventListener('popstate', handlePopState)
  }, [])
 // search, history, flashcards, settings, compare, compare-history, explain, explain-history
  const [words, setWords] = useState([])
  const [comparisons, setComparisons] = useState([])
  const [explains, setExplains] = useState([])
  
  const [searchTabs, setSearchTabs] = useState([
    { id: 'history', title: 'History' },
    { id: 'init', title: 'New Search', loading: false, hasData: false, initialWord: null }
  ])
  const [activeSearchTabId, setActiveSearchTabId] = useState('init')
  
  const [compareTabs, setCompareTabs] = useState([
    { id: 'history', title: 'History' },
    { id: 'init', title: 'New Compare', loading: false, hasData: false, initialComparison: null }
  ])
  const [activeCompareTabId, setActiveCompareTabId] = useState('init')
  
  const [explainTabs, setExplainTabs] = useState([
    { id: 'history', title: 'History' },
    { id: 'init', title: 'New Explain', loading: false, hasData: false, initialExplain: null }
  ])
  const [activeExplainTabId, setActiveExplainTabId] = useState('init')
  
  const [historySearchTerm, setHistorySearchTerm] = useState('')
  const [compareHistorySearchTerm, setCompareHistorySearchTerm] = useState('')
  const [explainHistorySearchTerm, setExplainHistorySearchTerm] = useState('')
  const [conversations, setConversations] = useState([])
  const [conversationTabs, setConversationTabs] = useState([{ id: 'history', title: 'History' }, { id: 'init', title: 'New Conversation', loading: false, hasData: false, initialConversation: null }])
  const [activeConversationTabId, setActiveConversationTabId] = useState('init')
  const [conversationHistorySearchTerm, setConversationHistorySearchTerm] = useState('')

  const [corrections, setCorrections] = useState([])
  const [correctionTabs, setCorrectionTabs] = useState([{ id: 'history', title: 'History' }, { id: 'init', title: 'New Correction', loading: false, hasData: false, initialCorrection: null }])
  const [activeCorrectionTabId, setActiveCorrectionTabId] = useState('init')
  const [correctionHistorySearchTerm, setCorrectionHistorySearchTerm] = useState('')

  const [translations, setTranslations] = useState([])
  const [translationTabs, setTranslationTabs] = useState([{ id: 'history', title: 'History' }, { id: 'init', title: 'New Translation', loading: false, hasData: false, initialTranslation: null }])
  const [activeTranslationTabId, setActiveTranslationTabId] = useState('init')
  const [translationHistorySearchTerm, setTranslationHistorySearchTerm] = useState('')

  const [searchTargetLang, setSearchTargetLang] = useState(localStorage.getItem('searchTargetLang') || 'Auto Detect')
  const [searchSourceLang, setSearchSourceLang] = useState(localStorage.getItem('searchSourceLang') || 'Auto Detect')
  useEffect(() => { localStorage.setItem('searchTargetLang', searchTargetLang) }, [searchTargetLang])
  useEffect(() => { localStorage.setItem('searchSourceLang', searchSourceLang) }, [searchSourceLang])
  const [translationSourceLang, setTranslationSourceLang] = useState(localStorage.getItem('translationSourceLang') || 'Auto Detect')
  const [translationTargetLang, setTranslationTargetLang] = useState(localStorage.getItem('translationTargetLang') || 'English')
  const [profiles, setProfiles] = useState([])
  const [activeProfileId, setActiveProfileId] = useState(parseInt(localStorage.getItem('activeProfileId')) || 1)
  const [translationLangs, setTranslationLangs] = useState(['Auto Detect', 'English', 'Vietnamese', 'French', 'Spanish', 'German', 'Japanese', 'Chinese', 'Korean', 'Russian', 'Italian', 'Portuguese', 'Dutch', 'Arabic'])
  
  const [settings, setSettings] = useState({ OPENROUTER_API_KEY: '', MAIN_MODEL: '', CHAT_MODEL: '', COMPARE_MODEL: '', FALLBACK_MODELS: '' })
  const [defaultSettings, setDefaultSettings] = useState({})
  const [templates, setTemplates] = useState([])
  const [editingTemplate, setEditingTemplate] = useState(null)
  const [models, setModels] = useState([])
  const [theme, setTheme] = useState('tokyonight')
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [historySort, setHistorySort] = useState('date')
  
  const [hoverReviewMode, setHoverReviewMode] = useState(() => {
    const saved = localStorage.getItem('hoverReviewMode')
    return saved !== null ? JSON.parse(saved) : true
  })
  
  const toggleHoverReviewMode = () => {
    const next = !hoverReviewMode
    setHoverReviewMode(next)
    localStorage.setItem('hoverReviewMode', JSON.stringify(next))
  }
  
  const [hoveredPreviewId, setHoveredPreviewId] = useState(null)
  const [previewContent, setPreviewContent] = useState({})
  
  const [popupSize, setPopupSize] = useState(() => {
    const saved = localStorage.getItem('hoverPopupSize')
    return saved ? JSON.parse(saved) : null
  })
  
  const handleHover = async (id, type) => {
    if (!hoverReviewMode) return;
    setHoveredPreviewId(id);
    if (!previewContent[id]) {
      const endpoint = type === 'search' ? `/api/words/${id}/preview` : type === 'compare' ? `/api/comparisons/${id}/preview` : type === 'translation' ? `/api/translations/${id}/preview` : `/api/explains/${id}/preview`;
      try {
        const res = await fetch(endpoint);
        if (res.ok) {
          const data = await res.json();
          setPreviewContent(prev => ({...prev, [id]: data.content}));
        }
      } catch (e) {
        console.error(e);
      }
    }
  }

  const getGroupedByDay = (items, sortKey) => {
    if (historySort === 'count') {
      return { 'All': [...items].sort((a,b) => (b.search_count || 0) - (a.search_count || 0)) };
    }
    if (historySort === 'alpha') {
      return { 'All': [...items].sort((a,b) => (a[sortKey] || '').localeCompare(b[sortKey] || '')) };
    }
    
    const sorted = [...items].sort((a,b) => new Date(b.updated_at || b.created_at || 0) - new Date(a.updated_at || a.created_at || 0));
    const groups = {};
    sorted.forEach(item => {
      let key;
      if (item.session_id) {
        key = item.session_id;
      } else {
        const d = new Date(item.updated_at || item.created_at || Date.now());
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        
        key = d.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
        if (d.toDateString() === today.toDateString()) key = 'Today';
        else if (d.toDateString() === yesterday.toDateString()) key = 'Yesterday';
      }
      
      if (!groups[key]) groups[key] = [];
      groups[key].push(item);
    });
    return groups;
  }


  const handleRenameSession = async (oldName) => {
    const newName = prompt("Enter new session name:", oldName);
    if (!newName || newName.trim() === '' || newName === oldName) return;
    
    try {
      const res = await fetch(`/api/sessions/${oldName}`, { 
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_name: newName.trim() })
      });
      if (res.ok) {
        if (localStorage.getItem('active_session_id') === oldName) {
          localStorage.setItem('active_session_id', newName.trim());
        }
        fetchProfiles()
    fetchWords();
        fetchComparisons()
    fetchTranslations();
        fetchExplains();
        if(typeof fetchTranslations === 'function') fetchTranslations();
      }
    } catch (e) {
      console.error(e);
    }
  };



  useEffect(() => {
    localStorage.setItem('activeProfileId', activeProfileId)
    fetchWords()
    fetchComparisons()
    fetchExplains()
    fetchTranslations()
  }, [activeProfileId])
  useEffect(() => {
    localStorage.setItem('translationSourceLang', translationSourceLang)
  }, [translationSourceLang])

  useEffect(() => {
    localStorage.setItem('translationTargetLang', translationTargetLang)
  }, [translationTargetLang])

  useEffect(() => {
    fetchProfiles()
    fetchWords()
    fetchComparisons()
    fetchTranslations()
    fetchExplains()
    fetchSettings()
    // Load theme preference
    const savedTheme = localStorage.getItem('theme') || 'tokyonight'
    setTheme(savedTheme)
  }, [])

  useEffect(() => {
    let emoji = '📖';
    let title = 'AI Dict';
    if (activeTab === 'search') {
      const tab = searchTabs.find(t => t.id === activeSearchTabId);
      if (tab) title = tab.title;
      emoji = tab?.id === 'history' ? '🕒' : '📖';
    } else if (activeTab === 'compare') {
      const tab = compareTabs.find(t => t.id === activeCompareTabId);
      if (tab) title = tab.title;
      emoji = tab?.id === 'history' ? '🕒' : '⚖️';
    } else if (activeTab === 'explain') {
      const tab = explainTabs.find(t => t.id === activeExplainTabId);
      if (tab) title = tab.title;
      emoji = tab?.id === 'history' ? '🕒' : '💬';
    } else if (activeTab === 'translation') {
      const tab = translationTabs.find(t => t.id === activeTranslationTabId);
      if (tab) title = tab.title;
      emoji = tab?.id === 'history' ? '🕒' : '🌐';
    } else if (activeTab === 'settings') {
      title = 'Settings';
      emoji = '⚙️';
    } else if (activeTab === 'flashcards') {
      title = 'Flashcards';
      emoji = '🃏';
    }
    document.title = `${emoji} ${title} | AI Dict`;
  }, [activeTab, activeSearchTabId, activeCompareTabId, activeExplainTabId, activeTranslationTabId, searchTabs, compareTabs, explainTabs, translationTabs]);

  useEffect(() => {
    const isDark = theme !== 'light';
    if (isDark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    
    document.documentElement.removeAttribute('data-theme')
    if (theme !== 'light' && theme !== 'dark') {
      document.documentElement.setAttribute('data-theme', theme)
    }
    localStorage.setItem('theme', theme)
  }, [theme])

  useEffect(() => {
    if (settings.OPENROUTER_API_KEY) {
      fetch('https://openrouter.ai/api/v1/models', {
        headers: { 'Authorization': `Bearer ${settings.OPENROUTER_API_KEY}` }
      })
      .then(r => r.json())
      .then(d => {
        if (d.data) setModels(d.data.sort((a,b) => a.id.localeCompare(b.id)))
      })
      .catch(e => console.error(e))
    }
  }, [settings.OPENROUTER_API_KEY])


  const fetchProfiles = async () => {
    try {
      const res = await fetch('/api/profiles')
      if (res.ok) setProfiles(await res.json())
    } catch (e) { console.error(e) }
  }

  const fetchWords = async () => {
    const res = await fetch(`/api/words?profile_id=${activeProfileId}`)
    if (res.ok) setWords(await res.json())
  }

  const fetchComparisons = async () => {
    const res = await fetch(`/api/comparisons?profile_id=${activeProfileId}`)
    if (res.ok) setComparisons(await res.json())
  }

  const fetchTranslations = async () => { try { const res = await fetch(`/api/translations?profile_id=${activeProfileId}`); if (res.ok) setTranslations(await res.json()); } catch (e) { console.error(e) } }

  const fetchExplains = async () => {
    const res = await fetch(`/api/explains?profile_id=${activeProfileId}`)
    if (res.ok) setExplains(await res.json())
  }

  const deleteComparison = async (id) => {
    if (!confirm('Are you sure?')) return
    await fetch(`/api/comparisons/${id}`, { method: 'DELETE' })
    fetchComparisons()
    fetchTranslations()
  }

  
  const deleteTranslation = async (id) => {
    if (!confirm('Are you sure?')) return
    await fetch(`/api/translations/${id}`, { method: 'DELETE' })
    fetchTranslations()
  }

  const deleteExplain = async (id) => {
    if (!confirm('Are you sure?')) return
    await fetch(`/api/explains/${id}`, { method: 'DELETE' })
    fetchExplains()
  }


  const fetchSettings = async () => {
    try {
      const defRes = await fetch('/api/settings/defaults')
      if (defRes.ok) setDefaultSettings(await defRes.json())
    } catch(e) {}
    
    const res = await fetch('/api/settings')

    if (res.ok) {
      const data = await res.json()
      setSettings(prev => ({...prev, ...data.settings}))
      if (!localStorage.getItem('searchTargetLang') && data.settings.SEARCH_TARGET_LANG) {
        setSearchTargetLang(data.settings.SEARCH_TARGET_LANG)
      }
      if (!localStorage.getItem('searchSourceLang') && data.settings.SEARCH_SOURCE_LANG) {
        setSearchSourceLang(data.settings.SEARCH_SOURCE_LANG)
      }
      setTemplates(data.templates)
    }
  }

  const deleteWord = async (id) => {
    if (!confirm('Are you sure?')) return
    await fetch(`/api/words/${id}`, { method: 'DELETE' })
    fetchProfiles()
    fetchWords()
  }

  const updateLanguage = async (id, currentLanguage) => {
    const newLang = prompt('Enter correct language (e.g. German):', currentLanguage || '');
    if (newLang !== null) {
      await fetch(`/api/words/${id}/language`, {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ language: newLang })
      });
      fetchProfiles()
    fetchWords();
    }
  }

  const handleHomeClick = () => {
    handleSearchClick()
  }

  const handleSearchClick = () => {
    const id = Date.now().toString()
    setSearchTabs([...searchTabs, { id, title: 'New Search', loading: false, hasData: false, initialWord: null }])
    setActiveSearchTabId(id)
    setActiveTab('search')
  }

  const handleCompareClick = () => {
    const id = Date.now().toString()
    setCompareTabs([...compareTabs, { id, title: 'New Compare', loading: false, hasData: false, initialComparison: null }])
    setActiveCompareTabId(id)
    setActiveTab('compare')
  }

  const handleExplainClick = () => {
    const id = Date.now().toString()
    setExplainTabs([...explainTabs, { id, title: 'New Explain', loading: false, hasData: false, initialExplain: null }])
    setActiveExplainTabId(id)
    setActiveTab('explain')
  }

  const exportData = async (type) => {
    const res = await fetch(`/api/data/export?type=${type}`)
    const data = await res.json()
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const dateStr = new Date().toISOString().replace(/[:T]/g, '-').split('.')[0]; a.download = `ai_dict_data_${type}_${dateStr}.json`
    a.click()
  }

  const importData = async (type, e) => {
    const file = e.target.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = async (event) => {
      try {
        const data = JSON.parse(event.target.result)
        await fetch(`/api/data/import?type=${type}`, {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(data)
        })
        alert(`${type} imported successfully`)
        fetchProfiles()
    fetchWords()
        fetchExplains()
        fetchComparisons()
    fetchTranslations()
      } catch (err) {
        alert('Invalid JSON file')
      }
    }
    reader.readAsText(file)
  }

  const clearData = async (type) => {
    if (!confirm(`Are you sure you want to delete ALL ${type} history? This cannot be undone.`)) return
    await fetch(`/api/data/clear?type=${type}`, { method: 'DELETE' })
    fetchProfiles()
    fetchWords()
    fetchExplains()
    fetchComparisons()
    fetchTranslations()
  }

  const renderContent = () => {
    if (activeTab === 'settings') {
      return <SettingsTab settings={settings} defaultSettings={defaultSettings} setSettings={setSettings} fetchSettings={fetchSettings} models={models} theme={theme} setTheme={setTheme} templates={templates} setTemplates={setTemplates} editingTemplate={editingTemplate} setEditingTemplate={setEditingTemplate} exportData={exportData} importData={importData} clearData={clearData} />
    }

    if (activeTab === 'compare') {
      const filteredComparisons = comparisons.filter(c => 
        c.terms.toLowerCase().includes(compareHistorySearchTerm.toLowerCase())
      );
      const totalComparisons = filteredComparisons.length;
      const totalSearches = filteredComparisons.reduce((sum, c) => sum + (c.search_count || 0), 0);

      return (
        <div className="h-full flex flex-col">
          <div className="flex bg-gray-100 dark:bg-gray-900 border-b dark:border-gray-800 overflow-x-auto" onWheel={(e) => { if (e.deltaY !== 0) { e.currentTarget.scrollLeft += e.deltaY; } }}>
            {compareTabs.map(t => (
              <div key={t.id} className={`shrink-0 flex items-center gap-2 px-4 py-2 border-r dark:border-gray-800 cursor-pointer ${t.id === activeCompareTabId ? 'bg-white dark:bg-gray-800 font-medium text-blue-600 dark:text-blue-400' : 'hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400'}`} onClick={() => setActiveCompareTabId(t.id)}>
                {t.id === 'history' ? <History size={14} /> : <GitCompare size={14} />}
                <span className="truncate max-w-[150px]">{t.title || 'New Compare'}</span>
                {t.id !== 'history' && (
                  <>
                    {t.loading && <Loader2 size={12} className="animate-spin text-blue-500" />}
                    {!t.loading && t.hasData && <div className="w-2 h-2 rounded-full bg-green-500 shrink-0" title="Done"></div>}
                    <button onClick={(e) => { e.stopPropagation(); setCompareTabs(compareTabs.filter(st => st.id !== t.id)); if(activeCompareTabId === t.id) setActiveCompareTabId(compareTabs[0]?.id || 'history') }} className="ml-2 text-gray-400 hover:text-red-500 shrink-0">&times;</button>
                  </>
                )}
              </div>
            ))}
            <button onClick={() => { const id = Date.now().toString(); setCompareTabs([...compareTabs, { id, title: 'New Compare', loading: false, hasData: false, initialComparison: null }]); setActiveCompareTabId(id) }} className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 font-bold shrink-0">+</button>
          </div>
          <div className="flex-1 overflow-hidden relative bg-gray-100 dark:bg-gray-950">
            {compareTabs.map(t => (
              <div key={t.id} className={t.id === activeCompareTabId ? 'h-full block' : 'hidden'}>
                {t.id === 'history' ? (
                  <div className="h-full overflow-y-auto p-6 text-gray-900 dark:text-gray-100">
                    <div className="flex flex-col xl:flex-row xl:items-center justify-between mb-6 gap-4">
                      <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                        <h2 className="text-2xl font-bold">Comparison History</h2>
                        <div className="relative w-full sm:w-64">
                          <input 
                            type="text" 
                            value={compareHistorySearchTerm}
                            onChange={e => setCompareHistorySearchTerm(e.target.value)}
                            placeholder="Search comparison history..."
                            className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded-lg py-1.5 pl-9 pr-3 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-sm"
                          />
                          <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                        </div>
                        <div className="flex items-center gap-2">
                          <button 
                            onClick={() => toggleHoverReviewMode()}
                            className={`p-1.5 rounded-lg flex items-center gap-1.5 text-sm border shadow-sm transition-colors ${hoverReviewMode ? 'bg-blue-600 border-blue-600 text-white hover:bg-blue-700 dark:bg-blue-600 dark:border-blue-600 dark:text-white dark:hover:bg-blue-700' : 'bg-white border-gray-300 text-gray-600 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700'}`}
                            title="Toggle Quick Review on Hover"
                          >
                            <ScanLine size={16} /> 
                            <span className="hidden sm:inline font-medium">Hover Review</span>
                          </button>
                          <span className="text-sm font-medium text-gray-500 dark:text-gray-400 ml-2">Sort by:</span>
                          <select 
                            value={historySort} 
                            onChange={e => setHistorySort(e.target.value)} 
                            className="border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded-lg py-1.5 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-sm"
                          >
                            <option value="date">Date (Grouped)</option>
                            <option value="count">Most Searched</option>
                            <option value="alpha">Alphabetical</option>
                          </select>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-4 text-sm text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-800 px-4 py-2 rounded-lg border dark:border-gray-700 shadow-sm items-center justify-between w-full">
                        <div className="flex items-center gap-4">
                          <div className="flex items-center gap-1">
                            <span className="font-medium">Total Comparisons:</span> 
                            <span className="text-gray-900 dark:text-gray-100 font-bold">{totalComparisons}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <span className="font-medium">Total Searches:</span> 
                            <span className="text-gray-900 dark:text-gray-100 font-bold">{totalSearches}</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <button onClick={() => {
                              const sessionId = "Session " + new Date().toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
                              localStorage.setItem('active_session_id', sessionId);
                              alert("Started " + sessionId);
                            }} className="px-2 py-1 bg-blue-100 hover:bg-blue-200 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded text-xs font-medium transition-colors">New Session</button>
                            <button onClick={() => exportData('comparisons')} className="px-2 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded text-xs font-medium transition-colors text-gray-700 dark:text-gray-300">Export</button>
                          <label className="px-2 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded text-xs font-medium transition-colors text-gray-700 dark:text-gray-300 cursor-pointer">
                            Import
                            <input type="file" accept=".json" className="hidden" onChange={(e) => importData('comparisons', e)} />
                          </label>
                          <button onClick={() => clearData('comparisons')} className="px-2 py-1 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-600 dark:text-red-400 rounded text-xs font-medium transition-colors">Clear All</button>
                        </div>
                      </div>
                    </div>
                    <div className="grid gap-6">
                      {Object.entries(getGroupedByDay(filteredComparisons, 'terms')).map(([groupName, groupItems]) => (
                        <div key={groupName}>
                          {historySort === 'date' && (
                              <div className="flex items-center justify-between mb-3 border-b dark:border-gray-800 pb-1">
                                <h3 className="text-lg font-bold text-gray-500 dark:text-gray-400">{groupName}</h3>
                                {groupName.startsWith('Session') && (
                                  <button 
                                    onClick={async () => {
                                      if(!confirm(`Delete all data in ${groupName}?`)) return;
                                      await fetch(`/api/sessions/${groupName}`, { method: 'DELETE' });
                                      if(localStorage.getItem('active_session_id') === groupName) localStorage.removeItem('active_session_id');
                                      fetchProfiles()
    fetchWords();
                                      fetchComparisons();
                                      fetchExplains();
                                    }}
                                    className="text-xs text-red-500 hover:text-red-600 transition-colors"
                                  >
                                    Delete Group
                                  </button>
                                )}
                              </div>
                            )}
                          <div className="grid gap-3">
                            {groupItems.map(c => (
                              <div key={c.id} className="border dark:border-gray-700 p-4 rounded-lg flex justify-between items-center bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow relative">
                                <div 
                                  className="flex-1 cursor-pointer" 
                                  onClick={() => {
                                    const id = Date.now().toString();
                                    setCompareTabs([...compareTabs, { id, title: c.terms, loading: true, hasData: false, initialComparison: c }]);
                                    setActiveCompareTabId(id);
                                  }}
                                >
                                  <div 
                                    className="flex items-center gap-2 w-fit relative"
                                    onMouseEnter={() => handleHover(c.id, 'compare')}
                                    onMouseLeave={() => setHoveredPreviewId(null)}
                                  >
                                    <span className="font-bold text-lg">{c.terms}</span>
                                    <span className="text-gray-500 dark:text-gray-400 text-sm">({c.search_count} searches)</span>
                                    {hoverReviewMode && hoveredPreviewId === c.id && (
                                      <HoverReviewPopup content={previewContent[c.id]} popupSize={popupSize} setPopupSize={setPopupSize} />
                                    )}
                                  </div>
                                </div>
                                <button onClick={() => deleteComparison(c.id)} className="text-red-500 p-2 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors"><Trash2 size={20} /></button>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <CompareTab profileId={activeProfileId} tabId={t.id} fetchComparisons={fetchComparisons} settings={settings} defaultSettings={defaultSettings} models={models} initialComparison={t.initialComparison} onUpdateTab={(id, data) => setCompareTabs(prev => prev.map(pt => pt.id === id ? { ...pt, ...data } : pt))} />
                )}
              </div>
            ))}
          </div>
        </div>
      )
    }

    if (activeTab === 'search') {
      const filteredWords = words.filter(w => 
        w.term.toLowerCase().includes(historySearchTerm.toLowerCase()) || 
        w.lemma?.toLowerCase().includes(historySearchTerm.toLowerCase())
      );
      const totalWords = filteredWords.length;
      const totalSearches = filteredWords.reduce((sum, w) => sum + (w.search_count || 0), 0);

      return (
        <div className="h-full flex flex-col">
          <div className="flex bg-gray-100 dark:bg-gray-900 border-b dark:border-gray-800 overflow-x-auto" onWheel={(e) => { if (e.deltaY !== 0) { e.currentTarget.scrollLeft += e.deltaY; } }}>
            {searchTabs.map(t => (
              <div key={t.id} className={`shrink-0 flex items-center gap-2 px-4 py-2 border-r dark:border-gray-800 cursor-pointer ${t.id === activeSearchTabId ? 'bg-white dark:bg-gray-800 font-medium text-blue-600 dark:text-blue-400' : 'hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400'}`} onClick={() => setActiveSearchTabId(t.id)}>
                {t.id === 'history' ? <History size={14} /> : <BookOpen size={14} />}
                <span className="truncate max-w-[150px]">{t.title || 'New Search'}</span>
                {t.id !== 'history' && (
                  <>
                    {t.loading && <Loader2 size={12} className="animate-spin text-blue-500" />}
                    {!t.loading && t.hasData && <div className="w-2 h-2 rounded-full bg-green-500 shrink-0" title="Done"></div>}
                    <button onClick={(e) => { e.stopPropagation(); setSearchTabs(searchTabs.filter(st => st.id !== t.id)); if(activeSearchTabId === t.id) setActiveSearchTabId(searchTabs[0]?.id || 'history') }} className="ml-2 text-gray-400 hover:text-red-500 shrink-0">&times;</button>
                  </>
                )}
              </div>
            ))}
            <button onClick={() => { const id = Date.now().toString(); setSearchTabs([...searchTabs, { id, title: 'New Search', loading: false, hasData: false, initialWord: null }]); setActiveSearchTabId(id) }} className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 font-bold shrink-0">+</button>
          </div>
          <div className="flex-1 overflow-hidden relative bg-gray-100 dark:bg-gray-950">
            {searchTabs.map(t => (
              <div key={t.id} className={t.id === activeSearchTabId ? 'h-full block' : 'hidden'}>
                {t.id === 'history' ? (
                    <div className="h-full overflow-y-auto p-6 text-gray-900 dark:text-gray-100">
                      <div className="flex flex-col xl:flex-row xl:items-center justify-between mb-6 gap-4">
                        <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                          <h2 className="text-2xl font-bold">Search History</h2>
                          <div className="relative w-full sm:w-64">
                            <input 
                              type="text" 
                              value={historySearchTerm}
                              onChange={e => setHistorySearchTerm(e.target.value)}
                              placeholder="Search history..."
                              className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded-lg py-1.5 pl-9 pr-3 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-sm"
                            />
                            <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                          </div>
                          <div className="flex items-center gap-2">
                            <button 
                              onClick={() => toggleHoverReviewMode()}
                              className={`p-1.5 rounded-lg flex items-center gap-1.5 text-sm border shadow-sm transition-colors ${hoverReviewMode ? 'bg-blue-600 border-blue-600 text-white hover:bg-blue-700 dark:bg-blue-600 dark:border-blue-600 dark:text-white dark:hover:bg-blue-700' : 'bg-white border-gray-300 text-gray-600 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700'}`}
                              title="Toggle Quick Review on Hover"
                            >
                              <ScanLine size={16} /> 
                              <span className="hidden sm:inline font-medium">Hover Review</span>
                            </button>
                            <span className="text-sm font-medium text-gray-500 dark:text-gray-400 ml-2">Sort by:</span>
                            <select 
                              value={historySort} 
                              onChange={e => setHistorySort(e.target.value)} 
                              className="border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded-lg py-1.5 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-sm"
                            >
                              <option value="date">Date (Grouped)</option>
                              <option value="count">Most Searched</option>
                              <option value="alpha">Alphabetical</option>
                            </select>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-4 text-sm text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-800 px-4 py-2 rounded-lg border dark:border-gray-700 shadow-sm items-center justify-between w-full">
                          <div className="flex items-center gap-4">
                            <div className="flex items-center gap-1">
                              <span className="font-medium">Total Words:</span> 
                              <span className="text-gray-900 dark:text-gray-100 font-bold">{totalWords}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <span className="font-medium">Total Searches:</span> 
                              <span className="text-gray-900 dark:text-gray-100 font-bold">{totalSearches}</span>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <button onClick={() => {
                              const sessionId = "Session " + new Date().toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
                              localStorage.setItem('active_session_id', sessionId);
                              alert("Started " + sessionId);
                            }} className="px-2 py-1 bg-blue-100 hover:bg-blue-200 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded text-xs font-medium transition-colors">New Session</button>
                            <button onClick={() => exportData('words')} className="px-2 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded text-xs font-medium transition-colors text-gray-700 dark:text-gray-300">Export</button>
                            <label className="px-2 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded text-xs font-medium transition-colors text-gray-700 dark:text-gray-300 cursor-pointer">
                              Import
                              <input type="file" accept=".json" className="hidden" onChange={(e) => importData('words', e)} />
                            </label>
                            <button onClick={() => clearData('words')} className="px-2 py-1 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-600 dark:text-red-400 rounded text-xs font-medium transition-colors">Clear All</button>
                          </div>
                        </div>
                      </div>
                      <div className="grid gap-6">
                        {Object.entries(getGroupedByDay(filteredWords, 'term')).map(([groupName, groupItems]) => (
                          <div key={groupName}>
                            {historySort === 'date' && (
                              <div className="flex items-center justify-between mb-3 border-b dark:border-gray-800 pb-1">
                                <h3 className="text-lg font-bold text-gray-500 dark:text-gray-400">{groupName}</h3>
                                {groupName.startsWith('Session') && (
                                  <button 
                                    onClick={async () => {
                                      if(!confirm(`Delete all data in ${groupName}?`)) return;
                                      await fetch(`/api/sessions/${groupName}`, { method: 'DELETE' });
                                      if(localStorage.getItem('active_session_id') === groupName) localStorage.removeItem('active_session_id');
                                      fetchProfiles()
    fetchWords();
                                      fetchComparisons();
                                      fetchExplains();
                                    }}
                                    className="text-xs text-red-500 hover:text-red-600 transition-colors"
                                  >
                                    Delete Group
                                  </button>
                                )}
                              </div>
                            )}
                            <div className="grid gap-3">
                              {groupItems.map(w => (
                                <div key={w.id} className="border dark:border-gray-700 p-4 rounded-lg flex justify-between items-center bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow relative">
                                  <div 
                                    className="flex-1 cursor-pointer" 
                                    onClick={() => {
                                      const id = Date.now().toString();
                                      setSearchTabs([...searchTabs, { id, title: w.term, loading: true, hasData: false, initialWord: w }]);
                                      setActiveSearchTabId(id);
                                    }}
                                  >
                                    <div 
                                      className="flex items-center gap-2 w-fit relative"
                                      onMouseEnter={() => handleHover(w.id, 'search')}
                                      onMouseLeave={() => setHoveredPreviewId(null)}
                                    >
                                      {w.color && (
                                        <div className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: COLORS.find(c => c.id === w.color)?.hex || w.color }} title={COLORS.find(c => c.id === w.color)?.label} />
                                      )}
                                      <span className="font-bold text-lg">{w.term}</span>
                                      <span className="text-gray-500 dark:text-gray-400 text-sm">({w.search_count} searches)</span>
                                      {hoverReviewMode && hoveredPreviewId === w.id && (
                                        <HoverReviewPopup content={previewContent[w.id]} popupSize={popupSize} setPopupSize={setPopupSize} />
                                      )}
                                    </div>
                                    <div className="text-sm text-gray-500 dark:text-gray-400 mt-1 flex items-center flex-wrap gap-2">
                                      <span 
                                        className="px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                                        title="Click to edit language"
                                        onClick={(e) => { e.stopPropagation(); updateLanguage(w.id, w.language); }}
                                      >
                                        {w.language || '+ Add Language'}
                                      </span>
                                      {w.lemma && <span>Lemma: {w.lemma}</span>}
                                    </div>
                                  </div>
                                  <button onClick={() => deleteWord(w.id)} className="text-red-500 p-2 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors"><Trash2 size={20} /></button>
                                </div>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                ) : (
                  <SearchTab profileId={activeProfileId} searchSourceLang={searchSourceLang} setSearchSourceLang={setSearchSourceLang} searchTargetLang={searchTargetLang} setSearchTargetLang={setSearchTargetLang} translationLangs={translationLangs} tabId={t.id} fetchWords={fetchWords} settings={settings} defaultSettings={defaultSettings} models={models} templates={templates} initialWord={t.initialWord} onUpdateTab={(id, data) => setSearchTabs(prev => prev.map(pt => pt.id === id ? { ...pt, ...data } : pt))} />
                )}
              </div>
            ))}
          </div>
        </div>
      )
    }

    if (activeTab === 'explain') {
      const filteredExplains = explains.filter(c => 
        c.text.toLowerCase().includes(explainHistorySearchTerm.toLowerCase())
      );
      const totalExplains = filteredExplains.length;
      const totalSearches = filteredExplains.reduce((sum, c) => sum + (c.search_count || 0), 0);

      return (
        <div className="h-full flex flex-col">
          <div className="flex bg-gray-100 dark:bg-gray-900 border-b dark:border-gray-800 overflow-x-auto" onWheel={(e) => { if (e.deltaY !== 0) { e.currentTarget.scrollLeft += e.deltaY; } }}>
            {explainTabs.map(t => (
              <div key={t.id} className={`shrink-0 flex items-center gap-2 px-4 py-2 border-r dark:border-gray-800 cursor-pointer ${t.id === activeExplainTabId ? 'bg-white dark:bg-gray-800 font-medium text-blue-600 dark:text-blue-400' : 'hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400'}`} onClick={() => setActiveExplainTabId(t.id)}>
                {t.id === 'history' ? <History size={14} /> : <MessageSquare size={14} />}
                <span className="truncate max-w-[150px]">{t.title || 'New Explain'}</span>
                {t.id !== 'history' && (
                  <>
                    {t.loading && <Loader2 size={12} className="animate-spin text-blue-500" />}
                    {!t.loading && t.hasData && <div className="w-2 h-2 rounded-full bg-green-500 shrink-0" title="Done"></div>}
                    <button onClick={(e) => { e.stopPropagation(); setExplainTabs(explainTabs.filter(st => st.id !== t.id)); if(activeExplainTabId === t.id) setActiveExplainTabId(explainTabs[0]?.id || 'history') }} className="ml-2 text-gray-400 hover:text-red-500 shrink-0">&times;</button>
                  </>
                )}
              </div>
            ))}
            <button onClick={() => { const id = Date.now().toString(); setExplainTabs([...explainTabs, { id, title: 'New Explain', loading: false, hasData: false, initialExplain: null }]); setActiveExplainTabId(id) }} className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 font-bold shrink-0">+</button>
          </div>
          <div className="flex-1 overflow-hidden relative bg-gray-100 dark:bg-gray-950">
            {explainTabs.map(t => (
              <div key={t.id} className={t.id === activeExplainTabId ? 'h-full block' : 'hidden'}>
                {t.id === 'history' ? (
                  <div className="h-full overflow-y-auto p-6 text-gray-900 dark:text-gray-100">
                    <div className="flex flex-col xl:flex-row xl:items-center justify-between mb-6 gap-4">
                      <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                        <h2 className="text-2xl font-bold">Explain History</h2>
                        <div className="relative w-full sm:w-64">
                          <input 
                            type="text" 
                            value={explainHistorySearchTerm}
                            onChange={e => setExplainHistorySearchTerm(e.target.value)}
                            placeholder="Search explain history..."
                            className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded-lg py-1.5 pl-9 pr-3 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-sm"
                          />
                          <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                        </div>
                        <div className="flex items-center gap-2">
                          <button 
                            onClick={() => toggleHoverReviewMode()}
                            className={`p-1.5 rounded-lg flex items-center gap-1.5 text-sm border shadow-sm transition-colors ${hoverReviewMode ? 'bg-blue-600 border-blue-600 text-white hover:bg-blue-700 dark:bg-blue-600 dark:border-blue-600 dark:text-white dark:hover:bg-blue-700' : 'bg-white border-gray-300 text-gray-600 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700'}`}
                            title="Toggle Quick Review on Hover"
                          >
                            <ScanLine size={16} /> 
                            <span className="hidden sm:inline font-medium">Hover Review</span>
                          </button>
                          <span className="text-sm font-medium text-gray-500 dark:text-gray-400 ml-2">Sort by:</span>
                          <select 
                            value={historySort} 
                            onChange={e => setHistorySort(e.target.value)} 
                            className="border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded-lg py-1.5 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-sm"
                          >
                            <option value="date">Date (Grouped)</option>
                            <option value="count">Most Searched</option>
                            <option value="alpha">Alphabetical</option>
                          </select>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-4 text-sm text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-800 px-4 py-2 rounded-lg border dark:border-gray-700 shadow-sm items-center justify-between w-full">
                        <div className="flex items-center gap-4">
                          <div className="flex items-center gap-1">
                            <span className="font-medium">Total Explains:</span> 
                            <span className="text-gray-900 dark:text-gray-100 font-bold">{totalExplains}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <span className="font-medium">Total Searches:</span> 
                            <span className="text-gray-900 dark:text-gray-100 font-bold">{totalSearches}</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <button onClick={() => {
                              const sessionId = "Session " + new Date().toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
                              localStorage.setItem('active_session_id', sessionId);
                              alert("Started " + sessionId);
                            }} className="px-2 py-1 bg-blue-100 hover:bg-blue-200 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded text-xs font-medium transition-colors">New Session</button>
                            <button onClick={() => exportData('explains')} className="px-2 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded text-xs font-medium transition-colors text-gray-700 dark:text-gray-300">Export</button>
                          <label className="px-2 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded text-xs font-medium transition-colors text-gray-700 dark:text-gray-300 cursor-pointer">
                            Import
                            <input type="file" accept=".json" className="hidden" onChange={(e) => importData('explains', e)} />
                          </label>
                          <button onClick={() => clearData('explains')} className="px-2 py-1 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-600 dark:text-red-400 rounded text-xs font-medium transition-colors">Clear All</button>
                        </div>
                      </div>
                    </div>
                    <div className="grid gap-6">
                      {Object.entries(getGroupedByDay(filteredExplains, 'text')).map(([groupName, groupItems]) => (
                        <div key={groupName}>
                          {historySort === 'date' && (
                              <div className="flex items-center justify-between mb-3 border-b dark:border-gray-800 pb-1">
                                <h3 className="text-lg font-bold text-gray-500 dark:text-gray-400">{groupName}</h3>
                                {groupName.startsWith('Session') && (
                                  <button 
                                    onClick={async () => {
                                      if(!confirm(`Delete all data in ${groupName}?`)) return;
                                      await fetch(`/api/sessions/${groupName}`, { method: 'DELETE' });
                                      if(localStorage.getItem('active_session_id') === groupName) localStorage.removeItem('active_session_id');
                                      fetchProfiles()
    fetchWords();
                                      fetchComparisons();
                                      fetchExplains();
                                    }}
                                    className="text-xs text-red-500 hover:text-red-600 transition-colors"
                                  >
                                    Delete Group
                                  </button>
                                )}
                              </div>
                            )}
                          <div className="grid gap-3">
                            {groupItems.map(c => (
                              <div key={c.id} className="border dark:border-gray-700 p-4 rounded-lg flex justify-between items-center bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow relative">
                                <div 
                                  className="flex-1 cursor-pointer" 
                                  onClick={() => {
                                    const id = Date.now().toString();
                                    setExplainTabs([...explainTabs, { id, title: c.text, loading: true, hasData: false, initialExplain: c }]);
                                    setActiveExplainTabId(id);
                                  }}
                                >
                                  <div 
                                    className="flex items-center gap-2 w-fit relative"
                                    onMouseEnter={() => handleHover(c.id, 'explain')}
                                    onMouseLeave={() => setHoveredPreviewId(null)}
                                  >
                                    <span className="font-bold text-lg">{c.text}</span>
                                    <span className="text-gray-500 dark:text-gray-400 text-sm">({c.search_count} searches)</span>
                                    {hoverReviewMode && hoveredPreviewId === c.id && (
                                      <HoverReviewPopup content={previewContent[c.id]} popupSize={popupSize} setPopupSize={setPopupSize} />
                                    )}
                                  </div>
                                </div>
                                <button onClick={() => deleteExplain(c.id)} className="text-red-500 p-2 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors"><Trash2 size={20} /></button>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <ExplainTab profileId={activeProfileId} tabId={t.id} fetchExplains={fetchExplains} settings={settings} defaultSettings={defaultSettings} models={models} initialExplain={t.initialExplain} onUpdateTab={(id, data) => setExplainTabs(prev => prev.map(pt => pt.id === id ? { ...pt, ...data } : pt))} />
                )}
              </div>
            ))}
          </div>
        </div>
      )
    }


    if (activeTab === 'flashcards') {
      return (
        <div className="p-6 max-w-4xl mx-auto h-full flex flex-col text-gray-900 dark:text-gray-100">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Flashcards & Export</h2>
            <button 
              onClick={() => {
                const csv = [
                  ['Term', 'Language', 'Lemma', 'Color', 'Searches'].join(','),
                  ...words.map(w => [w.term, w.language || '', w.lemma || '', w.color || '', w.search_count].map(s => `"${s}"`).join(','))
                ].join('\n')
                const blob = new Blob([csv], { type: 'text/csv' })
                const url = URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = 'ai_dict_export.csv'
                a.click()
              }}
              className="bg-green-600 hover:bg-green-700 transition-colors text-white px-4 py-2 rounded font-medium"
            >
              Export CSV
            </button>
          </div>
          
          <div className="flex-1 overflow-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pb-10">
            {words.map(w => (
              <div key={w.id} className="border dark:border-gray-700 p-4 rounded-xl shadow-sm bg-white dark:bg-gray-800 hover:shadow-md transition-shadow relative overflow-hidden">
                <div className="absolute top-0 left-0 w-1 h-full" style={{backgroundColor: COLORS.find(c => c.id === w.color)?.hex || 'transparent'}} />
                <div className="flex justify-between mb-2 pl-2">
                  <span className="text-sm text-gray-500 dark:text-gray-400">{w.language}</span>
                  <span className="text-xs text-gray-400">{new Date(w.updated_at).toLocaleDateString()}</span>
                </div>
                <h3 className="text-2xl font-bold mb-2 pl-2">{w.term}</h3>
                {w.lemma && <div className="text-gray-600 dark:text-gray-400 pl-2">Lemma: {w.lemma}</div>}
              </div>
            ))}
          </div>
        </div>
      )
    }



    if (activeTab === 'translation') {
      const filteredItems = translations.filter(c => 
        (c.text || '').toLowerCase().includes(translationHistorySearchTerm.toLowerCase())
      );
      const totalItems = filteredItems.length;
      const totalSearches = filteredItems.reduce((sum, c) => sum + (c.search_count || 0), 0);
      const setter = setTranslationTabs;
      const activeSetter = setActiveTranslationTabId;

      return (
        <div className="flex-1 flex flex-col h-full bg-gray-100 dark:bg-gray-950 overflow-hidden relative">
          {/* Tabs Header */}
          <div className="flex bg-gray-100 dark:bg-gray-950 overflow-x-auto border-b dark:border-gray-800 scrollbar-hide">
            {translationTabs.map(t => (
              <div 
                key={t.id}
                className={`shrink-0 flex items-center gap-2 px-4 py-2 border-r dark:border-gray-800 cursor-pointer ${t.id === activeTranslationTabId ? 'bg-white dark:bg-gray-800 font-medium text-blue-600 dark:text-blue-400' : 'hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400'}`}
                onClick={() => activeSetter(t.id)}
              >
                {t.id === 'history' ? <History size={14}/> : <Globe size={14}/>}
                <span className="truncate max-w-[150px]">{t.title || 'New Translation'}</span>
                {t.id !== 'history' && (
                  <>
                    {t.loading && <Loader2 size={12} className="animate-spin text-blue-500" />}
                    {!t.loading && t.hasData && <div className="w-2 h-2 rounded-full bg-green-500 shrink-0" title="Done" />}
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        setter(translationTabs.filter(tab => tab.id !== t.id));
                        if (activeTranslationTabId === t.id) activeSetter(translationTabs[0]?.id || 'history');
                      }}
                      className="ml-2 text-gray-400 hover:text-red-500 shrink-0"
                    >×</button>
                  </>
                )}
              </div>
            ))}
            <button 
              onClick={() => {
                const id = Date.now().toString()
                setter([...translationTabs, { id, title: 'New Translation', loading: false, hasData: false, initialTranslation: null }])
                activeSetter(id)
              }}
              className="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 font-bold shrink-0"
            >
              +
            </button>
          </div>

          {/* Tab Contents */}
          <div className="flex-1 overflow-hidden relative bg-gray-100 dark:bg-gray-950">
            {translationTabs.map(t => (
              <div key={t.id} className={t.id === activeTranslationTabId ? 'h-full block overflow-y-auto' : 'hidden'}>
                {t.id === 'history' ? (
                  <div className="h-full overflow-y-auto p-6 text-gray-900 dark:text-gray-100">
                    <div className="flex flex-col xl:flex-row xl:items-center justify-between mb-6 gap-4">
                      <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                        <h2 className="text-2xl font-bold">Translation History</h2>
                        <div className="relative w-full sm:w-64">
                          <input 
                            type="text" 
                            value={translationHistorySearchTerm}
                            onChange={e => setTranslationHistorySearchTerm(e.target.value)}
                            placeholder="Search translation history..."
                            className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded-lg py-1.5 pl-9 pr-3 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-sm"
                          />
                          <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                        </div>
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => setHoverReviewMode(!hoverReviewMode)}
                            className={`p-1.5 rounded-lg flex items-center gap-1.5 text-sm border shadow-sm transition-colors ${hoverReviewMode ? 'bg-blue-600 border-blue-600 text-white hover:bg-blue-700 dark:bg-blue-600 dark:border-blue-600 dark:text-white dark:hover:bg-blue-700' : 'bg-white border-gray-300 text-gray-600 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700'}`}
                            title="Toggle Quick Review on Hover"
                          >
                            <ScanLine size={16} /> 
                            <span className="hidden sm:inline font-medium">Hover Review</span>
                          </button>
                          <span className="text-sm font-medium text-gray-500 dark:text-gray-400 ml-2">Sort by:</span>
                          <select 
                            value={historySort} 
                            onChange={e => setHistorySort(e.target.value)} 
                            className="border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded-lg py-1.5 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-sm"
                          >
                            <option value="date">Date (Grouped)</option>
                            <option value="count">Most Searched</option>
                            <option value="alpha">Alphabetical</option>
                          </select>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-4 text-sm text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-800 px-4 py-2 rounded-lg border dark:border-gray-700 shadow-sm items-center justify-between w-full">
                        <div className="flex items-center gap-4">
                          <div className="flex items-center gap-1">
                            <span className="font-medium">Total Translations:</span> 
                            <span className="text-gray-900 dark:text-gray-100 font-bold">{totalItems}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <span className="font-medium">Total Searches:</span> 
                            <span className="text-gray-900 dark:text-gray-100 font-bold">{totalSearches}</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <button onClick={() => {
                            const sessionId = "Session " + new Date().toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
                            localStorage.setItem('active_session_id', sessionId);
                            alert("Started " + sessionId);
                          }} className="px-2 py-1 bg-blue-100 hover:bg-blue-200 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded text-xs font-medium transition-colors">New Session</button>
                          <button onClick={() => exportData('translations')} className="px-2 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded text-xs font-medium transition-colors text-gray-700 dark:text-gray-300">Export</button>
                          <label className="px-2 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded text-xs font-medium transition-colors text-gray-700 dark:text-gray-300 cursor-pointer">
                            Import
                            <input type="file" accept=".json" className="hidden" onChange={(e) => importData('translations', e)} />
                          </label>
                          <button onClick={() => clearData('translations')} className="px-2 py-1 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 text-red-600 dark:text-red-400 rounded text-xs font-medium transition-colors">Clear All</button>
                        </div>
                      </div>
                    </div>

                    <div className="grid gap-6">
                      {Object.entries(getGroupedByDay(filteredItems, 'text')).map(([groupName, groupItems]) => (
                        <div key={groupName}>
                          {historySort === 'date' && (
                              <div className="flex items-center justify-between mb-3 border-b dark:border-gray-800 pb-1">
                                <h3 className="text-lg font-bold text-gray-500 dark:text-gray-400">{groupName}</h3>
                                {(groupName !== 'All' && groupItems[0]?.session_id === groupName) && (
                                  <div className="flex gap-2">
                                    <button onClick={() => handleRenameSession(groupName)} className="text-xs text-blue-500 hover:text-blue-700 bg-blue-100 dark:bg-blue-900/30 dark:hover:bg-blue-900/50 px-2 py-1 rounded transition-colors" title="Rename Session">Rename</button>
                                    <button onClick={async () => {
                                      if (confirm(`Delete all data in ${groupName}?`)) {
                                        await fetch(`/api/sessions/${groupName}`, { method: 'DELETE' });
                                        if (localStorage.getItem('active_session_id') === groupName) {
                                          localStorage.removeItem('active_session_id');
                                        }
                                        fetchProfiles()
    fetchWords(); fetchComparisons(); fetchExplains(); fetchTranslations();
                                      }
                                    }} className="text-xs text-red-500 hover:text-red-700 bg-red-100 dark:bg-red-900/30 dark:hover:bg-red-900/50 px-2 py-1 rounded transition-colors" title="Delete Session">Delete Session</button>
                                  </div>
                                )}
                              </div>
                          )}
                          <div className="grid gap-3">
                            {groupItems.map(c => (
                              <div key={c.id} className="border dark:border-gray-700 p-4 rounded-lg flex justify-between items-center bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow relative">
                                <div 
                                  className="flex-1 cursor-pointer"
                                  onClick={() => {
                                    const newId = Date.now().toString()
                                    setTranslationTabs([...translationTabs, { id: newId, title: c.text, loading: true, hasData: false, initialTranslation: c }])
                                    setActiveTranslationTabId(newId)
                                  }}
                                >
                                  <div 
                                    className="flex items-center gap-2 w-fit relative"
                                    onMouseEnter={() => handleHover(c.id, 'translation')}
                                    onMouseLeave={() => setHoveredPreviewId(null)}
                                  >
                                    <span className="font-bold text-lg">{c.text}</span>
                                    <span className="text-gray-500 dark:text-gray-400 text-sm">({c.search_count} searches)</span>
                                    {hoverReviewMode && hoveredPreviewId === c.id && (
                                      <HoverReviewPopup content={previewContent[c.id]} popupSize={popupSize} setPopupSize={setPopupSize} />
                                    )}
                                  </div>
                                </div>
                                <button onClick={() => deleteTranslation(c.id)} className="text-red-500 p-2 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors"><Trash2 size={20} /></button>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <TranslationTab profileId={activeProfileId} tabId={t.id} fetchTranslations={fetchTranslations} settings={settings} defaultSettings={defaultSettings} models={models} initialTranslation={t.initialTranslation} onUpdateTab={(id, data) => setTranslationTabs(prev => prev.map(pt => pt.id === id ? { ...pt, ...data } : pt))} translationSourceLang={translationSourceLang} setTranslationSourceLang={setTranslationSourceLang} translationTargetLang={translationTargetLang} setTranslationTargetLang={setTranslationTargetLang} translationLangs={translationLangs} setTranslationLangs={setTranslationLangs} />
                )}
              </div>
            ))}
          </div>
        </div>
      )
    }

  }

  return (
    <div className={`flex h-screen font-sans ${theme !== 'light' ? 'bg-gray-950' : 'bg-gray-100'}`}>
      {models && models.length > 0 && (
        <datalist id="all-models-list">
          {models.map(m => <option key={m.id} value={m.id} />)}
        </datalist>
      )}
      {/* Sidebar */}
      <div className={`bg-white dark:bg-gray-900 border-r dark:border-gray-800 flex flex-col z-10 shadow-sm transition-all duration-300 ${sidebarCollapsed ? "w-16" : "w-16 md:w-64"}`}>
        <div className={`h-16 flex items-center justify-between border-b dark:border-gray-800 ${sidebarCollapsed ? "px-2 justify-center" : "md:px-6 px-2"}`}>
          <button 
            onClick={handleHomeClick}
            className={`font-bold text-xl text-blue-600 dark:text-blue-500 tracking-tight flex items-center justify-center md:justify-start gap-2 hover:opacity-80 transition-opacity ${sidebarCollapsed ? "hidden" : "flex-1 hidden md:flex"}`}
            title="Home / New Search"
          >
            <Library size={24} />
            <span className="hidden md:inline">AI Dict</span>
          </button>
          
          <button 
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400 transition-colors hidden md:flex mx-auto"
            title="Toggle Sidebar"
          >
            <Menu size={20} />
          </button>
        </div>
        <nav className="flex-1 p-2 md:p-4 space-y-2 overflow-y-auto">
          <NavItem collapsed={sidebarCollapsed} icon={<Search />} label="Search" active={activeTab === 'search'} onClick={handleSearchClick} />
          <NavItem collapsed={sidebarCollapsed} icon={<GitCompare />} label="Compare" active={activeTab === 'compare'} onClick={handleCompareClick} />
          <NavItem collapsed={sidebarCollapsed} icon={<MessageSquare />} label="Explain" active={activeTab === 'explain'} onClick={handleExplainClick} />
          <NavItem collapsed={sidebarCollapsed} icon={<Globe />} label="Translation" active={activeTab === 'translation'} onClick={() => {
            const id = Date.now().toString()
            setTranslationTabs([...translationTabs, { id, title: 'New Translation', loading: false, hasData: false, initialTranslation: null }])
            setActiveTranslationTabId(id)
            setActiveTab('translation')
          }} />
        </nav>

        <div className="p-2 md:p-4 border-t dark:border-gray-800 space-y-2">
          {!sidebarCollapsed && (
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider block">Profile</label>
                <div className="flex items-center gap-1">
                  <button onClick={() => {
                    const idx = profiles.findIndex(p => p.id === activeProfileId);
                    if (idx > 0) {
                      const newProfiles = [...profiles];
                      [newProfiles[idx - 1], newProfiles[idx]] = [newProfiles[idx], newProfiles[idx - 1]];
                      setProfiles(newProfiles);
                      fetch('/api/profiles/reorder', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({profile_ids: newProfiles.map(p => p.id)})});
                    }
                  }} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200" title="Move Up"><ChevronUp size={14}/></button>
                  <button onClick={() => {
                    const idx = profiles.findIndex(p => p.id === activeProfileId);
                    if (idx < profiles.length - 1 && idx !== -1) {
                      const newProfiles = [...profiles];
                      [newProfiles[idx + 1], newProfiles[idx]] = [newProfiles[idx], newProfiles[idx + 1]];
                      setProfiles(newProfiles);
                      fetch('/api/profiles/reorder', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({profile_ids: newProfiles.map(p => p.id)})});
                    }
                  }} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200" title="Move Down"><ChevronDown size={14}/></button>
                </div>
              </div>
              <select 
                value={activeProfileId} 
                onChange={(e) => {
                  if (e.target.value === 'new') {
                    const name = prompt('Enter new profile name:')
                    if (name) {
                      fetch('/api/profiles', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name })
                      }).then(r => r.json()).then(p => {
                        fetchProfiles()
                        setActiveProfileId(p.id)
                      })
                    }
                  } else if (e.target.value === 'rename') {
                    const currentProfile = profiles.find(p => p.id === activeProfileId);
                    const name = prompt('Enter new name for profile:', currentProfile?.name);
                    if (name && name !== currentProfile?.name) {
                      fetch(`/api/profiles/${activeProfileId}/rename`, {
                        method: 'PATCH',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name })
                      }).then(() => fetchProfiles());
                    }
                  } else if (e.target.value === 'set_default') {
                    fetch(`/api/profiles/${activeProfileId}/set_default`, { method: 'PATCH' })
                      .then(() => fetchProfiles());
                  } else if (e.target.value === 'delete') {
                    const currentProfile = profiles.find(p => p.id === activeProfileId);
                    if (currentProfile?.is_default) {
                      alert("Cannot delete the default profile")
                    } else if (confirm('Are you sure you want to delete this profile and ALL its history?')) {
                      fetch(`/api/profiles/${activeProfileId}`, { method: 'DELETE' }).then(() => {
                        fetchProfiles()
                        setActiveProfileId(1)
                      })
                    }
                  } else {
                    setActiveProfileId(parseInt(e.target.value))
                  }
                }}
                className="w-full bg-gray-100 dark:bg-gray-800 border-none rounded p-2 text-sm text-gray-800 dark:text-gray-200 focus:ring-0 cursor-pointer"
              >
                {profiles.map(p => (
                  <option key={p.id} value={p.id}>{p.name} {p.is_default ? '(Default)' : ''}</option>
                ))}
                <option disabled>──────────</option>
                <option value="new">+ Create Profile</option>
                <option value="rename">~ Rename Current</option>
                <option value="set_default">☆ Set as Default</option>
                <option value="delete" className="text-red-500">- Delete Current</option>
              </select>
            </div>
          )}

          <NavItem collapsed={sidebarCollapsed} icon={<SettingsIcon />} label="Settings" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
        </div>
      </div>

      {/* Main Area */}
      <div className="flex-1 overflow-hidden bg-gray-100 dark:bg-gray-950">
        {renderContent()}
      </div>
    </div>
  )
}

function NavItem({ icon, label, active, onClick, collapsed }) {
  return (
    <button 
      onClick={onClick}
      className={`w-full flex items-center gap-3 p-3 rounded-lg transition-colors ${collapsed ? "justify-center" : "justify-center md:justify-start"} ${active ? "bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 font-medium" : "hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400"}`}
      title={collapsed ? label : undefined}
    >
      <div className="shrink-0">{icon}</div>
      <span className={collapsed ? "hidden" : "hidden md:inline overflow-hidden text-ellipsis whitespace-nowrap"}>{label}</span>
    </button>
  )
}

export default App
