import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    hs = f.read()

replacement = """    val detailContent = @Composable {
        if (selectedWord != null) {
            Column(modifier = Modifier.fillMaxSize().padding(16.dp).background(MaterialTheme.colorScheme.surface)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(text = "Details", style = MaterialTheme.typography.headlineSmall, modifier = Modifier.weight(1f))
                    Button(onClick = { onNavigateToChat(selectedWord!!) }) { Text("Resume Chat") }
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(onClick = { selectedWord = null }) {
                        Icon(Icons.Default.Close, contentDescription = "Close Details")
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                Text("Word: ${selectedWord?.term}", style = MaterialTheme.typography.titleMedium)
                Text("Language/Mode: ${selectedWord?.language}", style = MaterialTheme.typography.bodyMedium)
                Spacer(modifier = Modifier.height(16.dp))
                Text("Click 'Resume Chat' to view the full conversation history and continue where you left off.", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }"""

pattern = r'    val detailContent = @Composable \{\n        if \(selectedWord != null\) \{\n            Column.*?Text\("Chat history for this word will appear here\."\)\n            \}\n        \}\n    \}'

hs = re.sub(pattern, replacement, hs, flags=re.DOTALL)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(hs)
