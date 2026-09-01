import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# 1. Remove UI Scale
ui_scale_block = """                val uiScaleStr by viewModel.getSettingFlow("UI_SCALE", "1.0").collectAsState()
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
                )"""

if ui_scale_block in text:
    text = text.replace(ui_scale_block, "")
    print("Removed UI Scale slider")
else:
    print("Could not find UI Scale block")

# 2. Convert Bubble Size to Number Input
bubble_block = """            val bubbleSizeStr by viewModel.getSettingFlow("BUBBLE_SIZE", "160").collectAsState()
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
            )"""

new_bubble_block = """            val bubbleSizeStr by viewModel.getSettingFlow("BUBBLE_SIZE", "160").collectAsState()
            val popupWidthStr by viewModel.getSettingFlow("POPUP_WIDTH", "0.95").collectAsState()
            val popupHeightStr by viewModel.getSettingFlow("POPUP_HEIGHT", "0.90").collectAsState()
            
            var localBubbleSizeStr by remember { mutableStateOf(bubbleSizeStr) }
            LaunchedEffect(bubbleSizeStr) {
                localBubbleSizeStr = bubbleSizeStr
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

            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                Text("Bubble Size (px):", style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1f))
                OutlinedTextField(
                    value = localBubbleSizeStr,
                    onValueChange = { localBubbleSizeStr = it.filter { char -> char.isDigit() } },
                    keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number),
                    modifier = Modifier.width(80.dp),
                    singleLine = true
                )
                Spacer(modifier = Modifier.width(8.dp))
                Button(onClick = {
                    val newSize = localBubbleSizeStr.toIntOrNull()?.coerceIn(50, 500) ?: 160
                    localBubbleSizeStr = newSize.toString()
                    viewModel.saveSetting("BUBBLE_SIZE", newSize.toString())
                    
                    val context = androidx.compose.ui.platform.LocalContext.current
                    val intent = android.content.Intent(context, com.aidict.app.FloatingBubbleService::class.java)
                    context.stopService(intent)
                    if (android.provider.Settings.canDrawOverlays(context)) {
                        context.startService(intent)
                        android.widget.Toast.makeText(context, "Bubble Restarted!", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }) {
                    Text("Apply")
                }
            }"""

if bubble_block in text:
    text = text.replace(bubble_block, new_bubble_block)
    print("Replaced Bubble Size slider with Number Input")
else:
    print("Could not find Bubble Size block")

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)
