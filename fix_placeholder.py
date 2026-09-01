import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

# Fix the send icon in ChatInputBar
text = text.replace(
    'if (isFollowUp) Icons.AutoMirrored.Filled.Send else Icons.Default.Search',
    'if (isFollowUp && !autoNewSearch) Icons.AutoMirrored.Filled.Send else Icons.Default.Search'
)

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

# Fix placeholder in SearchScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'r') as f:
    text = f.read()
text = text.replace(
    'placeholder = if (isFollowUp) "Enter your question..." else "Search word..."',
    'placeholder = if (isFollowUp && !autoNewSearch) "Enter your question..." else "Search word..."'
)
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'w') as f:
    f.write(text)

# Fix placeholder in CompareScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'r') as f:
    text = f.read()
text = text.replace(
    'placeholder = if (state.word != null) "Enter your question..." else "Words to compare (comma separated)..."',
    'placeholder = if (state.word != null && !autoNewSearch) "Enter your question..." else "Words to compare (comma separated)..."'
)
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'w') as f:
    f.write(text)

# Fix placeholder in TranslateScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'r') as f:
    text = f.read()
text = text.replace(
    'placeholder = if (state.word != null) "Enter your question..." else "Text to translate..."',
    'placeholder = if (state.word != null && !autoNewSearch) "Enter your question..." else "Text to translate..."'
)
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'w') as f:
    f.write(text)

# Fix placeholder in ExplainScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'r') as f:
    text = f.read()
text = text.replace(
    'placeholder = if (state.word != null) "Enter your question..." else "Paste sentence/paragraph to explain..."',
    'placeholder = if (state.word != null && !autoNewSearch) "Enter your question..." else "Paste sentence/paragraph to explain..."'
)
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'w') as f:
    f.write(text)

