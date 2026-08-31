import sys, re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

def replace_function(text, func_name, new_func_code):
    match = re.search(r'^\s*fun ' + func_name + r'\(.*?\)\s*\{', text, re.MULTILINE)
    if not match: return text
    start_idx = match.start()
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

follow_up_code = """    fun sendFollowUpMessage(content: String, mode: String = "dict") {
        val _uiState = getUiState(mode)
        val word = _uiState.value.word ?: return
        val currentWordId = word.id
        viewModelScope.launch {
            val userMsg = ChatMessage(wordId = word.id, role = "user", content = content)
            val userMsgId = database.appDao().insertChatMessage(userMsg).toInt()
            
            val updatedMessages = database.appDao().getChatMessagesSync(word.id)
            if (_uiState.value.word?.id == currentWordId) {
                _uiState.value = _uiState.value.copy(chatMessages = updatedMessages, isLoading = true, currentStream = "")
            }

            try {
                var currentText = ""
                llmRepository.streamChat(word, updatedMessages).collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == currentWordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }
                val assistantMsg = ChatMessage(wordId = word.id, role = "assistant", content = currentText)
                database.appDao().insertChatMessage(assistantMsg)
                
                val finalMessages = database.appDao().getChatMessagesSync(word.id)
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, chatMessages = finalMessages, currentStream = "")
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }"""

retry_code = """    fun retryMessage(assistantMsg: com.aidict.app.data.entities.ChatMessage, forceFallback: Boolean, mode: String = "dict") {
        val _uiState = getUiState(mode)
        val word = _uiState.value.word ?: return
        val currentWordId = word.id
        viewModelScope.launch {
            // Delete the assistant message to restart generation from that point
            database.appDao().deleteChatMessage(assistantMsg)
            val historyBefore = database.appDao().getChatMessagesSync(assistantMsg.wordId)
            
            if (_uiState.value.word?.id == currentWordId) {
                _uiState.value = _uiState.value.copy(
                    chatMessages = historyBefore,
                    isLoading = true,
                    currentStream = ""
                )
            }

            try {
                var currentText = ""
                // Determine if this is the first message or a follow-up
                val flow = if (historyBefore.size == 1 && historyBefore.first().role == "user") {
                    llmRepository.streamChat(word, historyBefore, forceFallback)
                } else {
                    llmRepository.streamChat(word, historyBefore, forceFallback)
                }
                
                flow.collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == currentWordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMarkdown = currentText
                val newAssistantMsg = com.aidict.app.data.entities.ChatMessage(wordId = assistantMsg.wordId, role = "assistant", content = finalMarkdown)
                database.appDao().insertChatMessage(newAssistantMsg)

                val finalMessages = database.appDao().getChatMessagesSync(assistantMsg.wordId)
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        chatMessages = finalMessages,
                        currentStream = ""
                    )
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }"""

text = replace_function(text, 'sendFollowUpMessage', follow_up_code)
text = replace_function(text, 'retryMessage', retry_code)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)
