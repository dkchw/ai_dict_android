import re
import glob

for filename in glob.glob('android_app/app/src/main/java/com/aidict/app/ui/screens/*Screen.kt'):
    if filename.endswith('HistoryScreen.kt') or filename.endswith('SettingsScreen.kt') or filename.endswith('NotesScreen.kt'):
        continue
    
    with open(filename, 'r') as f:
        text = f.read()
    
    old_lazy = """        LazyColumn(modifier = Modifier.weight(1f)) {
            items(state.chatMessages) {"""
    
    new_lazy = """        LazyColumn(modifier = Modifier.weight(1f)) {
            if (state.chatMessages.isEmpty()) {
                item { Spacer(modifier = Modifier.fillParentMaxSize()) }
            }
            items(state.chatMessages) {"""
            
    if old_lazy in text:
        text = text.replace(old_lazy, new_lazy)
        with open(filename, 'w') as f:
            f.write(text)

