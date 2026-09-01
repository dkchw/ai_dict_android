import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

target = "override fun onPreScroll(available: Offset, source: NestedScrollSource): Offset {"
replacement = "override fun onPreScroll(available: Offset, source: NestedScrollSource): Offset {\n                    if (source != androidx.compose.ui.input.nestedscroll.NestedScrollSource.Drag) return Offset.Zero"

text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Fixed NestedScrollSource")
