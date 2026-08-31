import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

old_scaling = """        item {
            var uiScale by remember { mutableStateOf(viewModel.getSetting("UI_SCALE")?.toFloatOrNull() ?: 1.0f) }
            Text(text = "UI Scale: ${String.format("%.2f", uiScale)}", modifier = Modifier.padding(top = 8.dp))
            Slider(
                value = uiScale,
                onValueChange = { uiScale = it },
                onValueChangeFinished = { viewModel.saveSetting("UI_SCALE", uiScale.toString()) },
                valueRange = 0.5f..2.0f
            )
        }
        item {
            var textScale by remember { mutableStateOf(viewModel.getSetting("TEXT_SIZE_SCALE")?.toFloatOrNull() ?: 1.0f) }
            Text(text = "Text Size: ${String.format("%.2f", textScale)}", modifier = Modifier.padding(top = 8.dp))
            Slider(
                value = textScale,
                onValueChange = { textScale = it },
                onValueChangeFinished = { viewModel.saveSetting("TEXT_SIZE_SCALE", textScale.toString()) },
                valueRange = 0.5f..2.0f
            )
            Spacer(modifier = Modifier.height(16.dp))
        }"""

new_scaling = """        item {
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

text = text.replace(old_scaling, new_scaling)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

