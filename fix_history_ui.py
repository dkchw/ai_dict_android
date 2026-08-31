import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

# Fix Session Header to include count
# Old active session header:
old_header = """                            Text(
                                text = session.name + if (isSessionActive) " (Active)" else "",
                                style = MaterialTheme.typography.titleMedium,"""

new_header = """                            Text(
                                text = "${session.name} (${wordsInSession.size})" + if (isSessionActive) " (Active)" else "",
                                style = MaterialTheme.typography.titleMedium,"""
text = text.replace(old_header, new_header)

# Fix unknown session header:
old_unknown_header = """                    item { Text(text = "Session: $sid", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(vertical = 8.dp)) }"""
new_unknown_header = """                    item { 
                        val count = (grouped[sid] ?: emptyList()).size
                        Text(text = "Session: $sid ($count)", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(vertical = 8.dp)) 
                    }"""
text = text.replace(old_unknown_header, new_unknown_header)

# Fix unknown session card to include color and stars
old_card_content = """                        Card(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).clickable { selectedWord = word },
                            elevation = CardDefaults.cardElevation(if (selectedWord?.id == word.id) 8.dp else 2.dp)
                        ) {
                            Row(modifier = Modifier.padding(start = 12.dp, top = 4.dp, bottom = 4.dp, end = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text(text = word.term, modifier = Modifier.weight(1f).padding(8.dp))
                                IconButton(onClick = {"""

new_card_content = """                        Card(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).clickable { selectedWord = word },
                            elevation = CardDefaults.cardElevation(if (selectedWord?.id == word.id) 8.dp else 2.dp),
                            colors = CardDefaults.cardColors(
                                containerColor = if (selectedWord?.id == word.id) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant
                            )
                        ) {
                            Row(modifier = Modifier.padding(start = 12.dp, top = 4.dp, bottom = 4.dp, end = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(text = word.term, style = MaterialTheme.typography.bodyLarge)
                                    if (!word.language.isNullOrBlank()) {
                                        Text(text = word.language, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.secondary)
                                    }
                                }
                                if (word.color != null) {
                                    val c = colors.find { it.first == word.color }?.second ?: androidx.compose.ui.graphics.Color.Gray
                                    Box(modifier = Modifier.size(12.dp).background(c, CircleShape).padding(end = 8.dp))
                                }
                                if (word.stars > 0) {
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Row { (1..word.stars).forEach { _ -> Icon(Icons.Default.Star, contentDescription = "Star", tint = androidx.compose.ui.graphics.Color(0xFFFFC107), modifier = Modifier.size(16.dp)) } }
                                }
                                IconButton(onClick = {"""
text = text.replace(old_card_content, new_card_content)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

