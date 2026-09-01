import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

target = """@Composable
fun ExternalDictManager(viewModel: com.aidict.app.ui.viewmodels.SettingsViewModel) {
    val externalDictsStr by viewModel.getSettingFlow("EXTERNAL_DICTS", "Cambridge|https://dictionary.cambridge.org/dictionary/english/%s").collectAsState()
    
    val dicts = remember(externalDictsStr) {
        if (externalDictsStr.isBlank()) emptyList()
        else externalDictsStr.split(",").mapNotNull { 
            val parts = it.split("|")
            if (parts.size >= 2) parts[0] to parts[1] else null
        }
    }

    var showDialog by remember { mutableStateOf(false) }

    if (showDialog) {
        var newName by remember { mutableStateOf("") }
        var newUrl by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { showDialog = false },
            title = { Text("Add External Dictionary") },
            text = {
                Column {
                    Text("Use %s for the search word placeholder.", style = MaterialTheme.typography.bodySmall)
                    Spacer(modifier = Modifier.height(8.dp))
                    OutlinedTextField(
                        value = newName,
                        onValueChange = { newName = it },
                        label = { Text("Dictionary Name") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    OutlinedTextField(
                        value = newUrl,
                        onValueChange = { newUrl = it },
                        label = { Text("URL (e.g. https://.../%s)") },
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        if (newName.isNotBlank() && newUrl.contains("%s")) {
                            val newList = dicts + (newName to newUrl)
                            viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}" })
                            showDialog = false
                        }
                    },
                    enabled = newName.isNotBlank() && newUrl.contains("%s")
                ) { Text("Add") }
            },
            dismissButton = {
                TextButton(onClick = { showDialog = false }) { Text("Cancel") }
            }
        )
    }

    SettingsGroup("External Dictionaries") {
        Column(modifier = Modifier.fillMaxWidth().padding(8.dp)) {
            dicts.forEachIndexed { index, (name, url) ->
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(name, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        Text(url, style = MaterialTheme.typography.bodySmall, maxLines = 1)
                    }
                    IconButton(onClick = {
                        val newList = dicts.toMutableList().apply { removeAt(index) }
                        viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}" })
                    }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                    }
                }
                androidx.compose.material3.HorizontalDivider()
            }
            
            Button(
                onClick = { showDialog = true },
                modifier = Modifier.align(Alignment.End).padding(top = 8.dp)
            ) {
                Text("Add Link")
            }
        }
    }
}"""

replacement = """@Composable
fun ExternalDictManager(viewModel: com.aidict.app.ui.viewmodels.SettingsViewModel) {
    val externalDictsStr by viewModel.getSettingFlow("EXTERNAL_DICTS", "Cambridge|https://dictionary.cambridge.org/dictionary/english/{{str}}").collectAsState()
    
    val dicts = remember(externalDictsStr) {
        if (externalDictsStr.isBlank()) emptyList()
        else externalDictsStr.split(",").mapNotNull { 
            val parts = it.split("|")
            if (parts.size >= 2) Triple(parts[0], parts[1], parts.getOrNull(2) ?: "") else null
        }
    }

    var showDialog by remember { mutableStateOf(false) }

    if (showDialog) {
        var newName by remember { mutableStateOf("") }
        var newUrl by remember { mutableStateOf("") }
        var newIcon by remember { mutableStateOf("") }
        
        AlertDialog(
            onDismissRequest = { showDialog = false },
            title = { Text("Add External Dictionary") },
            text = {
                Column {
                    Text("Use {{str}} for the search word placeholder.", style = MaterialTheme.typography.bodySmall)
                    Spacer(modifier = Modifier.height(8.dp))
                    OutlinedTextField(
                        value = newName,
                        onValueChange = { newName = it },
                        label = { Text("Dictionary Name") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    OutlinedTextField(
                        value = newUrl,
                        onValueChange = { newUrl = it },
                        label = { Text("URL (e.g. https://.../{{str}})") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    OutlinedTextField(
                        value = newIcon,
                        onValueChange = { newIcon = it },
                        label = { Text("Icon URL (Optional)") },
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            },
            confirmButton = {
                val isValid = newName.isNotBlank() && (newUrl.contains("{{str}}") || newUrl.contains("%s"))
                Button(
                    onClick = {
                        if (isValid) {
                            val newList = dicts + Triple(newName, newUrl, newIcon)
                            viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}|${it.third}" })
                            showDialog = false
                        }
                    },
                    enabled = isValid
                ) { Text("Add") }
            },
            dismissButton = {
                TextButton(onClick = { showDialog = false }) { Text("Cancel") }
            }
        )
    }

    SettingsGroup("External Dictionaries") {
        Column(modifier = Modifier.fillMaxWidth().padding(8.dp)) {
            dicts.forEachIndexed { index, (name, url, icon) ->
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                    if (icon.isNotBlank()) {
                        coil.compose.AsyncImage(
                            model = icon,
                            contentDescription = name,
                            modifier = Modifier.size(24.dp).padding(end = 8.dp)
                        )
                    }
                    Column(modifier = Modifier.weight(1f)) {
                        Text(name, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        Text(url, style = MaterialTheme.typography.bodySmall, maxLines = 1)
                    }
                    IconButton(onClick = {
                        val newList = dicts.toMutableList().apply { removeAt(index) }
                        viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}|${it.third}" })
                    }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                    }
                }
                androidx.compose.material3.HorizontalDivider()
            }
            
            Button(
                onClick = { showDialog = true },
                modifier = Modifier.align(Alignment.End).padding(top = 8.dp)
            ) {
                Text("Add Link")
            }
        }
    }
}"""

if "val parts = it.split(\"|\")\n            if (parts.size >= 2) Triple" not in text:
    text = text.replace(target, replacement)
    with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
        f.write(text)

