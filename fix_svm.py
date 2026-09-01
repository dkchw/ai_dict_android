import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# I will just revert the catch blocks to original, and then we know the history empty bug is because of the catch block dropping it.
# Actually I'll just change the catch blocks to insert a new message if _uiState has a word!
def replace_catch(match):
    return """} catch (e: Exception) {
                _uiState.value.word?.let { w ->
                    val userMsg = com.aidict.app.data.entities.ChatMessage(wordId = w.id, role = "assistant", content = "*Generation Failed:* \\n${e.localizedMessage}")
                    database.appDao().insertChatMessage(userMsg)
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }"""

text = re.sub(r'\} catch \(e: Exception\) \{\s+val errorMsg = savedMsg\.copy[^\}]+?\s+\}\s+\}', replace_catch, text)

# Also for retryMessage:
text = re.sub(r'\} catch \(e: Exception\) \{\s+val userMsg = ChatMessage.*?copy\(isLoading = false, error = e\.localizedMessage\)\s+\}\s+\}', replace_catch, text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

print("Fixed SearchViewModel catch scope issue")
