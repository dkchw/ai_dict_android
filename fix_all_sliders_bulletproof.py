import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Replace Display & Scaling
target_display = re.compile(r'Text\("UI Scale".*?valueRange = 0\.5f\.\.2\.0f,\s*steps = 14\s*\)', re.MULTILINE | re.DOTALL)

replacement_display = """Text("UI Scale", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 16.dp, bottom = 4.dp))
            val uiScaleStr by viewModel.getSettingFlow("UI_SCALE", "1.0").collectAsState()
            var localUiScale by remember { mutableStateOf(1.0f) }
            var isDraggingUiScale by remember { mutableStateOf(false) }
            
            LaunchedEffect(uiScaleStr) {
                if (!isDraggingUiScale) {
                    localUiScale = uiScaleStr.toFloatOrNull() ?: 1.0f
                }
            }
            
            Text(text = "UI Scale: ${java.lang.String.format("%.2f", localUiScale)}", modifier = Modifier.padding(top = 8.dp))
            Slider(
                value = localUiScale,
                onValueChange = { 
                    isDraggingUiScale = true
                    localUiScale = it 
                },
                onValueChangeFinished = { 
                    isDraggingUiScale = false
                    val rounded = Math.round(localUiScale * 100) / 100f
                    viewModel.saveSetting("UI_SCALE", rounded.toString()) 
                },
                valueRange = 0.5f..2.0f
            )
            
            val textScaleStr by viewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
            var localTextScale by remember { mutableStateOf(1.0f) }
            var isDraggingTextScale by remember { mutableStateOf(false) }
            
            LaunchedEffect(textScaleStr) {
                if (!isDraggingTextScale) {
                    localTextScale = textScaleStr.toFloatOrNull() ?: 1.0f
                }
            }
            
            Text(text = "Text Size: ${java.lang.String.format("%.2f", localTextScale)}", modifier = Modifier.padding(top = 8.dp))
            Slider(
                value = localTextScale,
                onValueChange = { 
                    isDraggingTextScale = true
                    localTextScale = it 
                },
                onValueChangeFinished = { 
                    isDraggingTextScale = false
                    val rounded = Math.round(localTextScale * 100) / 100f
                    viewModel.saveSetting("TEXT_SIZE_SCALE", rounded.toString()) 
                },
                valueRange = 0.5f..2.0f
            )"""

text = target_display.sub(replacement_display, text)

# Replace Floating UI & Bubble Sizing
target_floating = re.compile(r'val bubbleSizeStr by viewModel\.getSettingFlow\("BUBBLE_SIZE", "160"\)\.collectAsState\(\).*?valueRange = 0\.3f\.\.1\.0f,\s*steps = 13\s*\)', re.MULTILINE | re.DOTALL)

replacement_floating = """val bubbleSizeStr by viewModel.getSettingFlow("BUBBLE_SIZE", "160").collectAsState()
            val popupWidthStr by viewModel.getSettingFlow("POPUP_WIDTH", "0.95").collectAsState()
            val popupHeightStr by viewModel.getSettingFlow("POPUP_HEIGHT", "0.90").collectAsState()
            
            var localBubbleSize by remember { mutableStateOf(160f) }
            var isDraggingBubble by remember { mutableStateOf(false) }
            LaunchedEffect(bubbleSizeStr) {
                if (!isDraggingBubble) localBubbleSize = bubbleSizeStr.toFloatOrNull() ?: 160f
            }
            
            var localPopupWidth by remember { mutableStateOf(0.95f) }
            var isDraggingWidth by remember { mutableStateOf(false) }
            LaunchedEffect(popupWidthStr) {
                if (!isDraggingWidth) localPopupWidth = popupWidthStr.toFloatOrNull() ?: 0.95f
            }
            
            var localPopupHeight by remember { mutableStateOf(0.90f) }
            var isDraggingHeight by remember { mutableStateOf(false) }
            LaunchedEffect(popupHeightStr) {
                if (!isDraggingHeight) localPopupHeight = popupHeightStr.toFloatOrNull() ?: 0.90f
            }

            Text("Bubble Size: ${Math.round(localBubbleSize)}px", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = localBubbleSize,
                onValueChange = { 
                    isDraggingBubble = true
                    localBubbleSize = it 
                },
                onValueChangeFinished = { 
                    isDraggingBubble = false
                    val rounded = Math.round(localBubbleSize).toString()
                    viewModel.saveSetting("BUBBLE_SIZE", rounded) 
                },
                valueRange = 80f..300f
            )

            Text("Popup Width: ${Math.round(localPopupWidth * 100)}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = localPopupWidth,
                onValueChange = { 
                    isDraggingWidth = true
                    localPopupWidth = it 
                },
                onValueChangeFinished = { 
                    isDraggingWidth = false
                    val rounded = Math.round(localPopupWidth * 100) / 100f
                    viewModel.saveSetting("POPUP_WIDTH", rounded.toString()) 
                },
                valueRange = 0.3f..1.0f
            )

            Text("Popup Height: ${Math.round(localPopupHeight * 100)}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = localPopupHeight,
                onValueChange = { 
                    isDraggingHeight = true
                    localPopupHeight = it 
                },
                onValueChangeFinished = { 
                    isDraggingHeight = false
                    val rounded = Math.round(localPopupHeight * 100) / 100f
                    viewModel.saveSetting("POPUP_HEIGHT", rounded.toString()) 
                },
                valueRange = 0.3f..1.0f
            )"""

text = target_floating.sub(replacement_floating, text)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

