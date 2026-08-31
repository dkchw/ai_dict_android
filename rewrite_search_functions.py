import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# 1. Rewrite searchWord
search_word_pattern = r'    fun searchWord\(term: String, sourceLang: String, targetLang: String, profileId: Int\) \{[\s\S]*?    \}'
new_search_word = """    fun searchWord(term: String, sourceLang: String, targetLang: String, profileId: Int) {
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
text = re.sub(search_word_pattern, new_search_word, text, flags=re.MULTILINE)

# 2. Rewrite streamTranslation
stream_translation_pattern = r'    fun streamTranslation\(text: String, source: String, target: String, profileId: Int\) \{[\s\S]*?    \}'
new_stream_translation = """    fun streamTranslation(text: String, source: String, target: String, profileId: Int) {
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
text = re.sub(stream_translation_pattern, new_stream_translation, text, flags=re.MULTILINE)

# 3. Rewrite streamExplain
stream_explain_pattern = r'    fun streamExplain\(text: String, sourceLang: String, targetLang: String, profileId: Int\) \{[\s\S]*?    \}'
new_stream_explain = """    fun streamExplain(text: String, sourceLang: String, targetLang: String, profileId: Int) {
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
text = re.sub(stream_explain_pattern, new_stream_explain, text, flags=re.MULTILINE)

# 4. Rewrite streamCompare
stream_compare_pattern = r'    fun streamCompare\(words: String, sourceLang: String, targetLang: String, profileId: Int\) \{[\s\S]*?    \}'
new_stream_compare = """    fun streamCompare(words: String, sourceLang: String, targetLang: String, profileId: Int) {
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
text = re.sub(stream_compare_pattern, new_stream_compare, text, flags=re.MULTILINE)


with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

