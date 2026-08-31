import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Refactor searchWord (Dict Mode)
old_dict = """                llmRepository.streamExplanation(term, sourceLang, targetLang).collect { currentText ->
                    _uiState.value = _uiState.value.copy(currentStream = currentText)
                }

                val finalMarkdown = _uiState.value.currentStream
                val (language, lemma) = MarkdownParser.extractMetadata(finalMarkdown)
                
                // Save Word
                val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
                val sessionId = sdf.format(Date())
                val word = Word(profileId = profileId, term = term, language = language, lemma = lemma, sessionId = sessionId, mode = "dict")
                val wordId = database.appDao().insertWord(word).toInt()
                val savedWord = word.copy(id = wordId)

                // Save Assistant Message
                val msg = ChatMessage(wordId = wordId, role = "assistant", content = finalMarkdown)
                val msgId = database.appDao().insertChatMessage(msg).toInt()
                val savedMsg = msg.copy(id = msgId)
                
                _uiState.value = SearchState(
                    isLoading = false,
                    word = savedWord,
                    chatMessages = listOf(savedMsg),
                    currentStream = ""
                )"""

new_dict = """                // Save Word early
                val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault())
                val activeSessionId = database.appDao().getSetting("ACTIVE_SESSION_ID")?.value
                val sessionId = if (!activeSessionId.isNullOrBlank()) activeSessionId else sdf.format(java.util.Date())
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = term, sessionId = sessionId, mode = "dict")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                
                llmRepository.streamExplanation(term, sourceLang, targetLang).collect { currentText ->
                    _uiState.value = _uiState.value.copy(currentStream = currentText)
                }

                val finalMarkdown = _uiState.value.currentStream
                val (language, lemma) = MarkdownParser.extractMetadata(finalMarkdown)
                
                // Update Word and Message
                val savedWord = initialWord.copy(id = wordId, language = language, lemma = lemma)
                database.appDao().insertWord(savedWord)
                val savedMsg = initialMsg.copy(id = msgId, content = finalMarkdown)
                database.appDao().insertChatMessage(savedMsg)
                
                _uiState.value = SearchState(
                    isLoading = false,
                    word = savedWord,
                    chatMessages = listOf(savedMsg),
                    currentStream = ""
                )"""

text = text.replace(old_dict, new_dict)

# Refactor streamTranslation
old_trans = """                llmRepository.streamTranslation(text, source, target).collect {
                    _uiState.value = _uiState.value.copy(currentStream = it)
                }
                val wordId = database.appDao().insertWord(com.aidict.app.data.entities.Word(profileId = profileId, term = text, language = "$source -> $target", sessionId = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date()), mode = "translate")).toInt()
                val msgId = database.appDao().insertChatMessage(com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = _uiState.value.currentStream)).toInt()
                _uiState.value = SearchState(isLoading = false, word = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = text, language = "$source -> $target", mode = "translate", sessionId = ""), chatMessages = listOf(com.aidict.app.data.entities.ChatMessage(id = msgId, wordId = wordId, role = "assistant", content = _uiState.value.currentStream)), currentStream = "")"""

new_trans = """                val activeSessionId = database.appDao().getSetting("ACTIVE_SESSION_ID")?.value
                val sessionId = if (!activeSessionId.isNullOrBlank()) activeSessionId else java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = text, language = "$source -> $target", sessionId = sessionId, mode = "translate")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()

                llmRepository.streamTranslation(text, source, target).collect {
                    _uiState.value = _uiState.value.copy(currentStream = it)
                }

                val savedMsg = initialMsg.copy(id = msgId, content = _uiState.value.currentStream)
                database.appDao().insertChatMessage(savedMsg)
                _uiState.value = SearchState(isLoading = false, word = initialWord.copy(id = wordId), chatMessages = listOf(savedMsg), currentStream = "")"""

text = text.replace(old_trans, new_trans)

# Refactor streamExplain
old_explain = """                llmRepository.streamExplain(text, sourceLang, targetLang).collect {
                    _uiState.value = _uiState.value.copy(currentStream = it)
                }
                val wordId = database.appDao().insertWord(com.aidict.app.data.entities.Word(profileId = profileId, term = text, sessionId = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date()), mode = "explain")).toInt()
                val msgId = database.appDao().insertChatMessage(com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = _uiState.value.currentStream)).toInt()
                _uiState.value = SearchState(isLoading = false, word = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = text, language = "$sourceLang -> $targetLang", mode = "explain", sessionId = ""), chatMessages = listOf(com.aidict.app.data.entities.ChatMessage(id = msgId, wordId = wordId, role = "assistant", content = _uiState.value.currentStream)), currentStream = "")"""

new_explain = """                val activeSessionId = database.appDao().getSetting("ACTIVE_SESSION_ID")?.value
                val sessionId = if (!activeSessionId.isNullOrBlank()) activeSessionId else java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = text, language = "$sourceLang -> $targetLang", sessionId = sessionId, mode = "explain")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()

                llmRepository.streamExplain(text, sourceLang, targetLang).collect {
                    _uiState.value = _uiState.value.copy(currentStream = it)
                }

                val savedMsg = initialMsg.copy(id = msgId, content = _uiState.value.currentStream)
                database.appDao().insertChatMessage(savedMsg)
                _uiState.value = SearchState(isLoading = false, word = initialWord.copy(id = wordId), chatMessages = listOf(savedMsg), currentStream = "")"""

text = text.replace(old_explain, new_explain)

# Refactor streamCompare
old_compare = """                llmRepository.streamCompare(words, sourceLang, targetLang).collect {
                    _uiState.value = _uiState.value.copy(currentStream = it)
                }
                val wordId = database.appDao().insertWord(com.aidict.app.data.entities.Word(profileId = profileId, term = words, sessionId = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date()), mode = "compare")).toInt()
                val msgId = database.appDao().insertChatMessage(com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = _uiState.value.currentStream)).toInt()
                _uiState.value = SearchState(isLoading = false, word = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = words, language = "$sourceLang -> $targetLang", mode = "compare", sessionId = ""), chatMessages = listOf(com.aidict.app.data.entities.ChatMessage(id = msgId, wordId = wordId, role = "assistant", content = _uiState.value.currentStream)), currentStream = "")"""

new_compare = """                val activeSessionId = database.appDao().getSetting("ACTIVE_SESSION_ID")?.value
                val sessionId = if (!activeSessionId.isNullOrBlank()) activeSessionId else java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = words, language = "$sourceLang -> $targetLang", sessionId = sessionId, mode = "compare")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()

                llmRepository.streamCompare(words, sourceLang, targetLang).collect {
                    _uiState.value = _uiState.value.copy(currentStream = it)
                }

                val savedMsg = initialMsg.copy(id = msgId, content = _uiState.value.currentStream)
                database.appDao().insertChatMessage(savedMsg)
                _uiState.value = SearchState(isLoading = false, word = initialWord.copy(id = wordId), chatMessages = listOf(savedMsg), currentStream = "")"""

text = text.replace(old_compare, new_compare)


with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

