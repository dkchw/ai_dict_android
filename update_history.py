import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

# Replace the create session button
old_button = """            Button(onClick = { 
                val timeName = java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss", java.util.Locale.getDefault()).format(java.util.Date())
                viewModel.createSession(timeName)
            }, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Default.Add, contentDescription = "Create Session")
                Spacer(Modifier.width(8.dp))
                Text("Create Session")
            }"""

new_button = """            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = { viewModel.setActiveSession(null) },
                    modifier = Modifier.weight(1f),
                    colors = androidx.compose.material3.ButtonDefaults.buttonColors(
                        containerColor = if (activeSessionId.isNullOrBlank()) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                        contentColor = if (activeSessionId.isNullOrBlank()) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                ) {
                    Text("Default Session")
                }
                Button(
                    onClick = { showCreateSession = true }, 
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Default.Add, contentDescription = "Create Session")
                    Spacer(Modifier.width(8.dp))
                    Text("New Session")
                }
            }"""

text = text.replace(old_button, new_button)


# Add Date & Time to Details
old_details = """                    Text(text = "Details", style = MaterialTheme.typography.titleLarge, modifier = Modifier.weight(1f))
                    Button(onClick = { onNavigateToChat(selectedWord!!) }) { Text("Resume Chat") }
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(onClick = { selectedWord = null
                        viewModel.setSelectedWordId(null) }) {
                        Icon(Icons.Default.Close, contentDescription = "Close Details")
                    }
                }
                Spacer(modifier = Modifier.height(8.dp))
                LazyColumn(modifier = Modifier.weight(1f).fillMaxWidth()) {"""

new_details = """                    Text(text = "Details", style = MaterialTheme.typography.titleLarge, modifier = Modifier.weight(1f))
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
                Spacer(modifier = Modifier.height(8.dp))
                LazyColumn(modifier = Modifier.weight(1f).fillMaxWidth()) {"""

text = text.replace(old_details, new_details)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

