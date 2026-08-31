import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

old_active_clickable = """                        items(wordsInSession, key = { it.id }) { word ->
                            Card(
                                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).clickable { selectedWord = word },"""
new_active_clickable = """                        items(wordsInSession, key = { it.id }) { word ->
                            Card(
                                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).clickable { selectedWord = word; viewModel.setSelectedWordId(word.id) },"""

text = text.replace(old_active_clickable, new_active_clickable)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

