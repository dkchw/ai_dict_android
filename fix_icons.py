import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

import_target = "import androidx.compose.material.icons.Icons"
import_replacement = "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.filled.Close\nimport androidx.compose.material.icons.filled.Add"
text = text.replace(import_target, import_replacement)

target = "androidx.compose.material.icons.Icons.Default.Close"
replacement = "Icons.Default.Close"
text = text.replace(target, replacement)

target = "androidx.compose.material.icons.Icons.Default.Add"
replacement = "Icons.Default.Add"
text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Fixed icons in AppNavigation.kt")
