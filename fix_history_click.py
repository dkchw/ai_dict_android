import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

# Replace clickable { selectedWord = word }
# to clickable { selectedWord = word; viewModel.setSelectedWordId(word.id) }
text = text.replace('clickable { selectedWord = word }', 'clickable { selectedWord = word; viewModel.setSelectedWordId(word.id) }')

# Replace selectedWord = null
text = text.replace('selectedWord = null', 'selectedWord = null\n                        viewModel.setSelectedWordId(null)')
# Wait, replacing selectedWord = null will match multiple places. Let's just do LaunchedEffect instead.

text = text.replace('clickable { selectedWord = word }', 'clickable { selectedWord = word }') # Revert just in case

# Actually, the safest way is a LaunchedEffect(selectedWord)
launched_effect = """    if (selectedWord != null) {
        BackHandler {
            selectedWord = null
        }
    }"""
new_launched_effect = """    LaunchedEffect(selectedWord) {
        viewModel.setSelectedWordId(selectedWord?.id)
    }
    if (selectedWord != null) {
        BackHandler {
            selectedWord = null
        }
    }"""
text = text.replace(launched_effect, new_launched_effect)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

