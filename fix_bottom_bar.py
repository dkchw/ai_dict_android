import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

# Replace padding
text = text.replace('modifier = Modifier.fillMaxWidth().padding(16.dp)', 'modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 8.dp)')
# Decrease height of OutlinedTextField if we can. Actually padding(16.dp) was the main bulk.
# Let's adjust padding of the Row elements too.
# I'll just change the main padding.

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

