import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

target = """                ) { Text("Floating Bubble") }
            }
        }
        item { ExternalDictManager(viewModel) }"""

replacement = """                ) { Text("Floating Bubble") }
            }
            val packageInfo = context.packageManager.getPackageInfo(context.packageName, 0)
            val versionName = packageInfo.versionName
            Text(
                "Version: $versionName", 
                style = MaterialTheme.typography.bodySmall, 
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f),
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), 
                textAlign = androidx.compose.ui.text.style.TextAlign.Center
            )
        }
        item { ExternalDictManager(viewModel) }"""

text = text.replace(target, replacement)
text = text.replace('import androidx.compose.ui.Alignment', 'import androidx.compose.ui.Alignment\nimport androidx.compose.ui.text.style.TextAlign')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

