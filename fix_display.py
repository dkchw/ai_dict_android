import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

target = re.compile(r'val uiScaleStr by viewModel\.getSettingFlow\("UI_SCALE".*?valueRange = 0\.5f\.\.2\.0f\n\s*\)', re.MULTILINE | re.DOTALL)

replacement = """val uiScaleStr by viewModel.getSettingFlow("UI_SCALE", "1.0").collectAsState()
                var localUiScale by remember { mutableStateOf(1.0f) }
                var isDraggingUiScale by remember { mutableStateOf(false) }
                
                LaunchedEffect(uiScaleStr) {
                    if (!isDraggingUiScale) localUiScale = uiScaleStr.toFloatOrNull() ?: 1.0f
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
                    if (!isDraggingTextScale) localTextScale = textScaleStr.toFloatOrNull() ?: 1.0f
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

text = target.sub(replacement, text)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

