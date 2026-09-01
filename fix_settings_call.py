import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

target = """        item {
            SettingsGroup("App Behavior") {"""

replacement = """        item { ExternalDictManager(viewModel) }
        item {
            SettingsGroup("App Behavior") {"""

if "item { ExternalDictManager(viewModel) }" not in text:
    text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

