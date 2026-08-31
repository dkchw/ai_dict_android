with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Quote
q_old = '        item { Text("Inspirational Quote", style = MaterialTheme.typography.titleLarge) }\n\n        item {\n\n            val quote by viewModel.quoteMode.collectAsState()'
q_new = '        item {\n            SettingsGroup("Inspirational Quote") {\n                val quote by viewModel.quoteMode.collectAsState()'
text = text.replace(q_old, q_new)

q_end = '                }\n            }\n\n        }\n\n        item { Spacer(Modifier.height(16.dp)) }\n\n        item { Text("General", style = MaterialTheme.typography.titleLarge) }'
q_end_new = '                }\n            }\n            } // end group\n        }\n\n        item { Spacer(Modifier.height(16.dp)) }\n\n        item { Text("General", style = MaterialTheme.typography.titleLarge) }'
text = text.replace(q_end, q_end_new)


# General
g_old = '        item { Text("General", style = MaterialTheme.typography.titleLarge) }\n        \n        item {\n            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {'
g_new = '        item {\n            SettingsGroup("General") {\n            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {'
text = text.replace(g_old, g_new)

# Since General consists of multiple items, we'll just merge them by removing `item {` wrappers inside it
text = text.replace('        item {\n            var expanded by remember { mutableStateOf(false) }', '        var expanded by remember { mutableStateOf(false) }')
text = text.replace('            }\n        }\n\n        item { Spacer(Modifier.height(16.dp)) }\n        item { com.aidict.app.ui.components.MultiSelectSearchableDropdown', '            }\n        Spacer(Modifier.height(16.dp))\n        com.aidict.app.ui.components.MultiSelectSearchableDropdown')
text = text.replace('})\n        item {\n        }\n        item {\n            SettingsGroup("API Configuration") {', '})\n        } } // end group\n        item {\n            SettingsGroup("API Configuration") {')

# The empty `item { }` before API configuration:
#        item { com.aidict.app.ui.components.MultiSelectSearchableDropdown(...) }
#        item {
#        }
#        item { SettingsGroup("API Configuration") {
text = text.replace('})\n        item {\n        }\n        item {\n            SettingsGroup("API Configuration") {', '})\n        } } // end group\n        item {\n            SettingsGroup("API Configuration") {')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

