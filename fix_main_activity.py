import re

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'r') as f:
    text = f.read()

old_material_theme = """            MaterialTheme(colorScheme = modifiedColorScheme) {
                Surface(color = MaterialTheme.colorScheme.background) {"""
new_material_theme = """            val uiScaleStr by settingsViewModel.getSettingFlow("UI_SCALE", "1.0").collectAsState()
            val textScaleStr by settingsViewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
            val uiScale = uiScaleStr.toFloatOrNull() ?: 1.0f
            val textScale = textScaleStr.toFloatOrNull() ?: 1.0f
            
            val currentDensity = androidx.compose.ui.platform.LocalDensity.current
            val newDensity = androidx.compose.ui.unit.Density(
                density = currentDensity.density * uiScale,
                fontScale = currentDensity.fontScale * textScale
            )

            MaterialTheme(colorScheme = modifiedColorScheme) {
                androidx.compose.runtime.CompositionLocalProvider(
                    androidx.compose.ui.platform.LocalDensity provides newDensity
                ) {
                    Surface(color = MaterialTheme.colorScheme.background) {"""
text = text.replace(old_material_theme, new_material_theme)

# Also fix the closing braces for CompositionLocalProvider
old_closing = """                    )
                }
            }
        }
    }
}"""
new_closing = """                    )
                    }
                }
            }
        }
    }
}"""
text = text.replace(old_closing, new_closing)

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'w') as f:
    f.write(text)

