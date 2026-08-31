import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

pattern = r'sessions\.forEach \{ session ->\s*val wordsInSession = grouped\[session\.id\] \?: emptyList\(\)\s*if \(wordsInSession\.isNotEmpty\(\) \|\| sessions\.size > 1\) \{\s*item \{\s*Row\(verticalAlignment = Alignment\.CenterVertically, modifier = Modifier\.padding\(vertical = 8\.dp\)\) \{\s*Text\(\s*text = session\.name,\s*style = MaterialTheme\.typography\.titleMedium,\s*modifier = Modifier\.weight\(1f\)\s*\)'

replacement = r"""sessions.forEach { session ->
                    val wordsInSession = grouped[session.id] ?: emptyList()
                    val isSessionActive = activeSessionId == session.id
                    item {
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp).background(if (isSessionActive) MaterialTheme.colorScheme.primaryContainer else androidx.compose.ui.graphics.Color.Transparent, shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp)).clickable { viewModel.setActiveSession(session.id) }.padding(8.dp)) {
                            Text(
                                text = session.name + if (isSessionActive) " (Active)" else "",
                                style = MaterialTheme.typography.titleMedium,
                                color = if (isSessionActive) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface,
                                modifier = Modifier.weight(1f)
                            )"""

text = re.sub(pattern, replacement, text)

# Now we need to find the closing brace of the removed `if` statement.
# The `if` statement was around the `item { ... }` and `items(...) { ... }` blocks.
# Let's see what follows `items(wordsInSession)`.

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)
