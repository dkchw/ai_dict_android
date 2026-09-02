import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

text = text.replace(
    '    val starsFilter by viewModel.starsFilter.collectAsState()\n    var query',
    '    val starsFilter by viewModel.starsFilter.collectAsState()\n    val searchInOutput by viewModel.searchInOutput.collectAsState()\n    var query'
)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)
print("Injected searchInOutput into HistoryScreen")
