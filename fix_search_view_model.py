import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Fix catch blocks to save error message to database
def replace_catch(match):
    prefix = match.group(1)
    word_id_var = match.group(2)
    return f"""{prefix} catch (e: Exception) {{
                val errorMsg = savedMsg.copy(content = "*Generation Failed:* \\n${{e.localizedMessage}}")
                database.appDao().insertChatMessage(errorMsg)
                if (_uiState.value.word?.id == {word_id_var}) {{
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }}
            }}"""

text = re.sub(r'(}?) catch \(e: Exception\) \{\s+if \(_uiState\.value\.word\?.+? == .+?\) \{\s+_uiState\.value = _uiState\.value\.copy\(isLoading = false, error = e\.localizedMessage\)\s+\}\s+\}', 
              r'\1 catch (e: Exception) {\n                val errorMsg = savedMsg.copy(content = "*Generation Failed:* \\n${e.localizedMessage}")\n                database.appDao().insertChatMessage(errorMsg)\n                if (_uiState.value.word?.id == wordId) {\n                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)\n                }\n            }', 
              text)

# Also fix searchWord (which uses currentWordId)
text = text.replace("""catch (e: Exception) {
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }""", """catch (e: Exception) {
                val userMsg = ChatMessage(wordId = word.id, role = "assistant", content = "*Generation Failed:* \\n${e.localizedMessage}")
                database.appDao().insertChatMessage(userMsg)
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }""")

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

print("Fixed SearchViewModel catch blocks")
