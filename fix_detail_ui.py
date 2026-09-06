import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

target = """    val detailContent = @Composable {
        val messages by viewModel.selectedChatMessages.collectAsState()
        if (selectedWord != null) {
            Column(modifier = Modifier.fillMaxSize().padding(16.dp).background(MaterialTheme.colorScheme.surface)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    SelectionContainer(modifier = Modifier.weight(1f)) { Text(text = "Details", style = MaterialTheme.typography.titleLarge) }
                    IconButton(onClick = { isDetailSearching = !isDetailSearching }) {
                        Icon(Icons.Default.Search, contentDescription = "Search in Chat")
                    }
                    IconButton(onClick = {
                        val lastUserMsg = messages.findLast { it.role == "assistant" }
                        if (lastUserMsg != null) onRestartChat(selectedWord!!, lastUserMsg, false)
                    }) {
                        Icon(Icons.Default.Refresh, contentDescription = "Restart with Current Model", tint = MaterialTheme.colorScheme.primary)
                    }
                    IconButton(onClick = { isDetailSearching = !isDetailSearching }) {
                        Icon(Icons.Default.Search, contentDescription = "Search in Chat")
                    }
                    IconButton(onClick = {
                        val lastUserMsg = messages.findLast { it.role == "assistant" }
                        if (lastUserMsg != null) onRestartChat(selectedWord!!, lastUserMsg, true)
                    }) {
                        Icon(Icons.Default.Autorenew, contentDescription = "Restart with Fallback Model", tint = MaterialTheme.colorScheme.error)
                    }
                    Button(onClick = { onNavigateToChat(selectedWord!!) }) { Text("Resume Chat") }
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(onClick = { selectedWord = null
                        viewModel.setSelectedWordId(null) }) {
                        Icon(Icons.Default.Close, contentDescription = "Close Details")
                    }
                }
                Text(
                    text = java.text.SimpleDateFormat("MMM dd, yyyy  HH:mm", java.util.Locale.getDefault()).format(java.util.Date(selectedWord!!.createdAt)),
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "Searches: ${selectedWord!!.searchCount} | Views: ${selectedWord!!.viewCount} | Gens: ${selectedWord!!.generationCount}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(8.dp))
                if (isDetailSearching) {"""

replacement = """    val detailContent = @Composable {
        val messages by viewModel.selectedChatMessages.collectAsState()
        if (selectedWord != null) {
            Column(modifier = Modifier.fillMaxSize().padding(16.dp).background(MaterialTheme.colorScheme.surface)) {
                
                androidx.compose.material3.Card(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                    colors = androidx.compose.material3.CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            SelectionContainer(modifier = Modifier.weight(1f)) { 
                                Text(
                                    text = selectedWord!!.term, 
                                    style = MaterialTheme.typography.titleLarge,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                            IconButton(onClick = { 
                                selectedWord = null
                                viewModel.setSelectedWordId(null) 
                            }) {
                                Icon(Icons.Default.Close, contentDescription = "Close Details")
                            }
                        }
                        
                        Text(
                            text = java.text.SimpleDateFormat("MMM dd, yyyy  HH:mm", java.util.Locale.getDefault()).format(java.util.Date(selectedWord!!.createdAt)),
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Text(
                            text = "Searches: ${selectedWord!!.searchCount} | Views: ${selectedWord!!.viewCount} | Gens: ${selectedWord!!.generationCount}",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        
                        Spacer(modifier = Modifier.height(12.dp))
                        
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                            Button(
                                onClick = { onNavigateToChat(selectedWord!!) },
                                modifier = Modifier.weight(1f)
                            ) {
                                Text("Resume Chat")
                            }
                            
                            IconButton(
                                onClick = { isDetailSearching = !isDetailSearching }, 
                                modifier = Modifier.background(MaterialTheme.colorScheme.primaryContainer, androidx.compose.foundation.shape.CircleShape)
                            ) {
                                Icon(Icons.Default.Search, contentDescription = "Search in Chat", tint = MaterialTheme.colorScheme.onPrimaryContainer)
                            }
                            
                            IconButton(
                                onClick = {
                                    val lastUserMsg = messages.findLast { it.role == "assistant" }
                                    if (lastUserMsg != null) onRestartChat(selectedWord!!, lastUserMsg, false)
                                }, 
                                modifier = Modifier.background(MaterialTheme.colorScheme.secondaryContainer, androidx.compose.foundation.shape.CircleShape)
                            ) {
                                Icon(Icons.Default.Refresh, contentDescription = "Restart with Current Model", tint = MaterialTheme.colorScheme.primary)
                            }
                            
                            IconButton(
                                onClick = {
                                    val lastUserMsg = messages.findLast { it.role == "assistant" }
                                    if (lastUserMsg != null) onRestartChat(selectedWord!!, lastUserMsg, true)
                                }, 
                                modifier = Modifier.background(MaterialTheme.colorScheme.errorContainer, androidx.compose.foundation.shape.CircleShape)
                            ) {
                                Icon(Icons.Default.Autorenew, contentDescription = "Restart with Fallback Model", tint = MaterialTheme.colorScheme.error)
                            }
                        }
                    }
                }
                
                if (isDetailSearching) {"""

text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

print("Updated Detail Window UI")
