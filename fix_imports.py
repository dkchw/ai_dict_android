import re
import os

screens = ['CompareScreen.kt', 'TranslateScreen.kt', 'ExplainScreen.kt', 'SearchScreen.kt']

for screen in screens:
    path = f'android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}'
    with open(path, 'r') as f:
        text = f.read()

    imports = """import androidx.compose.ui.Alignment
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Clear"""
    
    if "import androidx.compose.ui.Alignment" not in text:
        text = text.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.Alignment")
    
    if "import androidx.compose.material.icons.filled.Search" not in text:
        text = text.replace("import androidx.compose.material.icons.filled.Delete", "import androidx.compose.material.icons.filled.Delete\nimport androidx.compose.material.icons.filled.Search")
        
    if "import androidx.compose.material.icons.filled.Clear" not in text:
        text = text.replace("import androidx.compose.material.icons.filled.Delete", "import androidx.compose.material.icons.filled.Delete\nimport androidx.compose.material.icons.filled.Clear")

    with open(path, 'w') as f:
        f.write(text)

print("Fixed imports")
