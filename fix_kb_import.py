import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

text = text.replace("import androidx.compose.foundation.text.KeyboardActions", "import androidx.compose.foundation.text.KeyboardActions\nimport androidx.compose.ui.text.input.KeyboardActions as UIKeyboardActions")
# Wait, just import it from `androidx.compose.foundation.text.KeyboardActions`.

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

