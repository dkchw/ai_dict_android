import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

text = text.replace('state = pagerState,\n                            modifier = Modifier.fillMaxSize()\n                        ) { page ->', 'state = pagerState,\n                            modifier = Modifier.fillMaxSize(),\n                            beyondBoundsPageCount = 1\n                        ) { page ->')

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

