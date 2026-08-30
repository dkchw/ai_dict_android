import re

imports = """
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Warning
import androidx.compose.ui.platform.LocalContext
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.background
"""

files = [
    'android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt'
]

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # insert after the first import
    match = re.search(r'import .*\n', content)
    if match:
        content = content[:match.end()] + imports + content[match.end():]
    
    with open(file, 'w') as f:
        f.write(content)

