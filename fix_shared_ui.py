import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

text = text.replace('onClear: (() -> Unit)? = null,', 'onClear: (() -> Unit)? = null,\n    onExternalLink: (() -> Unit)? = null,')
text = text.replace('import androidx.compose.material.icons.filled.SwapHoriz', 'import androidx.compose.material.icons.filled.SwapHoriz\nimport androidx.compose.material.icons.filled.Language')

button_code = """                if (onExternalLink != null) {
                    IconButton(
                        onClick = onExternalLink, 
                        modifier = Modifier
                            .padding(bottom = 8.dp, end = 8.dp)
                            .background(MaterialTheme.colorScheme.tertiaryContainer, CircleShape)
                    ) {
                        Icon(Icons.Default.Language, contentDescription = "External Link", tint = MaterialTheme.colorScheme.onTertiaryContainer)
                    }
                }
"""

text = text.replace('OutlinedTextField(\n                    value = inputTerm,', button_code + '                OutlinedTextField(\n                    value = inputTerm,')

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

