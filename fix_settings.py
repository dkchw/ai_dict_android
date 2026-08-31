import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Add to state collection
insert_states = text.find('val dictPrompt by viewModel.dictPrompt.collectAsState()')
new_state = 'val externalLinkTemplate by viewModel.externalLinkTemplate.collectAsState()\n            '
text = text[:insert_states] + new_state + text[insert_states:]

# Add to UI
ui_code = """
        item { Spacer(Modifier.height(16.dp)) }
        item { Text("External Link", style = MaterialTheme.typography.titleLarge) }
        item {
            OutlinedTextField(
                value = externalLinkTemplate, 
                onValueChange = { viewModel.saveSetting("EXTERNAL_LINK", it) }, 
                label = { Text("External Link Template (use {word})") }, 
                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), 
                singleLine = true
            )
        }
"""
insert_ui = text.find('item { Spacer(Modifier.height(16.dp)) }\n        item { Text("Prompts", style = MaterialTheme.typography.titleLarge) }')
text = text[:insert_ui] + ui_code + '\n        ' + text[insert_ui:]

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

