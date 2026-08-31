import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

text = text.replace("import androidx.compose.foundation.text.KeyboardActions\nimport androidx.compose.ui.text.input.KeyboardActions as UIKeyboardActions", "")
text = text.replace("import androidx.compose.foundation.text.KeyboardOptions", "")
text = text.replace("import androidx.compose.ui.text.input.ImeAction", "")

text = text.replace("KeyboardOptions.Default.copy", "androidx.compose.foundation.text.KeyboardOptions.Default.copy")
text = text.replace("ImeAction.Send", "androidx.compose.ui.text.input.ImeAction.Send")
text = text.replace("ImeAction.Default", "androidx.compose.ui.text.input.ImeAction.Default")
text = text.replace("keyboardActions = KeyboardActions(", "keyboardActions = androidx.compose.foundation.text.KeyboardActions(")

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

