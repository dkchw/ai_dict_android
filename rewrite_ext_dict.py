import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# We can regex match the entire `fun ExternalDictManager` to the end of the file
pattern = re.compile(r'@Composable\nfun ExternalDictManager.*$', re.MULTILINE | re.DOTALL)

new_func = """@Composable
fun ExternalDictManager(viewModel: com.aidict.app.ui.viewmodels.SettingsViewModel) {
    val externalDictsStr by viewModel.getSettingFlow("EXTERNAL_DICTS", "Cambridge|https://dictionary.cambridge.org/dictionary/english/{{str}}").collectAsState()
    
    val dicts = remember(externalDictsStr) {
        if (externalDictsStr.isBlank()) emptyList<Triple<String, String, String>>()
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

    SettingsGroup("Floating UI & Bubble Sizing") {
        Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp, vertical = 4.dp)) {
            val bubbleSizeStr by viewModel.getSettingFlow("BUBBLE_SIZE", "160").collectAsState()
            val popupWidthStr by viewModel.getSettingFlow("POPUP_WIDTH", "0.95").collectAsState()
            val popupHeightStr by viewModel.getSettingFlow("POPUP_HEIGHT", "0.90").collectAsState()
            
            var bubbleSize by remember { mutableStateOf<Float?>(null) }
            var popupWidth by remember { mutableStateOf<Float?>(null) }
            var popupHeight by remember { mutableStateOf<Float?>(null) }
            
            val currentBubbleSize = bubbleSize ?: (bubbleSizeStr.toFloatOrNull() ?: 160f)
            val currentPopupWidth = popupWidth ?: (popupWidthStr.toFloatOrNull() ?: 0.95f)
            val currentPopupHeight = popupHeight ?: (popupHeightStr.toFloatOrNull() ?: 0.90f)

            Text("Bubble Size: ${currentBubbleSize.toInt()}px", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = currentBubbleSize,
                onValueChange = { bubbleSize = it },
                onValueChangeFinished = { viewModel.saveSetting("BUBBLE_SIZE", currentBubbleSize.toInt().toString()) },
                valueRange = 80f..320f,
                steps = 23
            )

            Text("Popup Width: ${(currentPopupWidth * 100).toInt()}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = currentPopupWidth,
                onValueChange = { popupWidth = it },
                onValueChangeFinished = { viewModel.saveSetting("POPUP_WIDTH", currentPopupWidth.toString()) },
                valueRange = 0.3f..1.0f,
                steps = 13
            )

            Text("Popup Height: ${(currentPopupHeight * 100).toInt()}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = currentPopupHeight,
                onValueChange = { popupHeight = it },
                onValueChangeFinished = { viewModel.saveSetting("POPUP_HEIGHT", currentPopupHeight.toString()) },
                valueRange = 0.3f..1.0f,
                steps = 13
            )
        }
    }
    Spacer(Modifier.height(16.dp))
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
                    if (index > 0) {
                        IconButton(onClick = {
                            val newList = dicts.toMutableList()
                            val temp = newList[index]
                            newList[index] = newList[index - 1]
                            newList[index - 1] = temp
                            viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}|${it.third}" })
                        }, modifier = Modifier.size(32.dp)) {
                            Icon(androidx.compose.material.icons.Icons.Default.KeyboardArrowUp, contentDescription = "Up")
                        }
                    }
                    if (index < dicts.size - 1) {
                        IconButton(onClick = {
                            val newList = dicts.toMutableList()
                            val temp = newList[index]
                            newList[index] = newList[index + 1]
                            newList[index + 1] = temp
                            viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}|${it.third}" })
                        }, modifier = Modifier.size(32.dp)) {
                            Icon(androidx.compose.material.icons.Icons.Default.KeyboardArrowDown, contentDescription = "Down")
                        }
                    }
                    IconButton(onClick = {
                        val newList = dicts.toMutableList().apply { removeAt(index) }
                        viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}|${it.third}" })
                    }, modifier = Modifier.size(32.dp)) {
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

text = pattern.sub(new_func, text)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

