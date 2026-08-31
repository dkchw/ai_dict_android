import re

# Update SearchScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('externalLinks = externalLinks,', 'externalLinks = if (state.word != null) externalLinks else emptyList(),')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'w') as f:
    f.write(text)

# Update CompareScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('externalLinks = externalLinks,', 'externalLinks = if (state.word != null) externalLinks else emptyList(),')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'w') as f:
    f.write(text)

# Update ExplainScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('    val externalLinks by viewModel.externalLinks.collectAsState()\n', '')
text = re.sub(r'\s*externalLinks = externalLinks,.*?context\.startActivity\(intent\)\n\s*\}\n\s*\},', '', text, flags=re.DOTALL)
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'w') as f:
    f.write(text)

# Update TranslateScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('    val externalLinks by viewModel.externalLinks.collectAsState()\n', '')
text = re.sub(r'\s*externalLinks = externalLinks,.*?context\.startActivity\(intent\)\n\s*\}\n\s*\},', '', text, flags=re.DOTALL)
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'w') as f:
    f.write(text)

