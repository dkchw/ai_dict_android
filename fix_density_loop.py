import re

def fix_density(filepath):
    with open(filepath, 'r') as f:
        text = f.read()
    
    target = """            val currentDensity = androidx.compose.ui.platform.LocalDensity.current
            val newDensity = androidx.compose.ui.unit.Density(
                density = currentDensity.density * uiScale,
                fontScale = currentDensity.fontScale * textScale
            )"""
            
    replacement = """            val currentDensity = androidx.compose.runtime.remember { androidx.compose.ui.platform.LocalDensity.current }
            val newDensity = androidx.compose.ui.unit.Density(
                density = currentDensity.density * uiScale,
                fontScale = currentDensity.fontScale * textScale
            )"""
            
    if target in text:
        text = text.replace(target, replacement)
        with open(filepath, 'w') as f:
            f.write(text)
        print(f"Fixed {filepath}")
    else:
        print(f"Target not found in {filepath}")

fix_density('android_app/app/src/main/java/com/aidict/app/MainActivity.kt')
fix_density('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt')

