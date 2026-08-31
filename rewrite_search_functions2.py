import sys

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

def replace_function(text, func_name, new_func_code):
    import re
    # Find start of function
    match = re.search(r'^\s*fun ' + func_name + r'\(.*?\)\s*\{', text, re.MULTILINE)
    if not match:
        return text
    start_idx = match.start()
    
    # Find end of function using brace counting
    brace_count = 0
    in_function = False
    end_idx = start_idx
    for i in range(start_idx, len(text)):
        if text[i] == '{':
            brace_count += 1
            in_function = True
        elif text[i] == '}':
            brace_count -= 1
        
        if in_function and brace_count == 0:
            end_idx = i + 1
            break
            
    return text[:start_idx] + new_func_code + text[end_idx:]

search_word_code = """    fun searchWord(term: String, sourceLang: String, targetLang: String, profileId: Int) {
        val _uiState = _dictState
        viewModelScope.launch {
            try {
                val activeSessionId = database.appDao().getSetting("ACTIVE_SESSION_ID")?.value
                val sessionId = if (!activeSessionId.isNullOrBlank()) activeSessionId else java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = term, sessionId = sessionId, mode = "dict")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val savedWord = initialWord.copy(id = wordId)
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                val savedMsg = initialMsg.copy(id = msgId)
                
                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "")
                
                var currentText = ""
                llmRepository.streamExplanation(term, sourceLang, targetLang).collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMarkdown = currentText
                val (language, lemma) = MarkdownParser.extractMetadata(finalMarkdown)
                
                val finalWord = savedWord.copy(language = language, lemma = lemma)
                database.appDao().insertWord(finalWord)
                val finalMsg = savedMsg.copy(content = finalMarkdown)
                database.appDao().insertChatMessage(finalMsg)
                
                if (_uiState.value.word?.id == wordId) {
                    _uiState.value = SearchState(isLoading = false, word = finalWord, chatMessages = listOf(finalMsg), currentStream = "")
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.term == term) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }"""

stream_translation_code = """    fun streamTranslation(text: String, source: String, target: String, profileId: Int) {
        val _uiState = _translateState
        viewModelScope.launch {
            try {
                val activeSessionId = database.appDao().getSetting("ACTIVE_SESSION_ID")?.value
                val sessionId = if (!activeSessionId.isNullOrBlank()) activeSessionId else java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = text, language = "$source -> $target", sessionId = sessionId, mode = "translate")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val savedWord = initialWord.copy(id = wordId)
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                val savedMsg = initialMsg.copy(id = msgId)

                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "")

                var currentText = ""
                llmRepository.streamTranslation(text, source, target).collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMsg = savedMsg.copy(content = currentText)
                database.appDao().insertChatMessage(finalMsg)
                if (_uiState.value.word?.id == wordId) {
                    _uiState.value = SearchState(isLoading = false, word = savedWord, chatMessages = listOf(finalMsg), currentStream = "")
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.term == text) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }"""

stream_explain_code = """    fun streamExplain(text: String, sourceLang: String, targetLang: String, profileId: Int) {
        val _uiState = _explainState
        viewModelScope.launch {
            try {
                val activeSessionId = database.appDao().getSetting("ACTIVE_SESSION_ID")?.value
                val sessionId = if (!activeSessionId.isNullOrBlank()) activeSessionId else java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = text, language = "$sourceLang -> $targetLang", sessionId = sessionId, mode = "explain")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val savedWord = initialWord.copy(id = wordId)
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                val savedMsg = initialMsg.copy(id = msgId)

                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "")

                var currentText = ""
                llmRepository.streamExplain(text, sourceLang, targetLang).collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMsg = savedMsg.copy(content = currentText)
                database.appDao().insertChatMessage(finalMsg)
                if (_uiState.value.word?.id == wordId) {
                    _uiState.value = SearchState(isLoading = false, word = savedWord, chatMessages = listOf(finalMsg), currentStream = "")
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.term == text) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }"""

stream_compare_code = """    fun streamCompare(words: String, sourceLang: String, targetLang: String, profileId: Int) {
        val _uiState = _compareState
        viewModelScope.launch {
            try {
                val activeSessionId = database.appDao().getSetting("ACTIVE_SESSION_ID")?.value
                val sessionId = if (!activeSessionId.isNullOrBlank()) activeSessionId else java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = words, language = "$sourceLang -> $targetLang", sessionId = sessionId, mode = "compare")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val savedWord = initialWord.copy(id = wordId)
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                val savedMsg = initialMsg.copy(id = msgId)

                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "")

                var currentText = ""
                llmRepository.streamCompare(words, sourceLang, targetLang).collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMsg = savedMsg.copy(content = currentText)
                database.appDao().insertChatMessage(finalMsg)
                if (_uiState.value.word?.id == wordId) {
                    _uiState.value = SearchState(isLoading = false, word = savedWord, chatMessages = listOf(finalMsg), currentStream = "")
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.term == words) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }"""

clear_search_code = """    fun clearCurrentSearch() {
        _dictState.value = SearchState()
        _compareState.value = SearchState()
        _translateState.value = SearchState()
        _explainState.value = SearchState()
        
        searchInput = ""
        translateInput = ""
        compareInput = ""
        explainInput = ""
    }"""

text = replace_function(text, 'searchWord', search_word_code)
text = replace_function(text, 'streamTranslation', stream_translation_code)
text = replace_function(text, 'streamExplain', stream_explain_code)
text = replace_function(text, 'streamCompare', stream_compare_code)
text = replace_function(text, 'clearCurrentSearch', clear_search_code)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

