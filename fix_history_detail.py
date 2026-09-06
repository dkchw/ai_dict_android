import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

target = """    val detailContent = @Composable {
        val messages by viewModel.selectedChatMessages.collectAsState()
        if (selectedWord != null) {"""
replacement = """    var isDetailSearching by remember { mutableStateOf(false) }
    var detailSearchQuery by remember { mutableStateOf("") }
    val detailContent = @Composable {
        val messages by viewModel.selectedChatMessages.collectAsState()
        if (selectedWord != null) {"""
text = text.replace(target, replacement)

target_row = """                    IconButton(onClick = {
                        val lastUserMsg = messages.findLast { it.role == "assistant" }"""
replacement_row = """                    IconButton(onClick = { isDetailSearching = !isDetailSearching }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Search, contentDescription = "Search in Chat")
                    }
                    IconButton(onClick = {
                        val lastUserMsg = messages.findLast { it.role == "assistant" }"""
text = text.replace(target_row, replacement_row)

target_body = """                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(8.dp))
                LazyColumn(modifier = Modifier.weight(1f).fillMaxWidth()) {"""
replacement_body = """                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(8.dp))
                if (isDetailSearching) {
                    OutlinedTextField(
                        value = detailSearchQuery,
                        onValueChange = { detailSearchQuery = it },
                        modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                        placeholder = { Text("Find in chat...") },
                        singleLine = true,
                        trailingIcon = {
                            if (detailSearchQuery.isNotEmpty()) {
                                IconButton(onClick = { detailSearchQuery = "" }) {
                                    Icon(Icons.Default.Clear, contentDescription = "Clear Search")
                                }
                            }
                        }
                    )
                }
                LazyColumn(modifier = Modifier.weight(1f).fillMaxWidth()) {"""
text = text.replace(target_body, replacement_body)

text = text.replace("com.aidict.app.ui.components.MarkdownText(\n                                            text = msg.content,\n                                            color = MaterialTheme.colorScheme.onSecondaryContainer\n                                        )", "com.aidict.app.ui.components.MarkdownText(\n                                            text = msg.content,\n                                            color = MaterialTheme.colorScheme.onSecondaryContainer,\n                                            searchQuery = detailSearchQuery\n                                        )")

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

print("Updated HistoryScreen detail view")
