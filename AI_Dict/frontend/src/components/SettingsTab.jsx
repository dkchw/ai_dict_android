import React from 'react'
import { Palette, Edit, Trash2, ExternalLink } from 'lucide-react'

export default function SettingsTab({
  settings, setSettings, fetchSettings, defaultSettings,
  models, theme, setTheme,
  templates, setTemplates, editingTemplate, setEditingTemplate,
  exportData, importData, clearData
}) {
  return (
    <div className="h-full overflow-y-auto">
          <div className="p-6 max-w-2xl mx-auto text-gray-900 dark:text-gray-100">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Settings</h2>
              <div className="flex gap-2">
                <button
                  onClick={async () => {
                    const res = await fetch('/api/settings/export')
                    const data = await res.json()
                    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
                    const url = URL.createObjectURL(blob)
                    const a = document.createElement('a')
                    a.href = url
                    const dateStr = new Date().toISOString().replace(/[:T]/g, '-').split('.')[0]; a.download = `ai_dict_settings_${dateStr}.json`
                    a.click()
                  }}
                  className="bg-green-600 hover:bg-green-700 transition-colors text-white px-3 py-1.5 rounded text-sm font-medium"
                >
                  Export
                </button>
                <label className="bg-purple-600 hover:bg-purple-700 transition-colors text-white px-3 py-1.5 rounded text-sm font-medium cursor-pointer">
                  Import
                  <input
                    type="file"
                    accept=".json"
                    className="hidden"
                    onChange={async (e) => {
                      const file = e.target.files[0]
                      if (!file) return
                      const reader = new FileReader()
                      reader.onload = async (e) => {
                        try {
                          const data = JSON.parse(e.target.result)
                          await fetch('/api/settings/import', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(data)
                          })
                          alert('Settings imported successfully')
                          fetchSettings()
                        } catch (err) {
                          alert('Invalid settings file')
                        }
                      }
                      reader.readAsText(file)
                    }}
                  />
                </label>
              </div>
            </div>
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">App Theme</label>
              <div className="flex items-center gap-2">
                <Palette size={20} className="text-gray-500" />
                <select 
                  value={theme}
                  onChange={e => setTheme(e.target.value)}
                  className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="tokyonight">Tokyo Night (Default)</option>
                  <option value="nord">Nord</option>
                  <option value="dracula">Dracula</option>
                </select>
              </div>
            </div>
            <h3 className="text-xl font-bold mt-8 mb-4 border-b dark:border-gray-800 pb-2">Default Languages</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Default Search Source Language</label>
                <input 
                  type="text" 
                  value={settings.SEARCH_SOURCE_LANG || ''}
                  onChange={e => setSettings({...settings, SEARCH_SOURCE_LANG: e.target.value})}
                  className="w-full border dark:border-gray-600 dark:bg-gray-800 rounded p-2"
                  placeholder="e.g. Auto Detect"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Default Search Target Language</label>
                <input 
                  type="text" 
                  value={settings.SEARCH_TARGET_LANG || ''}
                  onChange={e => setSettings({...settings, SEARCH_TARGET_LANG: e.target.value})}
                  className="w-full border dark:border-gray-600 dark:bg-gray-800 rounded p-2"
                  placeholder="e.g. English"
                />
              </div>
            </div>
            
            <h3 className="text-xl font-bold mt-8 mb-4 border-b dark:border-gray-800 pb-2">API Configuration</h3>
            <div>
              <label className="block text-sm font-medium mb-2">OpenRouter API Key</label>
              <input 
                type="password" 
                value={settings.OPENROUTER_API_KEY || ''}
                onChange={e => setSettings({...settings, OPENROUTER_API_KEY: e.target.value})}
                className="w-full border dark:border-gray-600 dark:bg-gray-800 rounded p-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Main Model (For initial explanation)</label>
              <input 
                type="text" 
                list="main-models-list"
                value={settings.MAIN_MODEL || ''}
                onChange={e => setSettings({...settings, MAIN_MODEL: e.target.value})}
                placeholder="inclusionai/ling-3.0-flash"
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {models.length > 0 && (
                <datalist id="main-models-list">
                  <option value="inclusionai/ling-3.0-flash" />
                  {models.map(m => <option key={m.id} value={m.id} />)}
                </datalist>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Chat Model (For follow up)</label>
              <input 
                type="text" 
                list="chat-models-list"
                value={settings.CHAT_MODEL || ''}
                onChange={e => setSettings({...settings, CHAT_MODEL: e.target.value})}
                placeholder="~deepseek/deepseek-v4-flash-latest"
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {models.length > 0 && (
                <datalist id="chat-models-list">
                  <option value="~deepseek/deepseek-v4-flash-latest" />
                  {models.map(m => <option key={m.id} value={m.id} />)}
                </datalist>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Compare Model (For comparison)</label>
              <input 
                type="text" 
                list="compare-models-list"
                value={settings.COMPARE_MODEL || ''}
                onChange={e => setSettings({...settings, COMPARE_MODEL: e.target.value})}
                placeholder="~deepseek/deepseek-v4-flash-latest"
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {models.length > 0 && (
                <datalist id="compare-models-list">
                  <option value="~deepseek/deepseek-v4-flash-latest" />
                  {models.map(m => <option key={m.id} value={m.id} />)}
                </datalist>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Translation Model</label>
              <input 
                type="text" 
                list="translation_model-list"
                value={settings.TRANSLATION_MODEL || ''}
                onChange={e => setSettings({...settings, TRANSLATION_MODEL: e.target.value})}
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {models.length > 0 && (
                <datalist id="translation_model-list">
                  {models.map(m => <option key={m.id} value={m.id} />)}
                </datalist>
              )}
            </div>


            <div>
              <label className="block text-sm font-medium mb-2">Main Reasoning Effort</label>
              <select 
                value={settings.MAIN_REASONING || 'default'} 
                onChange={e => setSettings({...settings, MAIN_REASONING: e.target.value})}
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="default">Default</option>
                <option value="max">Max</option>
                <option value="xhigh">X-High</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
                <option value="minimal">Minimal</option>
                <option value="none">None</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Chat Reasoning Effort</label>
              <select 
                value={settings.CHAT_REASONING || 'default'} 
                onChange={e => setSettings({...settings, CHAT_REASONING: e.target.value})}
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="default">Default</option>
                <option value="max">Max</option>
                <option value="xhigh">X-High</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
                <option value="minimal">Minimal</option>
                <option value="none">None</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Compare Reasoning Effort</label>
              <select 
                value={settings.COMPARE_REASONING || 'default'} 
                onChange={e => setSettings({...settings, COMPARE_REASONING: e.target.value})}
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="default">Default</option>
                <option value="max">Max</option>
                <option value="xhigh">X-High</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
                <option value="minimal">Minimal</option>
                <option value="none">None</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Translation Reasoning Effort</label>
              <select 
                value={settings.TRANSLATION_REASONING || 'default'} 
                onChange={e => setSettings({...settings, TRANSLATION_REASONING: e.target.value})}
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="default">Default</option>
                <option value="max">Max</option>
                <option value="xhigh">X-High</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
                <option value="minimal">Minimal</option>
                <option value="none">None</option>
              </select>
            </div>


            <div>
              <label className="block text-sm font-medium mb-2">Fallback Models (Comma separated)</label>
              <input 
                type="text" 
                value={settings.FALLBACK_MODELS || ''}
                placeholder="model1/a, model2/b"
                onChange={e => setSettings({...settings, FALLBACK_MODELS: e.target.value})}
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium">Dictionary Prompt</label>
                <button 
                  onClick={(e) => {
                    e.preventDefault();
                    setSettings({...settings, DICT_PROMPT: ''});
                  }}
                  className="text-[10px] bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 px-2 py-1 rounded transition-colors"
                >
                  Restore Default
                </button>
              </div>
              <textarea 
                value={settings.DICT_PROMPT || (defaultSettings ? defaultSettings.DICT_PROMPT : '') || ''}
                onChange={e => setSettings({...settings, DICT_PROMPT: e.target.value})}
                placeholder="Leave blank to use default..."
                rows="4"
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
              />
            </div>
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium">Comparison Prompt</label>
                <button 
                  onClick={(e) => {
                    e.preventDefault();
                    setSettings({...settings, COMPARE_PROMPT: ''});
                  }}
                  className="text-[10px] bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 px-2 py-1 rounded transition-colors"
                >
                  Restore Default
                </button>
              </div>
              <textarea 
                value={settings.COMPARE_PROMPT || (defaultSettings ? defaultSettings.COMPARE_PROMPT : '') || ''}
                onChange={e => setSettings({...settings, COMPARE_PROMPT: e.target.value})}
                placeholder="Leave blank to use default..."
                rows="4"
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
              />
            </div>
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium">Explain Prompt</label>
                <button 
                  onClick={(e) => {
                    e.preventDefault();
                    setSettings({...settings, EXPLAIN_PROMPT: ''});
                  }}
                  className="text-[10px] bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 px-2 py-1 rounded transition-colors"
                >
                  Restore Default
                </button>
              </div>
              <textarea 
                value={settings.EXPLAIN_PROMPT || (defaultSettings ? defaultSettings.EXPLAIN_PROMPT : '') || ''}
                onChange={e => setSettings({...settings, EXPLAIN_PROMPT: e.target.value})}
                placeholder="Leave blank to use default..."
                rows="4"
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
              />
            </div>
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium">Translate Prompt</label>
                <button 
                  onClick={(e) => {
                    e.preventDefault();
                    setSettings({...settings, TRANSLATE_PROMPT: ''});
                  }}
                  className="text-[10px] bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 px-2 py-1 rounded transition-colors"
                >
                  Restore Default
                </button>
              </div>
              <textarea 
                value={settings.TRANSLATE_PROMPT || (defaultSettings ? defaultSettings.TRANSLATE_PROMPT : '') || ''}
                onChange={e => setSettings({...settings, TRANSLATE_PROMPT: e.target.value})}
                placeholder="Leave blank to use default..."
                rows="4"
                className="w-full border dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
              />
            </div>


            <button 
              onClick={async () => {
                const keys = ['SEARCH_SOURCE_LANG', 'SEARCH_TARGET_LANG', 'OPENROUTER_API_KEY', 'MAIN_MODEL', 'CHAT_MODEL', 'COMPARE_MODEL', 'FALLBACK_MODELS', 'TRANSLATION_MODEL', 'MAIN_REASONING', 'CHAT_REASONING', 'COMPARE_REASONING', 'TRANSLATION_REASONING', 'DICT_PROMPT', 'COMPARE_PROMPT', 'EXPLAIN_PROMPT', 'TRANSLATE_PROMPT'];
                for (let key of keys) {
                  await fetch('/api/settings', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ key, value: settings[key] || '' })
                  })
                }
                alert('Saved')
              }}
              className="mt-4 bg-blue-600 hover:bg-blue-700 transition-colors text-white px-4 py-2 rounded font-medium"
            >Save Settings</button>

                        <hr className="my-8 dark:border-gray-700" />
            
            <div>
              <h3 className="text-xl font-bold mb-4">Data Management (All History)</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                Export, import, or clear all of your history collectively. The "Database ZIP" option perfectly saves everything (profiles, settings, history) for easy transfer to a new computer!
              </p>
              <div className="flex flex-wrap gap-2 mb-2">
                <a
                  href="/api/data/export_zip"
                  
                  className="bg-blue-600 hover:bg-blue-700 transition-colors text-white px-3 py-1.5 rounded text-sm font-medium inline-block"
                >
                  Export Database (ZIP)
                </a>
                <label className="bg-indigo-600 hover:bg-indigo-700 transition-colors text-white px-3 py-1.5 rounded text-sm font-medium cursor-pointer">
                  Import Database (ZIP)
                  <input
                    type="file"
                    accept=".zip"
                    className="hidden"
                    onChange={async (e) => {
                      const file = e.target.files[0]
                      if (!file) return
                      const formData = new FormData()
                      formData.append('file', file)
                      try {
                        const res = await fetch('/api/data/import_zip', {
                          method: 'POST',
                          body: formData
                        })
                        if (res.ok) {
                          alert("Database imported successfully! Please refresh the page.")
                          window.location.reload()
                        } else {
                          const err = await res.json()
                          alert("Failed: " + err.detail)
                        }
                      } catch (e) {
                        alert("Error importing database")
                      }
                    }}
                  />
                </label>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => exportData('all')}
                  className="bg-green-600 hover:bg-green-700 transition-colors text-white px-3 py-1.5 rounded text-sm font-medium"
                >
                  Export (JSON Only)
                </button>
                <label className="bg-purple-600 hover:bg-purple-700 transition-colors text-white px-3 py-1.5 rounded text-sm font-medium cursor-pointer">
                  Import (JSON Only)
                  <input
                    type="file"
                    accept=".json"
                    className="hidden"
                    onChange={(e) => importData('all', e)}
                  />
                </label>
                <button
                  onClick={() => clearData('all')}
                  className="bg-red-600 hover:bg-red-700 transition-colors text-white px-3 py-1.5 rounded text-sm font-medium"
                >
                  Clear All Data
                </button>
              </div>
            </div>

            <hr className="my-8 dark:border-gray-700" />
            
            <div>
              <h3 className="text-xl font-bold mb-4">External Links</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                Add buttons that appear based on the word's detected language. Use <code className="bg-gray-200 dark:bg-gray-700 px-1 rounded">{`{{str}}`}</code> as a placeholder for the searched word. Use "All" to show for all languages.
              </p>
              
              <div className="space-y-4 mb-6">
                {templates.map(t => (
                  <div key={t.id} className="flex gap-2 items-center bg-gray-50 dark:bg-gray-800 p-3 rounded-lg border dark:border-gray-700">
                    <div className="flex-1 overflow-hidden">
                      <div className="flex items-center gap-2 font-medium">
                        {t.icon_url ? <img src={t.icon_url} className="w-4 h-4" alt=""/> : <ExternalLink size={14} />}
                        {t.name || 'Dict'} <span className="text-sm font-normal text-gray-500">({t.language})</span>
                      </div>
                      <div className="text-sm text-gray-500 truncate">{t.url_template}</div>
                    </div>
                    <div className="flex gap-1">
                      <button 
                        onClick={() => setEditingTemplate(t)}
                        className="text-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/30 p-2 rounded"
                      ><Edit size={20}/></button>
                      <button 
                        onClick={async () => {
                          await fetch(`/api/templates/${t.id}`, { method: 'DELETE' })
                          if (editingTemplate?.id === t.id) setEditingTemplate(null)
                          fetchSettings()
                        }}
                        className="text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30 p-2 rounded"
                      ><Trash2 size={20}/></button>
                    </div>
                  </div>
                ))}
              </div>

              <form 
                id="template-form"
                onSubmit={async (e) => {
                  e.preventDefault()
                  const fd = new FormData(e.target)
                  const body = {
                    name: fd.get('name') || 'Dict',
                    language: fd.get('language'),
                    url_template: fd.get('url_template'),
                    icon_url: fd.get('icon_url')
                  }
                  if (editingTemplate) {
                    await fetch(`/api/templates/${editingTemplate.id}`, {
                      method: 'PUT',
                      headers: {'Content-Type': 'application/json'},
                      body: JSON.stringify(body)
                    })
                    setEditingTemplate(null)
                  } else {
                    await fetch('/api/templates', {
                      method: 'POST',
                      headers: {'Content-Type': 'application/json'},
                      body: JSON.stringify(body)
                    })
                  }
                  e.target.reset()
                  fetchSettings()
                }}
                className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border dark:border-gray-700 space-y-4"
              >
                <div className="flex items-center justify-between">
                  <h4 className="font-bold">{editingTemplate ? 'Edit Template' : 'Add New Template'}</h4>
                  {editingTemplate && (
                    <button type="button" onClick={() => { setEditingTemplate(null); document.getElementById('template-form').reset(); }} className="text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">Cancel</button>
                  )}
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Name</label>
                    <input name="name" required placeholder="e.g. Leo Dict" defaultValue={editingTemplate?.name || 'Dict'} key={`name-${editingTemplate?.id || 'new'}`} className="w-full border dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 rounded p-2" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Language</label>
                    <input name="language" required placeholder="e.g. German, All" defaultValue={editingTemplate?.language || ''} key={`lang-${editingTemplate?.id || 'new'}`} className="w-full border dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 rounded p-2" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Icon URL (optional)</label>
                    <input name="icon_url" placeholder="https://..." defaultValue={editingTemplate?.icon_url || ''} key={`icon-${editingTemplate?.id || 'new'}`} className="w-full border dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 rounded p-2" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">URL Template</label>
                  <input name="url_template" required placeholder="https://dict.leo.org/german-english/{{str}}" defaultValue={editingTemplate?.url_template || ''} key={`url-${editingTemplate?.id || 'new'}`} className="w-full border dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 rounded p-2" />
                </div>
                <button type="submit" className="bg-gray-800 dark:bg-gray-700 hover:bg-gray-900 dark:hover:bg-gray-600 text-white px-4 py-2 rounded font-medium">{editingTemplate ? 'Update Template' : 'Add Template'}</button>
              </form>
            </div>
          </div>
        </div>
    </div>
  )
}
