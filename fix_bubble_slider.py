import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

target = """                var localBubbleSize by remember { mutableStateOf(160f) }
                var isDraggingBubble by remember { mutableStateOf(false) }
                LaunchedEffect(bubbleSizeStr) {
                    if (!isDraggingBubble) localBubbleSize = bubbleSizeStr.toFloatOrNull() ?: 160f
                }"""
                
replacement = """                var localBubbleSizeStr by remember { mutableStateOf(bubbleSizeStr) }
                LaunchedEffect(bubbleSizeStr) {
                    localBubbleSizeStr = bubbleSizeStr
                }"""

text = text.replace(target, replacement)

target_2 = """                Text("Bubble Size: ${Math.round(localBubbleSize)}px", style = MaterialTheme.typography.bodyMedium)
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
                
replacement_2 = """                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
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

text = text.replace(target_2, replacement_2)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)
