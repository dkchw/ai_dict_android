import re

files = [
    'android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt'
]

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # ensure val context = LocalContext.current exists before LazyColumn
    if 'val context = LocalContext.current' not in content and 'LazyColumn' in content:
        content = content.replace('LazyColumn', 'val context = LocalContext.current\n        val clipboardManager = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager\n        LazyColumn', 1)
        
    with open(file, 'w') as f:
        f.write(content)
