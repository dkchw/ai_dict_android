import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# I will just replace the catch block in retryMessage.
# It currently has:
target_catch = """            } catch (e: Exception) {
                _uiState.value.word?.let { w ->
                    val userMsg = com.aidict.app.data.entities.ChatMessage(wordId = w.id, role = "assistant", content = "*Generation Failed:* \\n${e.localizedMessage}")
                    database.appDao().insertChatMessage(userMsg)
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }"""

replacement_catch = """            } catch (e: Exception) {
                val errorMsg = loadingMsg.copy(content = "*Generation Failed:* \\n${e.localizedMessage}")
                database.appDao().insertChatMessage(errorMsg)
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }"""

# Note that searchWord, streamTranslation, streamExplain ALSO have this catch block!
# But for retryMessage, I'll just replace the one that follows `loadingMsg`.
# So let's find retryMessage boundaries.
start_idx = text.find("fun retryMessage")
end_idx = text.find("fun streamTranslation", start_idx)
sub_text = text[start_idx:end_idx]

sub_text = sub_text.replace(target_catch, replacement_catch)

text = text[:start_idx] + sub_text + text[end_idx:]

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

print("Fixed catch block in retryMessage")
