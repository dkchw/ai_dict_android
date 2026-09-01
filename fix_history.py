import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("    onNavigateToChat: (com.aidict.app.data.entities.Word) -> Unit,", "    onNavigateToChat: (com.aidict.app.data.entities.Word) -> Unit,\n    onRestartChat: (com.aidict.app.data.entities.Word, com.aidict.app.data.entities.ChatMessage, Boolean) -> Unit = {_,_,_ -> },")

# Now add the buttons to the detail view Row
target_row = """                    SelectionContainer(modifier = Modifier.weight(1f)) { Text(text = "Details", style = MaterialTheme.typography.titleLarge) }
                    Button(onClick = { onNavigateToChat(selectedWord!!) }) { Text("Resume Chat") }
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(onClick = { selectedWord = null
                        viewModel.setSelectedWordId(null) }) {"""

new_row = """                    SelectionContainer(modifier = Modifier.weight(1f)) { Text(text = "Details", style = MaterialTheme.typography.titleLarge) }
                    IconButton(onClick = {
                        val lastUserMsg = messages.findLast { it.role == "user" }
                        if (lastUserMsg != null) onRestartChat(selectedWord!!, lastUserMsg, false)
                    }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Refresh, contentDescription = "Restart with Current Model", tint = MaterialTheme.colorScheme.primary)
                    }
                    IconButton(onClick = {
                        val lastUserMsg = messages.findLast { it.role == "user" }
                        if (lastUserMsg != null) onRestartChat(selectedWord!!, lastUserMsg, true)
                    }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Autorenew, contentDescription = "Restart with Fallback Model", tint = MaterialTheme.colorScheme.error)
                    }
                    Button(onClick = { onNavigateToChat(selectedWord!!) }) { Text("Resume Chat") }
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(onClick = { selectedWord = null
                        viewModel.setSelectedWordId(null) }) {"""

text = text.replace(target_row, new_row)

if "import androidx.compose.material.icons.filled.Refresh" not in text:
    text = text.replace("import androidx.compose.material.icons.filled.Close", "import androidx.compose.material.icons.filled.Close\nimport androidx.compose.material.icons.filled.Refresh\nimport androidx.compose.material.icons.filled.Autorenew")

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

print("Updated HistoryScreen.kt")
