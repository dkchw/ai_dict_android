import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

target = "        item { Spacer(Modifier.height(16.dp)) }\n        item {\n            SettingsGroup(\"System Prompts\") {"
replacement = "        item { Spacer(Modifier.height(16.dp)) }\n        item { ExternalDictManager(viewModel) }\n" + target

if "ExternalDictManager(viewModel)" not in text:
    text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

