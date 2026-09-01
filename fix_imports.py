import re

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
    text = f.read()

# Replace the invalid syntax
text = text.replace('.androidx.compose.foundation.layout.width', '.width')
text = text.replace('.androidx.compose.foundation.layout.heightIn', '.heightIn')

# Add imports
imports = """import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.fillMaxWidth
"""
text = text.replace('import androidx.compose.foundation.layout.fillMaxWidth', imports)

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
    f.write(text)

