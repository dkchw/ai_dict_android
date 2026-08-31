import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# API Configuration
a_old = '        item { Text("API Configuration", style = MaterialTheme.typography.titleLarge) }\n        item {\n            var passwordVisible by remember { mutableStateOf(false) }'
a_new = '        item {\n            SettingsGroup("API Configuration") {\n                var passwordVisible by remember { mutableStateOf(false) }'
text = text.replace(a_old, a_new)

a_end = '                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)\n            )\n        }\n        \n        item { Spacer(Modifier.height(16.dp)) }\n        item {\n            SettingsGroup("Models") {'
a_end_new = '                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)\n            )\n            } // end group\n        }\n        \n        item { Spacer(Modifier.height(16.dp)) }\n        item {\n            SettingsGroup("Models") {'
text = text.replace(a_end, a_end_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)
