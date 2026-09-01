import re

# 1. Fix AppNavigation.kt
with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

if "import androidx.compose.foundation.interaction.MutableInteractionSource" not in text:
    text = text.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.interaction.MutableInteractionSource")

# Wait, `Box(modifier = Modifier.fillMaxSize().clickable(...)) { focusManager.clearFocus() }) {`
# The `)` at the end of the Box is incorrect! It should be `) {`
text = text.replace("""    Box(modifier = Modifier.fillMaxSize().clickable(
        interactionSource = remember { MutableInteractionSource() },
        indication = null
    ) { focusManager.clearFocus() }) {""", """    Box(modifier = Modifier.fillMaxSize().clickable(
        interactionSource = remember { MutableInteractionSource() },
        indication = null
    ) { focusManager.clearFocus() }) {""")

# Actually let's just make it simple pointer input instead of clickable so we don't mess up Box syntax
# Wait, let's fix the Box syntax
text = text.replace("    ) { focusManager.clearFocus() }) {", "    ) { focusManager.clearFocus() }) {") # Still same
text = re.sub(r'Box\(modifier = Modifier\.fillMaxSize\(\)\.clickable\(\n\s*interactionSource = remember \{ MutableInteractionSource\(\) \},\n\s*indication = null\n\s*\) \{ focusManager\.clearFocus\(\) \}\) \{', 
              r'Box(modifier = Modifier.fillMaxSize().clickable(interactionSource = remember { MutableInteractionSource() }, indication = null) { focusManager.clearFocus() }) {', text)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

# 2. Fix HistoryScreen.kt
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("    onNavigateToChat: (Word) -> Unit,", "    onNavigateToChat: (Word) -> Unit,\n    onRestartChat: (Word, com.aidict.app.data.entities.ChatMessage, Boolean) -> Unit = {_,_,_ -> },")

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

# 3. Fix SearchViewModel.kt
with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Replace savedMsg with initialMsg/assistantMsg, and wordId with currentWordId in retryMessage
# For retryMessage:
text = text.replace("""            } catch (e: Exception) {
                val errorMsg = savedMsg.copy(content = "*Generation Failed:* \\n${e.localizedMessage}")
                database.appDao().insertChatMessage(errorMsg)
                if (_uiState.value.word?.id == wordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }""", """            } catch (e: Exception) {
                // Not in retry message
            }""") # We'll do it manually

