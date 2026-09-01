import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

old_button = """        item {
            val context = androidx.compose.ui.platform.LocalContext.current
            Button(
                onClick = { com.aidict.app.utils.AutoUpdater(context).checkForUpdates() },
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.tertiary)
            ) { Text("Check for Updates") }
        }"""

new_button = """        item {
            val context = androidx.compose.ui.platform.LocalContext.current
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = { com.aidict.app.utils.AutoUpdater(context).checkForUpdates() },
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.tertiary)
                ) { Text("Check Updates") }
                
                Button(
                    onClick = {
                        if (!android.provider.Settings.canDrawOverlays(context)) {
                            val intent = android.content.Intent(android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION, android.net.Uri.parse("package:${context.packageName}"))
                            context.startActivity(intent)
                        } else {
                            val intent = android.content.Intent(context, com.aidict.app.FloatingBubbleService::class.java)
                            context.startService(intent)
                            android.widget.Toast.makeText(context, "Floating Bubble Started", android.widget.Toast.LENGTH_SHORT).show()
                        }
                    },
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                ) { Text("Floating Bubble") }
            }
        }"""

text = text.replace(old_button, new_button)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

