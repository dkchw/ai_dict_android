import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Extract the update button block
update_block_regex = r'\s*item \{ Spacer\(Modifier\.height\(32\.dp\)\) \}\n\s*item \{\n\s*val context = androidx\.compose\.ui\.platform\.LocalContext\.current\n\s*Button\(\n\s*onClick = \{ com\.aidict\.app\.utils\.AutoUpdater\(context\)\.checkForUpdates\(\) \},\n\s*modifier = Modifier\.fillMaxWidth\(\)\n\s*\) \{ Text\("Check for Updates"\) \}\n\s*\}\n'

update_match = re.search(update_block_regex, text)
if update_match:
    update_block = update_match.group(0)
    text = text.replace(update_block, '')
    
    # Inject it at the very top of LazyColumn
    lazy_start = "    LazyColumn(modifier = modifier.fillMaxSize().padding(16.dp)) {\n"
    new_top = lazy_start + """        item {
            val context = androidx.compose.ui.platform.LocalContext.current
            Button(
                onClick = { com.aidict.app.utils.AutoUpdater(context).checkForUpdates() },
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.tertiary)
            ) { Text("Check for Updates") }
        }\n"""
    
    text = text.replace(lazy_start, new_top)
else:
    print("Failed to find update block!")

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

