import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

target = "val leftOverscrollConnection = remember(pagerState.currentPage) {"
replacement = "val context = androidx.compose.ui.platform.LocalContext.current\n        " + target

text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Fixed context variable")
