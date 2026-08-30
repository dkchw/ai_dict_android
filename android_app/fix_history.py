import re

with open('app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    svm = f.read()
if 'fun loadWord' not in svm:
    svm_add = """
    fun loadWord(word: com.aidict.app.data.entities.Word) {
        viewModelScope.launch {
            val messages = database.appDao().getChatMessagesSync(word.id)
            _uiState.value = SearchState(
                isLoading = false,
                word = word,
                chatMessages = messages,
                currentStream = "",
                error = null
            )
        }
    }
"""
    svm = svm.replace('fun clearCurrentSearch() {', svm_add + '\n    fun clearCurrentSearch() {')
    with open('app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
        f.write(svm)

with open('app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    hs = f.read()

# Add a lambda parameter to HistoryScreen
hs = hs.replace('fun HistoryScreen(appViewModel: com.aidict.app.ui.viewmodels.AppViewModel,', 'fun HistoryScreen(appViewModel: com.aidict.app.ui.viewmodels.AppViewModel,\n    onNavigateToChat: (Word) -> Unit,')

# Add BackHandler for detail pane
imports = """import androidx.compose.ui.unit.dp
import androidx.activity.compose.BackHandler"""
hs = hs.replace('import androidx.compose.ui.unit.dp', imports)

back_handler = """    var selectedWord by remember { mutableStateOf<Word?>(null) }
    
    if (selectedWord != null) {
        BackHandler {
            selectedWord = null
        }
    }"""
hs = hs.replace('var selectedWord by remember { mutableStateOf<Word?>(null) }', back_handler)

# Modify detailContent to render messages
detail_content = """        val detailContent = @Composable {
            Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text("Detail", style = MaterialTheme.typography.titleLarge)
                    Row {
                        Button(onClick = { onNavigateToChat(selectedWord!!) }) { Text("Resume Chat") }
                        Spacer(modifier = Modifier.width(8.dp))
                        IconButton(onClick = { selectedWord = null }) { Icon(Icons.Default.Close, contentDescription = "Close") }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                // Note: to render full messages dynamically here requires a flow or passing them from VM.
                // For now we just show the selected word's term, and the "Resume Chat" button takes them to it!
                Text("Word: ${selectedWord?.term}", style = MaterialTheme.typography.headlineSmall)
                Text("Language: ${selectedWord?.language}", style = MaterialTheme.typography.bodyLarge)
                Spacer(modifier = Modifier.height(16.dp))
                Text("Click 'Resume Chat' to view the full conversation history and continue where you left off.", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }"""
pattern = r'        val detailContent = @Composable \{\n            Column.*?Text\("Chat history for this word will appear here\."\)\n            \}\n        \}'
hs = re.sub(pattern, detail_content, hs, flags=re.DOTALL)

with open('app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(hs)

