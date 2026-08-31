import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Fix order
old_decl = """    val coroutineScope = rememberCoroutineScope()
    val currentMode = pagerState.targetPage
    val pagerState = androidx.compose.foundation.pager.rememberPagerState(initialPage = 0, pageCount = { 4 })"""

new_decl = """    val coroutineScope = rememberCoroutineScope()
    val pagerState = androidx.compose.foundation.pager.rememberPagerState(initialPage = 0, pageCount = { 4 })
    val currentMode = pagerState.targetPage"""
text = text.replace(old_decl, new_decl)

# Add import for launch
if 'import kotlinx.coroutines.launch' not in text:
    text = text.replace('import androidx.compose.runtime.*', 'import androidx.compose.runtime.*\nimport kotlinx.coroutines.launch')

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

