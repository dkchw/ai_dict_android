import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

text = text.replace(
    ".androidx.compose.ui.draw.clip(CircleShape)",
    ".clip(CircleShape)"
)

text = text.replace(
    "Modifier.androidx.compose.foundation.combinedClickable(",
    "Modifier.combinedClickable("
)

text = text.replace(
    "androidx.compose.foundation.text.KeyboardOptions",
    "androidx.compose.foundation.text.KeyboardOptions" # wait, let's just use KeyboardOptions
)

text = text.replace(
    "keyboardOptions = androidx.compose.foundation.text.KeyboardOptions.Default.copy",
    "keyboardOptions = androidx.compose.foundation.text.KeyboardOptions.Default.copy"
)
# Actually, KeyboardOptions is `androidx.compose.foundation.text.KeyboardOptions`
# Let's just import them at the top.

imports = """import androidx.compose.ui.draw.clip
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.ui.text.input.ImeAction"""

if "import androidx.compose.ui.draw.clip" not in text:
    text = text.replace("import androidx.compose.ui.Alignment", imports + "\nimport androidx.compose.ui.Alignment")

text = text.replace("androidx.compose.foundation.text.KeyboardOptions.Default", "KeyboardOptions.Default")
text = text.replace("androidx.compose.ui.text.input.ImeAction.Send", "ImeAction.Send")
text = text.replace("androidx.compose.ui.text.input.ImeAction.Default", "ImeAction.Default")
text = text.replace("androidx.compose.foundation.text.KeyboardActions", "KeyboardActions")

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

