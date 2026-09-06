import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

text = text.replace('import androidx.compose.runtime.*', 'import androidx.compose.runtime.*\nimport androidx.compose.foundation.lazy.items')

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)
print("Import added")
