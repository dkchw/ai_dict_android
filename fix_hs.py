import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

# Add LaunchedEffect to notify ViewModel of word selection
launched_effect = """    var selectedWord by remember { mutableStateOf<Word?>(null) }
    
    LaunchedEffect(selectedWord) {
        viewModel.setSelectedWordId(selectedWord?.id)
    }"""
text = text.replace('    var selectedWord by remember { mutableStateOf<Word?>(null) }', launched_effect)

# Update detailContent to render messages
detail_content_old = """    val detailContent = @Composable {
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

detail_content_new = """    val detailContent = @Composable {
        val messages by viewModel.selectedChatMessages.collectAsState()
        if (selectedWord != null) {
            Column(modifier = Modifier.fillMaxSize().padding(16.dp).background(MaterialTheme.colorScheme.surface)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(text = "Details", style = MaterialTheme.typography.titleLarge, modifier = Modifier.weight(1f))
                    Button(onClick = { onNavigateToChat(selectedWord!!) }) { Text("Resume Chat") }
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(onClick = { selectedWord = null }) {
                        Icon(Icons.Default.Close, contentDescription = "Close Details")
                    }
                }
                Spacer(modifier = Modifier.height(8.dp))
                LazyColumn(modifier = Modifier.weight(1f).fillMaxWidth()) {
                    items(messages) { msg ->
                        val isUser = msg.role == "user"
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth(if (isUser) 0.85f else 1f)
                                    .background(
                                        color = if (isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.secondaryContainer,
                                        shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp)
                                    )
                                    .padding(12.dp)
                            ) {
                                com.aidict.app.ui.components.MarkdownText(
                                    text = msg.content,
                                    color = if (isUser) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSecondaryContainer
                                )
                            }
                        }
                    }
                }
            }
        }
    }"""

text = text.replace(detail_content_old, detail_content_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)
