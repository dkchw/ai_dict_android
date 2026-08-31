import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('val sessions by viewModel.sessions.collectAsState()', 'val sessions by viewModel.sessions.collectAsState()\n    val activeSessionId by viewModel.activeSessionId.collectAsState()')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()
if 'import kotlinx.coroutines.flow.map' not in text:
    text = text.replace('import kotlinx.coroutines.flow.flatMapLatest', 'import kotlinx.coroutines.flow.flatMapLatest\nimport kotlinx.coroutines.flow.map')
with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)
