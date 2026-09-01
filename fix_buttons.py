import re
import os

files_modes = {
    'SearchScreen.kt': '"dict"',
    'CompareScreen.kt': '"compare"',
    'TranslateScreen.kt': '"translate"',
    'ExplainScreen.kt': '"explain"'
}

for file_name, mode_str in files_modes.items():
    path = f'android_app/app/src/main/java/com/aidict/app/ui/screens/{file_name}'
    with open(path, 'r') as f:
        text = f.read()
    
    text = text.replace('val lastUserMsg = state.chatMessages.findLast { it.role == "user" }', 'val lastUserMsg = state.chatMessages.findLast { it.role == "assistant" }')
    
    with open(path, 'w') as f:
        f.write(text)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

text = text.replace('val lastUserMsg = messages.findLast { it.role == "user" }', 'val lastUserMsg = messages.findLast { it.role == "assistant" }')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

print("Fixed buttons to use assistant message instead of user message")
