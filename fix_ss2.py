import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Replace the closing brace of LazyColumn with our item and the closing brace
old_lazycolumn_end = """            }
        }
    }

    if (showProfileDialog) {"""

new_lazycolumn_end = """            }
        }

        item { Spacer(Modifier.height(32.dp)) }
        item {
            val context = androidx.compose.ui.platform.LocalContext.current
            Button(
                onClick = { com.aidict.app.utils.AutoUpdater(context).checkForUpdates() },
                modifier = Modifier.fillMaxWidth()
            ) { Text("Check for Updates") }
        }
    }

    if (showProfileDialog) {"""

text = text.replace(old_lazycolumn_end, new_lazycolumn_end)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

