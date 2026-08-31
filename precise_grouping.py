import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Models
# Models has `Row ... { Text("Models" ... Button(onClick = { viewModel.refreshModels() }) ... }`
# followed by `Column { SearchableModelDropdown ... }`
models_old = """        item { Spacer(Modifier.height(16.dp)) }
        item { Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Models", style = MaterialTheme.typography.titleLarge); Button(onClick = { viewModel.refreshModels() }) { Icon(Icons.Default.Refresh, contentDescription = "Refresh Models", modifier = Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Refresh") } } }

        item {
            Column {
                SearchableModelDropdown("Dict Model", dictModel, availableModels) { viewModel.saveSetting("DICT_MODEL", it) }
                SearchableModelDropdown("Compare Model", compareModel, availableModels) { viewModel.saveSetting("COMPARE_MODEL", it) }
                SearchableModelDropdown("Explain Model", explainModel, availableModels) { viewModel.saveSetting("EXPLAIN_MODEL", it) }
                SearchableModelDropdown("Translate Model", translateModel, availableModels) { viewModel.saveSetting("TRANSLATE_MODEL", it) }
                SearchableModelDropdown("Fallback Model", fallbackModels, availableModels) { viewModel.saveSetting("FALLBACK_MODELS", it) }
                SearchableModelDropdown("Chat Model", chatModel, availableModels) { viewModel.saveSetting("CHAT_MODEL", it) }
            }
        }"""
models_new = """        item { Spacer(Modifier.height(16.dp)) }
        item {
            SettingsGroup("Models") {
                Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.End) {
                    Button(onClick = { viewModel.refreshModels() }) { Icon(Icons.Default.Refresh, contentDescription = "Refresh Models", modifier = Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Refresh") }
                }
                SearchableModelDropdown("Dict Model", dictModel, availableModels) { viewModel.saveSetting("DICT_MODEL", it) }
                SearchableModelDropdown("Compare Model", compareModel, availableModels) { viewModel.saveSetting("COMPARE_MODEL", it) }
                SearchableModelDropdown("Explain Model", explainModel, availableModels) { viewModel.saveSetting("EXPLAIN_MODEL", it) }
                SearchableModelDropdown("Translate Model", translateModel, availableModels) { viewModel.saveSetting("TRANSLATE_MODEL", it) }
                SearchableModelDropdown("Fallback Model", fallbackModels, availableModels) { viewModel.saveSetting("FALLBACK_MODELS", it) }
                SearchableModelDropdown("Chat Model", chatModel, availableModels) { viewModel.saveSetting("CHAT_MODEL", it) }
            }
        }"""
text = text.replace(models_old, models_new)


# Prompts
prompts_old = """        item { Spacer(Modifier.height(16.dp)) }
        item { Text("Prompts", style = MaterialTheme.typography.titleLarge) }
        
        item {
            Column {
                OutlinedTextField(
                    value = dictPrompt,
                    onValueChange = { viewModel.saveSetting("DICT_PROMPT", it) },
                    label = { Text("Dict Prompt") },
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                    minLines = 3
                )
                Spacer(Modifier.height(16.dp))
                OutlinedTextField(
                    value = comparePrompt,
                    onValueChange = { viewModel.saveSetting("COMPARE_PROMPT", it) },
                    label = { Text("Compare Prompt") },
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                    minLines = 3
                )
                OutlinedTextField(
                    value = explainPrompt,
                    onValueChange = { viewModel.saveSetting("EXPLAIN_PROMPT", it) },
                    label = { Text("Explain Prompt") },
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                    minLines = 3
                )
                OutlinedTextField(
                    value = translatePrompt,
                    onValueChange = { viewModel.saveSetting("TRANSLATE_PROMPT", it) },
                    label = { Text("Translate Prompt") },
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                    minLines = 3
                )
            }
        }"""
prompts_new = """        item { Spacer(Modifier.height(16.dp)) }
        item {
            SettingsGroup("Prompts") {
                OutlinedTextField(
                    value = dictPrompt,
                    onValueChange = { viewModel.saveSetting("DICT_PROMPT", it) },
                    label = { Text("Dict Prompt") },
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                    minLines = 3
                )
                Spacer(Modifier.height(16.dp))
                OutlinedTextField(
                    value = comparePrompt,
                    onValueChange = { viewModel.saveSetting("COMPARE_PROMPT", it) },
                    label = { Text("Compare Prompt") },
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                    minLines = 3
                )
                OutlinedTextField(
                    value = explainPrompt,
                    onValueChange = { viewModel.saveSetting("EXPLAIN_PROMPT", it) },
                    label = { Text("Explain Prompt") },
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                    minLines = 3
                )
                OutlinedTextField(
                    value = translatePrompt,
                    onValueChange = { viewModel.saveSetting("TRANSLATE_PROMPT", it) },
                    label = { Text("Translate Prompt") },
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                    minLines = 3
                )
            }
        }"""
text = text.replace(prompts_old, prompts_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

