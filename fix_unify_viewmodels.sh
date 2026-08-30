cat << 'INNER' >> android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt

    fun streamTranslation(text: String, source: String, target: String, profileId: Int) {
        viewModelScope.launch {
            _uiState.value = SearchState(isLoading = true, currentStream = "")
            try {
                llmRepository.streamTranslation(text, source, target).collect {
                    _uiState.value = _uiState.value.copy(currentStream = it)
                }
                val wordId = database.appDao().insertWord(com.aidict.app.data.entities.Word(profileId = profileId, term = text, language = "$source -> $target", sessionId = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date()), mode = "translate")).toInt()
                val msgId = database.appDao().insertChatMessage(com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = _uiState.value.currentStream)).toInt()
                _uiState.value = SearchState(isLoading = false, word = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = text, language = "$source -> $target", mode = "translate", sessionId = ""), chatMessages = listOf(com.aidict.app.data.entities.ChatMessage(id = msgId, wordId = wordId, role = "assistant", content = _uiState.value.currentStream)), currentStream = "")
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }

    fun streamExplain(text: String, profileId: Int) {
        viewModelScope.launch {
            _uiState.value = SearchState(isLoading = true, currentStream = "")
            try {
                llmRepository.streamExplain(text).collect { _uiState.value = _uiState.value.copy(currentStream = it) }
                val wordId = database.appDao().insertWord(com.aidict.app.data.entities.Word(profileId = profileId, term = text, sessionId = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date()), mode = "explain")).toInt()
                val msgId = database.appDao().insertChatMessage(com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = _uiState.value.currentStream)).toInt()
                _uiState.value = SearchState(isLoading = false, word = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = text, mode = "explain", sessionId = ""), chatMessages = listOf(com.aidict.app.data.entities.ChatMessage(id = msgId, wordId = wordId, role = "assistant", content = _uiState.value.currentStream)), currentStream = "")
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }

    fun streamCompare(word1: String, word2: String, profileId: Int) {
        viewModelScope.launch {
            _uiState.value = SearchState(isLoading = true, currentStream = "")
            try {
                llmRepository.streamCompare(word1, word2).collect { _uiState.value = _uiState.value.copy(currentStream = it) }
                val wordId = database.appDao().insertWord(com.aidict.app.data.entities.Word(profileId = profileId, term = "$word1 vs $word2", sessionId = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date()), mode = "compare")).toInt()
                val msgId = database.appDao().insertChatMessage(com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = _uiState.value.currentStream)).toInt()
                _uiState.value = SearchState(isLoading = false, word = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = "$word1 vs $word2", mode = "compare", sessionId = ""), chatMessages = listOf(com.aidict.app.data.entities.ChatMessage(id = msgId, wordId = wordId, role = "assistant", content = _uiState.value.currentStream)), currentStream = "")
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }
}
INNER

# Fix missing brace
sed -i '$d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt
