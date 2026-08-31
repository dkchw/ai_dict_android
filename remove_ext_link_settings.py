import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Remove externalLinks collectAsState
text = re.sub(r'val externalLinks by viewModel\.externalLinks\.collectAsState\(\)\n\s*', '', text)

# Remove the block from item { Text("External Link", ...) } to the Add External Link button
# The block starts at `item { Text("External Link", style = MaterialTheme.typography.titleLarge) }`
# and ends before `item { Spacer(Modifier.height(16.dp)) }` above "Prompts".
# We use regex with DOTALL to remove it.

pattern = r'item \{ Text\("External Link", style = MaterialTheme\.typography\.titleLarge\) \}.*?Add External Link"\)\n\s*\}\n\s*\}'
text = re.sub(pattern, '', text, flags=re.DOTALL)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

