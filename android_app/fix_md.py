import re

files = [
    'app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt',
    'app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt',
    'app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt',
    'app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt'
]

for file in files:
    with open(file, 'r') as f:
        text = f.read()
    
    if 'import com.aidict.app.ui.components.MarkdownText' not in text:
        text = text.replace('import androidx.compose.ui.Modifier', 'import androidx.compose.ui.Modifier\nimport com.aidict.app.ui.components.MarkdownText')
        
    text = text.replace('Text(text = msg.content, color = MaterialTheme.colorScheme.onPrimary)', 'MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onPrimary)')
    text = text.replace('Text(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer)', 'MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer)')
    
    with open(file, 'w') as f:
        f.write(text)

