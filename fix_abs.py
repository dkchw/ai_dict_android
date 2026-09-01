import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

target = "if (pagerState.currentPage == 0 && pagerState.currentPageOffsetFraction <= 0.01f) {"
replacement = "if (pagerState.currentPage == 0 && kotlin.math.abs(pagerState.currentPageOffsetFraction) <= 0.01f) {"
text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Fixed abs condition")
