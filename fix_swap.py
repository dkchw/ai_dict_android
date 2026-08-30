import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    content = f.read()

# Add import
if 'import androidx.compose.material.icons.filled.SwapHoriz' not in content:
    content = content.replace('import androidx.compose.material.icons.filled.Search', 'import androidx.compose.material.icons.filled.Search\nimport androidx.compose.material.icons.filled.SwapHoriz')

# Replace ArrowForward icon with SwapHoriz IconButton
old_icon_code = 'Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = "To", modifier = Modifier.padding(horizontal = 4.dp).size(14.dp))'
new_icon_code = """IconButton(
                        onClick = { 
                            onSourceLangChange(targetLang)
                            onTargetLangChange(sourceLang)
                        },
                        modifier = Modifier.padding(horizontal = 4.dp).size(24.dp)
                    ) {
                        Icon(Icons.Default.SwapHoriz, contentDescription = "Swap Languages", modifier = Modifier.size(16.dp))
                    }"""

content = content.replace(old_icon_code, new_icon_code)

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(content)
