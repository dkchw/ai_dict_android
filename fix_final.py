import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

text = text.replace("    val bgDict by settingsViewModel.bgDict.collectAsState()", "    val focusManager = androidx.compose.ui.platform.LocalFocusManager.current\n    val bgDict by settingsViewModel.bgDict.collectAsState()")
with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Just replace ALL catch blocks in stream methods that look like:
# } catch (e: Exception) {
#    val errorMsg = savedMsg.copy(content = "*Generation Failed:* \n${e.localizedMessage}")
#    database.appDao().insertChatMessage(errorMsg)
#    if (_uiState.value.word?.id == wordId) {
#        _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
#    }
# }
text = re.sub(r'\} catch \(e: Exception\) \{\n\s*val errorMsg = savedMsg.*?_uiState\.value = _uiState\.value\.copy\(isLoading = false, error = e\.localizedMessage\)\n\s*\}\n\s*\}',
              r'} catch (e: Exception) {\n                _uiState.value.word?.let { w ->\n                    val userMsg = com.aidict.app.data.entities.ChatMessage(wordId = w.id, role = "assistant", content = "*Generation Failed:* \\n${e.localizedMessage}")\n                    database.appDao().insertChatMessage(userMsg)\n                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)\n                }\n            }',
              text, flags=re.DOTALL)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)
print("Fixed AppNavigation and SearchViewModel")
