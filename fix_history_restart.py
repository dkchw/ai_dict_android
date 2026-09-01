import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

target = """                        onRestartChat = { word, msg, fallback ->
                            searchViewModel.loadWord(word)
                            val modeInt = when (word.mode) {
                                "dict" -> 0
                                "compare" -> 1
                                "translate" -> 2
                                "explain" -> 3
                                else -> 0
                            }
                            coroutineScope.launch { pagerState.scrollToPage(modeInt) }
                            currentScreen = Screen.MAIN
                            searchViewModel.retryMessage(msg, fallback, word.mode)
                        },"""

replacement = """                        onRestartChat = { word, msg, fallback ->
                            searchViewModel.loadWord(word)
                            // Don't switch screens, let it generate in the background
                            searchViewModel.retryMessage(msg, fallback, word.mode)
                        },"""

text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Let's modify retryMessage to add the "Generating..." placeholder
target_retry = """            // Delete the assistant message to restart generation from that point
            database.appDao().deleteChatMessage(assistantMsg)
            val historyBefore = database.appDao().getChatMessagesSync(assistantMsg.wordId)
            
            if (_uiState.value.word?.id == currentWordId) {"""

replacement_retry = """            // Delete the assistant message to restart generation from that point
            database.appDao().deleteChatMessage(assistantMsg)
            val historyBefore = database.appDao().getChatMessagesSync(assistantMsg.wordId)
            
            // Re-insert it with "Generating..." so the UI shows progress
            val loadingMsg = assistantMsg.copy(content = "Generating...")
            database.appDao().insertChatMessage(loadingMsg)
            
            if (_uiState.value.word?.id == currentWordId) {"""

text = text.replace(target_retry, replacement_retry)

# In the success branch, update it:
target_success = """                val finalMarkdown = currentText
                val newAssistantMsg = com.aidict.app.data.entities.ChatMessage(wordId = assistantMsg.wordId, role = "assistant", content = finalMarkdown)
                database.appDao().insertChatMessage(newAssistantMsg)"""

replacement_success = """                val finalMarkdown = currentText
                val newAssistantMsg = loadingMsg.copy(content = finalMarkdown)
                database.appDao().insertChatMessage(newAssistantMsg)"""

text = text.replace(target_success, replacement_success)

# Note: The catch branch ALREADY uses `assistantMsg.copy` or `w.id` and inserts a new message.
# Wait! In fix_svm.py, I made the catch block do this:
# `val userMsg = com.aidict.app.data.entities.ChatMessage(wordId = w.id, role = "assistant", content = "*Generation Failed:* \\n${e.localizedMessage}")`
# Since it creates a NEW message with a new ID (id = 0 by default), it will ADD a new message instead of overwriting `loadingMsg`!
# Let's check how the catch block looks in SearchViewModel.kt.
