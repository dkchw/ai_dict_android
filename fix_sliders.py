import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Replace the sliders implementation

target = """            var bubbleSize by remember(bubbleSizeStr) { mutableStateOf(bubbleSizeStr.toFloatOrNull() ?: 160f) }
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
            )"""

replacement = """            var bubbleSize by remember { mutableStateOf<Float?>(null) }
            var popupWidth by remember { mutableStateOf<Float?>(null) }
            var popupHeight by remember { mutableStateOf<Float?>(null) }
            
            val currentBubbleSize = bubbleSize ?: (bubbleSizeStr.toFloatOrNull() ?: 160f)
            val currentPopupWidth = popupWidth ?: (popupWidthStr.toFloatOrNull() ?: 0.95f)
            val currentPopupHeight = popupHeight ?: (popupHeightStr.toFloatOrNull() ?: 0.90f)

            Text("Bubble Size: ${currentBubbleSize.toInt()}px", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = currentBubbleSize,
                onValueChange = { bubbleSize = it },
                onValueChangeFinished = { viewModel.saveSetting("BUBBLE_SIZE", currentBubbleSize.toInt().toString()) },
                valueRange = 80f..320f,
                steps = 23
            )

            Text("Popup Width: ${(currentPopupWidth * 100).toInt()}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = currentPopupWidth,
                onValueChange = { popupWidth = it },
                onValueChangeFinished = { viewModel.saveSetting("POPUP_WIDTH", currentPopupWidth.toString()) },
                valueRange = 0.3f..1.0f,
                steps = 13
            )

            Text("Popup Height: ${(currentPopupHeight * 100).toInt()}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = currentPopupHeight,
                onValueChange = { popupHeight = it },
                onValueChangeFinished = { viewModel.saveSetting("POPUP_HEIGHT", currentPopupHeight.toString()) },
                valueRange = 0.3f..1.0f,
                steps = 13
            )"""

if "steps = 23" not in text:
    text = text.replace(target, replacement)
    with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
        f.write(text)

