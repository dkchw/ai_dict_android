import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

# Make Create Session button open dialog
old_btn = """            Button(onClick = { 
                val timeName = java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss", java.util.Locale.getDefault()).format(java.util.Date())
                viewModel.createSession(timeName)
            }, modifier = Modifier.fillMaxWidth()) {"""
new_btn = """            Button(onClick = { 
                showCreateSession = true
            }, modifier = Modifier.fillMaxWidth()) {"""
text = text.replace(old_btn, new_btn)

# Add activeSessionId flow
collect_sessions = """            val sessions by viewModel.sessions.collectAsState(initial = emptyList())"""
new_collect_sessions = """            val sessions by viewModel.sessions.collectAsState(initial = emptyList())
            val activeSessionId by viewModel.activeSessionId.collectAsState()"""
text = text.replace(collect_sessions, new_collect_sessions)

# Update session item rendering
old_session_render = """                sessions.forEach { session ->
                    val wordsInSession = grouped[session.id] ?: emptyList()
                    if (wordsInSession.isNotEmpty() || sessions.size > 1) {
                        item {
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 8.dp)) {
                                Text(
                                    text = session.name,
                                    style = MaterialTheme.typography.titleMedium,
                                    modifier = Modifier.weight(1f)
                                )"""

new_session_render = """                sessions.forEach { session ->
                    val wordsInSession = grouped[session.id] ?: emptyList()
                    
                    item {
                        val isSessionActive = activeSessionId == session.id
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp).background(if (isSessionActive) MaterialTheme.colorScheme.primaryContainer else androidx.compose.ui.graphics.Color.Transparent, shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp)).clickable { viewModel.setActiveSession(session.id) }.padding(8.dp)) {
                            Text(
                                text = session.name + if (isSessionActive) " (Active)" else "",
                                style = MaterialTheme.typography.titleMedium,
                                color = if (isSessionActive) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface,
                                modifier = Modifier.weight(1f)
                            )"""
text = text.replace(old_session_render, new_session_render)

# Remove the closing brace of the if statement we removed
# The closing brace is right before `items(wordsInSession, key = { it.id }) { word ->` ... wait!
# Let's see how it was structured.
old_items = """                            }
                        }
                        items(wordsInSession, key = { it.id }) { word ->"""
new_items = """                            }
                        }
                        items(wordsInSession, key = { it.id }) { word ->"""
# Oh wait, the if statement closing brace is AT THE END of the session block!
