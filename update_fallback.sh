# Update SettingsViewModel.kt to set default for fallbackModels
sed -i 's/val fallbackModels = getSettingFlow("FALLBACK_MODELS", "")/val fallbackModels = getSettingFlow("FALLBACK_MODELS", "~deepseek\/deepseek-v4-flash-latest")/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt

# Update SettingsScreen.kt to use dropdown
sed -i 's/item { OutlinedTextField(value = fallbackModels, onValueChange = { viewModel.saveSetting("FALLBACK_MODELS", it) }, label = { Text("Fallback Models (Comma separated)") }, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) }/item { SearchableModelDropdown("Fallback Model", fallbackModels, availableModels) { viewModel.saveSetting("FALLBACK_MODELS", it) } }/' android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt
