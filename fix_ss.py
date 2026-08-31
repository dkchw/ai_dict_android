import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Remove the incorrectly injected code from the end of SettingsScreen
bad_code = """        item { Spacer(Modifier.height(16.dp)) }
        item {
            val context = androidx.compose.ui.platform.LocalContext.current
            Button(
                onClick = { com.aidict.app.utils.AutoUpdater(context).checkForUpdates() },
                modifier = Modifier.fillMaxWidth()
            ) { Text("Check for Updates") }
        }"""
text = text.replace(bad_code, "")

# Now find where LazyColumn actually ends and insert it correctly
# The LazyColumn ends right before `if (showAddDialog) {`
correct_injection = """        item { Spacer(Modifier.height(32.dp)) }
        item {
            val context = androidx.compose.ui.platform.LocalContext.current
            Button(
                onClick = { com.aidict.app.utils.AutoUpdater(context).checkForUpdates() },
                modifier = Modifier.fillMaxWidth()
            ) { Text("Check for Updates") }
        }
    }

    if (showAddDialog) {"""
text = text.replace('    }\n\n    if (showAddDialog) {', correct_injection)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)
