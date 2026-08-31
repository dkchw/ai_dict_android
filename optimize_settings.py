import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# 1. Group the Prompts
prompts_old = """        item { Text("Prompts", style = MaterialTheme.typography.titleLarge) }
        
        item {
            OutlinedTextField(
                value = dictPrompt,
                onValueChange = { viewModel.saveSetting("DICT_PROMPT", it) },
                label = { Text("Dict Prompt") },
                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                minLines = 3
            )
        }
        item { Spacer(Modifier.height(16.dp)) }
        item {
            OutlinedTextField(
                value = comparePrompt,
                onValueChange = { viewModel.saveSetting("COMPARE_PROMPT", it) },
                label = { Text("Compare Prompt") },
                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                minLines = 3
            )
        }
        
        item {
            OutlinedTextField(
                value = explainPrompt,
                onValueChange = { viewModel.saveSetting("EXPLAIN_PROMPT", it) },
                label = { Text("Explain Prompt") },
                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                minLines = 3
            )
        }
        
        item {
            OutlinedTextField(
                value = translatePrompt,
                onValueChange = { viewModel.saveSetting("TRANSLATE_PROMPT", it) },
                label = { Text("Translate Prompt") },
                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                minLines = 3
            )
        }"""

prompts_new = """        item {
            Column {
                Text("Prompts", style = MaterialTheme.typography.titleLarge)
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

# 2. Group Models
models_old = """        item { SearchableModelDropdown("Dict Model", dictModel, availableModels) { viewModel.saveSetting("DICT_MODEL", it) } }
        item { SearchableModelDropdown("Compare Model", compareModel, availableModels) { viewModel.saveSetting("COMPARE_MODEL", it) } }
        item { SearchableModelDropdown("Explain Model", explainModel, availableModels) { viewModel.saveSetting("EXPLAIN_MODEL", it) } }
        item { SearchableModelDropdown("Translate Model", translateModel, availableModels) { viewModel.saveSetting("TRANSLATE_MODEL", it) } }
        
        item { SearchableModelDropdown("Fallback Model", fallbackModels, availableModels) { viewModel.saveSetting("FALLBACK_MODELS", it) } }
        item { SearchableModelDropdown("Chat Model", chatModel, availableModels) { viewModel.saveSetting("CHAT_MODEL", it) } }"""

models_new = """        item {
            Column {
                SearchableModelDropdown("Dict Model", dictModel, availableModels) { viewModel.saveSetting("DICT_MODEL", it) }
                SearchableModelDropdown("Compare Model", compareModel, availableModels) { viewModel.saveSetting("COMPARE_MODEL", it) }
                SearchableModelDropdown("Explain Model", explainModel, availableModels) { viewModel.saveSetting("EXPLAIN_MODEL", it) }
                SearchableModelDropdown("Translate Model", translateModel, availableModels) { viewModel.saveSetting("TRANSLATE_MODEL", it) }
                SearchableModelDropdown("Fallback Model", fallbackModels, availableModels) { viewModel.saveSetting("FALLBACK_MODELS", it) }
                SearchableModelDropdown("Chat Model", chatModel, availableModels) { viewModel.saveSetting("CHAT_MODEL", it) }
            }
        }"""
        
text = text.replace(models_old, models_new)

# 3. Add Key to items(profiles)
profiles_old = "items(profiles.sortedBy { it.rank }) { profile ->"
profiles_new = "items(profiles.sortedBy { it.rank }, key = { it.id }) { profile ->"
text = text.replace(profiles_old, profiles_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)
    
