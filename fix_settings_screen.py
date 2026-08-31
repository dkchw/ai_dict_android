import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# I will add a new section for Display & Scaling under Background Settings or above it.
old_bg_settings = """        item { Text("Background", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 16.dp, bottom = 8.dp)) }"""

new_scaling_settings = """        item { Text("Display & Scaling", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 16.dp, bottom = 8.dp)) }
        item {
            var uiScale by remember { mutableStateOf(viewModel.getSetting("UI_SCALE")?.toFloatOrNull() ?: 1.0f) }
            Text(text = "UI Scale: ${String.format("%.2f", uiScale)}")
            Slider(
                value = uiScale,
                onValueChange = { uiScale = it },
                onValueChangeFinished = { viewModel.saveSetting("UI_SCALE", uiScale.toString()) },
                valueRange = 0.5f..2.0f
            )
        }
        item {
            var textScale by remember { mutableStateOf(viewModel.getSetting("TEXT_SIZE_SCALE")?.toFloatOrNull() ?: 1.0f) }
            Text(text = "Text Size: ${String.format("%.2f", textScale)}")
            Slider(
                value = textScale,
                onValueChange = { textScale = it },
                onValueChangeFinished = { viewModel.saveSetting("TEXT_SIZE_SCALE", textScale.toString()) },
                valueRange = 0.5f..2.0f
            )
        }
        
        item { Text("Background", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 16.dp, bottom = 8.dp)) }"""

text = text.replace(old_bg_settings, new_scaling_settings)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

