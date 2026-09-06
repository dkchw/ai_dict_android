import re

path = 'android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt'
with open(path, 'r') as f:
    text = f.read()

# Make sure we import Search and Clear
if "import androidx.compose.material.icons.filled.Search" not in text:
    text = text.replace("import androidx.compose.material.icons.filled.Delete", "import androidx.compose.material.icons.filled.Delete\nimport androidx.compose.material.icons.filled.Search\nimport androidx.compose.material.icons.filled.Clear")

# Reset fully qualified names
text = text.replace("androidx.compose.material.icons.Icons.Default.Search", "Icons.Default.Search")
text = text.replace("androidx.compose.material.icons.Icons.Default.Clear", "Icons.Default.Clear")
text = text.replace("androidx.compose.material.icons.Icons.Default.Refresh", "Icons.Default.Refresh")
text = text.replace("androidx.compose.material.icons.Icons.Default.Autorenew", "Icons.Default.Autorenew")

with open(path, 'w') as f:
    f.write(text)
print("Fixed HistoryScreen properly")
