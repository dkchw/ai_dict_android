import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

settings_start = """        item { Text("Display & Scaling", style = MaterialTheme.typography.titleLarge) }"""

settings_new = """        item { Text("App Behavior", style = MaterialTheme.typography.titleLarge) }
        item {
            val autoNewSearchStr by viewModel.autoNewSearch.collectAsState()
            val autoNewSearch = autoNewSearchStr.toBooleanStrictOrNull() ?: false
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Auto New Search", style = MaterialTheme.typography.titleMedium)
                    Text("Automatically clear chat and start a new search when submitting", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                Switch(checked = autoNewSearch, onCheckedChange = { viewModel.saveSetting("AUTO_NEW_SEARCH", it.toString()) })
            }
        }
        item {
            val enterToSendStr by viewModel.enterToSend.collectAsState()
            val enterToSend = enterToSendStr.toBooleanStrictOrNull() ?: false
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Enter to Send", style = MaterialTheme.typography.titleMedium)
                    Text("Pressing enter on the keyboard sends the message instead of new line", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                Switch(checked = enterToSend, onCheckedChange = { viewModel.saveSetting("ENTER_TO_SEND", it.toString()) })
            }
            Spacer(modifier = Modifier.height(16.dp))
        }
        item { Text("Display & Scaling", style = MaterialTheme.typography.titleLarge) }"""

text = text.replace(settings_start, settings_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

