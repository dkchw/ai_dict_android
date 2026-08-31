with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

update_item = """        item { Spacer(Modifier.height(16.dp)) }
        item {
            val context = androidx.compose.ui.platform.LocalContext.current
            Button(
                onClick = { com.aidict.app.utils.AutoUpdater(context).checkForUpdates() },
                modifier = Modifier.fillMaxWidth()
            ) { Text("Check for Updates") }
        }
    }
}"""
text = text.replace('    }\n}\n\n@OptIn(ExperimentalMaterial3Api::class)', update_item + '\n\n@OptIn(ExperimentalMaterial3Api::class)')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

