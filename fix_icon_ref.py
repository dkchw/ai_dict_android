import re
import os

screens = ['CompareScreen.kt', 'TranslateScreen.kt', 'ExplainScreen.kt']

for screen in screens:
    path = f'android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}'
    with open(path, 'r') as f:
        text = f.read()

    text = text.replace("androidx.compose.material.icons.Icons.Default.Search", "Icons.Default.Search")
    text = text.replace("androidx.compose.material.icons.Icons.Default.Clear", "Icons.Default.Clear")

    with open(path, 'w') as f:
        f.write(text)

print("Fixed icon refs")
