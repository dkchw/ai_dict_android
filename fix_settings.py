import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Remove the invalid `item { Spacer(...) }` inside ExternalDictManager
text = text.replace('    item { Spacer(Modifier.height(16.dp)) }\n    SettingsGroup("External Dictionaries") {', '    Spacer(Modifier.height(16.dp))\n    SettingsGroup("External Dictionaries") {')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)
