import re

files = [
    'android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt'
]

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

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # 1. Fix the corrupted import LazyColumn string:
    content = content.replace("import androidx.compose.foundation.lazy.val context = LocalContext.current\n        val clipboardManager = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager\n        LazyColumn", "import androidx.compose.foundation.lazy.LazyColumn")
    
    # 2. Fix the corrupted imports location (package at line 2)
    # If package is at line 2, move it to the top!
    if 'package com.aidict.app.ui.screens' in content:
        content = content.replace('package com.aidict.app.ui.screens', '')
        content = 'package com.aidict.app.ui.screens\n\n' + content
        
    # 3. Add context and clipboardManager inside the composable correctly!
    # Find `var text by remember` and insert there
    match = re.search(r'var text by remember \{ mutableStateOf\(""\) \}', content)
    if match:
        insertion = """var text by remember { mutableStateOf("") }
    val context = LocalContext.current
    val clipboardManager = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager"""
        content = content.replace(match.group(0), insertion)
        
    # for TranslateScreen, it's sourceText
    match2 = re.search(r'var sourceText by remember \{ mutableStateOf\(""\) \}', content)
    if match2:
        insertion2 = """var sourceText by remember { mutableStateOf("") }
    val context = LocalContext.current
    val clipboardManager = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager"""
        content = content.replace(match2.group(0), insertion2)
        
    with open(file, 'w') as f:
        f.write(content)

