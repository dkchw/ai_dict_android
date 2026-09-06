import re
import os

path = 'android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt'
with open(path, 'r') as f:
    text = f.read()

text = text.replace("androidx.compose.material.icons.Icons.Default.Search", "Icons.Default.Search")
text = text.replace("androidx.compose.material.icons.Icons.Default.Clear", "Icons.Default.Clear")
text = text.replace("androidx.compose.material.icons.Icons.Default.Refresh", "Icons.Default.Refresh")
text = text.replace("androidx.compose.material.icons.Icons.Default.Autorenew", "Icons.Default.Autorenew")
text = text.replace("Icons.Default.Clear", "androidx.compose.material.icons.Icons.Default.Clear")
text = text.replace("Icons.Default.Search", "androidx.compose.material.icons.Icons.Default.Search")

with open(path, 'w') as f:
    f.write(text)

print("Fixed icon refs in History")
