import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Let's add it right above "External Dictionaries"

sliders_ui = """    SettingsGroup("Floating UI & Bubble Sizing") {
        Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp, vertical = 4.dp)) {
            val bubbleSizeStr by viewModel.getSettingFlow("BUBBLE_SIZE", "160").collectAsState()
            val popupWidthStr by viewModel.getSettingFlow("POPUP_WIDTH", "0.95").collectAsState()
            val popupHeightStr by viewModel.getSettingFlow("POPUP_HEIGHT", "0.90").collectAsState()
            
            var bubbleSize by remember(bubbleSizeStr) { mutableStateOf(bubbleSizeStr.toFloatOrNull() ?: 160f) }
            var popupWidth by remember(popupWidthStr) { mutableStateOf(popupWidthStr.toFloatOrNull() ?: 0.95f) }
            var popupHeight by remember(popupHeightStr) { mutableStateOf(popupHeightStr.toFloatOrNull() ?: 0.90f) }

            Text("Bubble Size: ${bubbleSize.toInt()}px", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = bubbleSize,
                onValueChange = { bubbleSize = it },
                onValueChangeFinished = { viewModel.saveSetting("BUBBLE_SIZE", bubbleSize.toInt().toString()) },
                valueRange = 80f..300f
            )

            Text("Popup Width: ${(popupWidth * 100).toInt()}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = popupWidth,
                onValueChange = { popupWidth = it },
                onValueChangeFinished = { viewModel.saveSetting("POPUP_WIDTH", popupWidth.toString()) },
                valueRange = 0.3f..1.0f
            )

            Text("Popup Height: ${(popupHeight * 100).toInt()}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = popupHeight,
                onValueChange = { popupHeight = it },
                onValueChangeFinished = { viewModel.saveSetting("POPUP_HEIGHT", popupHeight.toString()) },
                valueRange = 0.3f..1.0f
            )
        }
    }
    item { Spacer(Modifier.height(16.dp)) }
"""

if 'Floating UI & Bubble Sizing' not in text:
    text = text.replace('    SettingsGroup("External Dictionaries") {', sliders_ui + '    SettingsGroup("External Dictionaries") {')
    with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
        f.write(text)

