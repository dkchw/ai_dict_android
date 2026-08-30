cat << 'INNER' >> android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt

    fun clearCurrentSearch() {
        _uiState.value = SearchState()
    }

    fun deleteMessage(msg: com.aidict.app.data.entities.ChatMessage) {
        viewModelScope.launch {
            database.appDao().deleteChatMessage(msg)
            val updated = database.appDao().getChatMessages(msg.wordId)
            if (updated.isEmpty() || updated.none { it.role == "assistant" }) {
                deleteCurrentWord()
            } else {
                _uiState.value = _uiState.value.copy(chatMessages = updated)
            }
        }
    }

    fun editMessage(msg: com.aidict.app.data.entities.ChatMessage, newContent: String) {
        viewModelScope.launch {
            val updatedMsg = msg.copy(content = newContent)
            database.appDao().insertChatMessage(updatedMsg)
            val updated = database.appDao().getChatMessages(msg.wordId)
            _uiState.value = _uiState.value.copy(chatMessages = updated)
        }
    }

    fun retryMessage(assistantMsg: com.aidict.app.data.entities.ChatMessage, forceFallback: Boolean) {
        viewModelScope.launch {
            // Delete the assistant message to restart generation from that point
            database.appDao().deleteChatMessage(assistantMsg)
            val historyBefore = database.appDao().getChatMessages(assistantMsg.wordId)
            
            _uiState.value = _uiState.value.copy(
                chatMessages = historyBefore,
                isLoading = true,
                currentStream = ""
            )

            try {
                // Determine if this is the first message or a follow-up
                if (historyBefore.size == 1 && historyBefore.first().role == "user") {
                    val userMsg = historyBefore.first()
                    // Re-run searchWord logic essentially, or just stream chat
                    llmRepository.streamChat(historyBefore, forceFallback).collect { currentText ->
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                } else {
                    llmRepository.streamChat(historyBefore, forceFallback).collect { currentText ->
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMarkdown = _uiState.value.currentStream
                val newAssistantMsg = com.aidict.app.data.entities.ChatMessage(wordId = assistantMsg.wordId, role = "assistant", content = finalMarkdown)
                val newId = database.appDao().insertChatMessage(newAssistantMsg).toInt()

                val finalMessages = database.appDao().getChatMessages(assistantMsg.wordId)
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    chatMessages = finalMessages,
                    currentStream = ""
                )

            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }
INNER
