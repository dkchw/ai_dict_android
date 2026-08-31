import re

# SearchScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('placeholder = if (isFollowUp) "Ask a follow up question..." else "Search word...",', 
                    'placeholder = if (isFollowUp) "Enter your question..." else "Search word...",')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'w') as f:
    f.write(text)

# CompareScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('placeholder = "Words to compare (comma separated)..."', 
                    'placeholder = if (state.word != null) "Enter your question..." else "Words to compare (comma separated)..."')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'w') as f:
    f.write(text)

# TranslateScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('placeholder = "Text to translate...",', 
                    'placeholder = if (state.word != null) "Enter your question..." else "Text to translate...",')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'w') as f:
    f.write(text)

# ExplainScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('placeholder = "Paste sentence/paragraph to explain..."', 
                    'placeholder = if (state.word != null) "Enter your question..." else "Paste sentence/paragraph to explain..."')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'w') as f:
    f.write(text)

