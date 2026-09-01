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
    
    text = text.replace("IconButton) {", f"IconButton(onClick = {{ viewModel.deleteCurrentWord({mode_str}) }}) {{")
    
    with open(path, 'w') as f:
        f.write(text)

print("Fixed syntax error")
