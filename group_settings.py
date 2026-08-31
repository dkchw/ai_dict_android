import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# We need to wrap specific sections in SettingsGroup.
# The sections are: App Behavior, Display & Scaling, Backgrounds, Inspirational Quote, General, API Configuration, Models, Prompts.
# But wait, some are already grouped in Column { Text(...) ... }
# Let's replace those specifically using standard string replace.

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

display_old = """        item { Text("Display & Scaling", style = MaterialTheme.typography.titleLarge) }
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
            val textSizeScaleStr by viewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
            var textSizeScale by remember(textSizeScaleStr) { mutableStateOf(textSizeScaleStr.toFloatOrNull() ?: 1.0f) }
            Text(text = "Text Size: ${java.lang.String.format("%.2f", textSizeScale)}", modifier = Modifier.padding(top = 8.dp))
            Slider(
                value = textSizeScale,
                onValueChange = { textSizeScale = it },
                onValueChangeFinished = { viewModel.saveSetting("TEXT_SIZE_SCALE", textSizeScale.toString()) },
                valueRange = 0.5f..2.0f
            )
        }
        item { Spacer(modifier = Modifier.height(16.dp)) }"""

display_new = """        item {
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
                val textSizeScaleStr by viewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
                var textSizeScale by remember(textSizeScaleStr) { mutableStateOf(textSizeScaleStr.toFloatOrNull() ?: 1.0f) }
                Text(text = "Text Size: ${java.lang.String.format("%.2f", textSizeScale)}", modifier = Modifier.padding(top = 8.dp))
                Slider(
                    value = textSizeScale,
                    onValueChange = { textSizeScale = it },
                    onValueChangeFinished = { viewModel.saveSetting("TEXT_SIZE_SCALE", textSizeScale.toString()) },
                    valueRange = 0.5f..2.0f
                )
            }
        }"""
text = text.replace(display_old, display_new)

bg_old = '            Column {\n                Text("Backgrounds", style = MaterialTheme.typography.titleLarge)'
bg_new = '            SettingsGroup("Backgrounds") {'
text = text.replace(bg_old, bg_new)

quote_start = '        item { Text("Inspirational Quote", style = MaterialTheme.typography.titleLarge) }\n\n        item {'
quote_new = '        item { SettingsGroup("Inspirational Quote") {'
text = text.replace(quote_start, quote_new)
text = text.replace('                    }\n                }\n            }\n        }\n\n        item { Spacer(Modifier.height(16.dp)) }\n\n        item { Text("General", style = MaterialTheme.typography.titleLarge) }', '                    }\n                }\n            }\n        } } // end group\n\n        item { Text("General", style = MaterialTheme.typography.titleLarge) }')

gen_start = '        item { Text("General", style = MaterialTheme.typography.titleLarge) }\n\n        item {'
gen_new = '        item { SettingsGroup("General") {'
text = text.replace(gen_start, gen_new)
text = text.replace('        item { Spacer(Modifier.height(16.dp)) }\n        item { com.aidict.app.ui.components.MultiSelectSearchableDropdown', '        com.aidict.app.ui.components.MultiSelectSearchableDropdown')
text = text.replace('            )\n        }\n        item { Text("API Configuration", style = MaterialTheme.typography.titleLarge) }', '            )\n        } } // end general\n        item { Text("API Configuration", style = MaterialTheme.typography.titleLarge) }')
# MultiSelectSearchableDropdown was in its own item.
text = text.replace('        item { com.aidict.app.ui.components.MultiSelectSearchableDropdown(label = "Search to add Starred Languages", currentCsv = viewModel.starredLanguages.collectAsState().value, options = viewModel.allAvailableLanguages.collectAsState().value, onCsvChange = { viewModel.saveSetting("STARRED_LANGUAGES", it) }) }\n        item {\n        }\n        item { Text("API Configuration", style = MaterialTheme.typography.titleLarge) }', '        com.aidict.app.ui.components.MultiSelectSearchableDropdown(label = "Search to add Starred Languages", currentCsv = viewModel.starredLanguages.collectAsState().value, options = viewModel.allAvailableLanguages.collectAsState().value, onCsvChange = { viewModel.saveSetting("STARRED_LANGUAGES", it) })\n        } } // end general\n        item { Text("API Configuration", style = MaterialTheme.typography.titleLarge) }')

api_start = '        item { Text("API Configuration", style = MaterialTheme.typography.titleLarge) }\n        item {'
api_new = '        item { SettingsGroup("API Configuration") {'
text = text.replace(api_start, api_new)
text = text.replace('                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)\n            )\n        }\n        \n        item { Spacer(Modifier.height(16.dp)) }\n        item { Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Models", style = MaterialTheme.typography.titleLarge)', '                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)\n            )\n        } } // end api config\n        item { Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Models", style = MaterialTheme.typography.titleLarge)')


models_start = 'Text("Models", style = MaterialTheme.typography.titleLarge); Button(onClick = { viewModel.refreshModels() }) { Icon(Icons.Default.Refresh, contentDescription = "Refresh Models", modifier = Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Refresh") } } }\n\n        item {\n            Column {\n                SearchableModelDropdown'
models_new = 'Text("Models", style = MaterialTheme.typography.titleLarge); Button(onClick = { viewModel.refreshModels() }) { Icon(Icons.Default.Refresh, contentDescription = "Refresh Models", modifier = Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Refresh") } } }\n\n        item {\n            SettingsGroup("Models") {\n                SearchableModelDropdown'
text = text.replace(models_start, models_new)


prompts_start = '            Column {\n                Text("Prompts", style = MaterialTheme.typography.titleLarge)'
prompts_new = '            SettingsGroup("Prompts") {'
text = text.replace(prompts_start, prompts_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

