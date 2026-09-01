import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Fix Display & Scaling
target_display = """    SettingsGroup("Display & Scaling") {
        Column(modifier = Modifier.fillMaxWidth().padding(8.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                Text("Dark Mode", modifier = Modifier.weight(1f))
                val isDark by viewModel.isDarkMode.collectAsState()
                Switch(checked = isDark, onCheckedChange = { viewModel.saveSetting("DARK_MODE", it.toString()) })
            }
            
            Text("App Theme", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 8.dp, bottom = 4.dp))
            val appTheme by viewModel.appTheme.collectAsState()
            val themes = listOf("light", "dark", "nord", "dracula", "tokyonight")
            themes.forEach { theme ->
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { viewModel.saveSetting("APP_THEME", theme) }.padding(vertical = 4.dp)) {
                    RadioButton(selected = appTheme == theme, onClick = { viewModel.saveSetting("APP_THEME", theme) })
                    Text(theme.replaceFirstChar { it.uppercase() })
                }
            }
            
            Text("UI Scale", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 16.dp, bottom = 4.dp))
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

replacement_display = """    SettingsGroup("Display & Scaling") {
        Column(modifier = Modifier.fillMaxWidth().padding(8.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                Text("Dark Mode", modifier = Modifier.weight(1f))
                val isDark by viewModel.isDarkMode.collectAsState()
                Switch(checked = isDark, onCheckedChange = { viewModel.saveSetting("DARK_MODE", it.toString()) })
            }
            
            Text("App Theme", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 8.dp, bottom = 4.dp))
            val appTheme by viewModel.appTheme.collectAsState()
            val themes = listOf("light", "dark", "nord", "dracula", "tokyonight")
            themes.forEach { theme ->
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { viewModel.saveSetting("APP_THEME", theme) }.padding(vertical = 4.dp)) {
                    RadioButton(selected = appTheme == theme, onClick = { viewModel.saveSetting("APP_THEME", theme) })
                    Text(theme.replaceFirstChar { it.uppercase() })
                }
            }
            
            Text("UI Scale", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 16.dp, bottom = 4.dp))
            val uiScaleStr by viewModel.getSettingFlow("UI_SCALE", "1.0").collectAsState()
            var uiScale by remember { mutableStateOf<Float?>(null) }
            val currentUiScale = uiScale ?: (uiScaleStr.toFloatOrNull() ?: 1.0f)
            
            Text(text = "UI Scale: ${java.lang.String.format("%.2f", currentUiScale)}", modifier = Modifier.padding(top = 8.dp))
            Slider(
                value = currentUiScale,
                onValueChange = { uiScale = it },
                onValueChangeFinished = { viewModel.saveSetting("UI_SCALE", currentUiScale.toString()) },
                valueRange = 0.5f..2.0f,
                steps = 14
            )
            
            val textScaleStr by viewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
            var textScale by remember { mutableStateOf<Float?>(null) }
            val currentTextScale = textScale ?: (textScaleStr.toFloatOrNull() ?: 1.0f)
            
            Text(text = "Text Size: ${java.lang.String.format("%.2f", currentTextScale)}", modifier = Modifier.padding(top = 8.dp))
            Slider(
                value = currentTextScale,
                onValueChange = { textScale = it },
                onValueChangeFinished = { viewModel.saveSetting("TEXT_SIZE_SCALE", currentTextScale.toString()) },
                valueRange = 0.5f..2.0f,
                steps = 14
            )
        }
    }"""

if 'var uiScale by remember { mutableStateOf<Float?>(null) }' not in text:
    text = text.replace(target_display, replacement_display)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

