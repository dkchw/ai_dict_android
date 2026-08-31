import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# App Behavior
app_old = """        item { Text("App Behavior", style = MaterialTheme.typography.titleLarge) }
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
        }"""
app_new = """        item {
            SettingsGroup("App Behavior") {
                val autoNewSearchStr by viewModel.autoNewSearch.collectAsState()
                val autoNewSearch = autoNewSearchStr.toBooleanStrictOrNull() ?: false
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("Auto New Search", style = MaterialTheme.typography.titleMedium)
                        Text("Automatically clear chat and start a new search when submitting", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Switch(checked = autoNewSearch, onCheckedChange = { viewModel.saveSetting("AUTO_NEW_SEARCH", it.toString()) })
                }
                val enterToSendStr by viewModel.enterToSend.collectAsState()
                val enterToSend = enterToSendStr.toBooleanStrictOrNull() ?: false
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("Enter to Send", style = MaterialTheme.typography.titleMedium)
                        Text("Pressing enter on the keyboard sends the message instead of new line", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Switch(checked = enterToSend, onCheckedChange = { viewModel.saveSetting("ENTER_TO_SEND", it.toString()) })
                }
            }
        }"""
text = text.replace(app_old, app_new)

# Display & Scaling
disp_old = """        item { Text("Display & Scaling", style = MaterialTheme.typography.titleLarge) }
        item {
            val uiScaleStr by viewModel.getSettingFlow("UI_SCALE", "1.0").collectAsState()
            var uiScale by remember(uiScaleStr) { mutableStateOf(uiScaleStr.toFloatOrNull() ?: 1.0f) }
            Text(text = "UI Scale: ${java.lang.String.format("%.2f", uiScale)}", modifier = Modifier.padding(top = 8.dp))
            Slider(
                value = uiScale,
                onValueChange = { uiScale = it },
                onValueChangeFinished = { viewModel.saveSetting("UI_SCALE", uiScale.toString()) },
                valueRange = 0.5f..2.0f
            )
        }
        item {
            val textScaleStr by viewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
            var textScale by remember(textScaleStr) { mutableStateOf(textScaleStr.toFloatOrNull() ?: 1.0f) }
            Text(text = "Text Size: ${java.lang.String.format("%.2f", textScale)}", modifier = Modifier.padding(top = 8.dp))
            Slider(
                value = textScale,
                onValueChange = { textScale = it },
                onValueChangeFinished = { viewModel.saveSetting("TEXT_SIZE_SCALE", textScale.toString()) },
                valueRange = 0.5f..2.0f
            )
            Spacer(modifier = Modifier.height(16.dp))
        }"""
disp_new = """        item {
            SettingsGroup("Display & Scaling") {
                val uiScaleStr by viewModel.getSettingFlow("UI_SCALE", "1.0").collectAsState()
                var uiScale by remember(uiScaleStr) { mutableStateOf(uiScaleStr.toFloatOrNull() ?: 1.0f) }
                Text(text = "UI Scale: ${java.lang.String.format("%.2f", uiScale)}", modifier = Modifier.padding(top = 8.dp))
                Slider(
                    value = uiScale,
                    onValueChange = { uiScale = it },
                    onValueChangeFinished = { viewModel.saveSetting("UI_SCALE", uiScale.toString()) },
                    valueRange = 0.5f..2.0f
                )
                val textScaleStr by viewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
                var textScale by remember(textScaleStr) { mutableStateOf(textScaleStr.toFloatOrNull() ?: 1.0f) }
                Text(text = "Text Size: ${java.lang.String.format("%.2f", textScale)}", modifier = Modifier.padding(top = 8.dp))
                Slider(
                    value = textScale,
                    onValueChange = { textScale = it },
                    onValueChangeFinished = { viewModel.saveSetting("TEXT_SIZE_SCALE", textScale.toString()) },
                    valueRange = 0.5f..2.0f
                )
            }
        }"""
text = text.replace(disp_old, disp_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

