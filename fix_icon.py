import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

text = text.replace('androidx.compose.material.icons.Icons.Default.Info', 'androidx.compose.material.icons.Icons.Default.Search')

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

