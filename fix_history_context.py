import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("    val isTablet = windowSizeClass.widthSizeClass == WindowWidthSizeClass.Expanded", "    val isTablet = windowSizeClass.widthSizeClass == WindowWidthSizeClass.Expanded\n    val context = androidx.compose.ui.platform.LocalContext.current")

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

print("Added context")
