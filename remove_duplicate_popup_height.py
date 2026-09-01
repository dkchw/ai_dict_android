import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

target = """            Text("Popup Height: ${(currentPopupHeight * 100).toInt()}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = currentPopupHeight,
                onValueChange = { popupHeight = it },
                onValueChangeFinished = { viewModel.saveSetting("POPUP_HEIGHT", currentPopupHeight.toString()) },
                valueRange = 0.3f..1.0f,
                steps = 13
            )"""

text = text.replace(target, "")

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

