import re

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
    text = f.read()

# Remove UI_SCALE logic
target = """            val uiScaleStr by settingsViewModel.getSettingFlow("UI_SCALE", "1.0").collectAsState()
            val textScaleStr by settingsViewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
            val uiScale = uiScaleStr.toFloatOrNull() ?: 1.0f
            val textScale = textScaleStr.toFloatOrNull() ?: 1.0f
            
            val systemDensity = androidx.compose.ui.platform.LocalDensity.current
            val initialDensity = androidx.compose.runtime.remember { systemDensity }
            val newDensity = androidx.compose.ui.unit.Density(
                density = initialDensity.density * uiScale,
                fontScale = initialDensity.fontScale * textScale
            )"""

replacement = """            val textScaleStr by settingsViewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
            val textScale = textScaleStr.toFloatOrNull() ?: 1.0f
            
            val systemDensity = androidx.compose.ui.platform.LocalDensity.current
            val initialDensity = androidx.compose.runtime.remember { systemDensity }
            val newDensity = androidx.compose.ui.unit.Density(
                density = initialDensity.density,
                fontScale = initialDensity.fontScale * textScale
            )"""

text = text.replace(target, replacement)

# Remove uiScale from height constraint
target_2 = """                                .heightIn(max = (screenHeight * popupHeight) / uiScale)"""
replacement_2 = """                                .heightIn(max = screenHeight * popupHeight)"""

text = text.replace(target_2, replacement_2)

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
    f.write(text)
print("Fixed PopupActivity")
