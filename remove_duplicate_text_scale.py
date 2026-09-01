import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

target = """                val textScaleStr by viewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
                var textScale by remember(textScaleStr) { mutableStateOf(textScaleStr.toFloatOrNull() ?: 1.0f) }
                Text(text = "Text Size: ${java.lang.String.format("%.2f", textScale)}", modifier = Modifier.padding(top = 8.dp))
                Slider(
                    value = textScale,
                    onValueChange = { textScale = it },
                    onValueChangeFinished = { viewModel.saveSetting("TEXT_SIZE_SCALE", textScale.toString()) },
                    valueRange = 0.5f..2.0f
                )"""

text = text.replace(target, "")

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

