import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

target = """fun ExternalDictButton(viewModel: com.aidict.app.ui.viewmodels.SettingsViewModel, currentWord: String?) {
    val externalDictsStr by viewModel.getSettingFlow("EXTERNAL_DICTS", "Cambridge|https://dictionary.cambridge.org/dictionary/english/%s").collectAsState()
    val dicts = remember(externalDictsStr) {
        if (externalDictsStr.isBlank()) emptyList()
        else externalDictsStr.split(",").mapNotNull { 
            val parts = it.split("|")
            if (parts.size >= 2) parts[0] to parts[1] else null
        }
    }
    
    if (dicts.isNotEmpty()) {
        val context = androidx.compose.ui.platform.LocalContext.current
        var expanded by remember { mutableStateOf(false) }
        
        Box {
            androidx.compose.foundation.layout.Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically, modifier = Modifier.padding(end = 4.dp)) {
                IconButton(onClick = {
                    if (currentWord.isNullOrBlank()) {
                        android.widget.Toast.makeText(context, "Search a word first", android.widget.Toast.LENGTH_SHORT).show()
                        return@IconButton
                    }
                    val url = dicts.first().second.replace("%s", currentWord.trim())
                    val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(url))
                    context.startActivity(intent)
                }) {
                    Icon(androidx.compose.material.icons.Icons.Default.Search, contentDescription = "External Dict")
                }
                
                if (dicts.size > 1) {
                    IconButton(onClick = { expanded = true }, modifier = Modifier.size(24.dp)) {
                        Icon(androidx.compose.material.icons.Icons.Default.ArrowDropDown, contentDescription = "More")
                    }
                }
            }
            
            androidx.compose.material3.DropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                dicts.forEach { (name, urlTemplate) ->
                    androidx.compose.material3.DropdownMenuItem(
                        text = { Text(name) },
                        onClick = {
                            expanded = false
                            if (currentWord.isNullOrBlank()) {
                                android.widget.Toast.makeText(context, "Search a word first", android.widget.Toast.LENGTH_SHORT).show()
                            } else {
                                val url = urlTemplate.replace("%s", currentWord.trim())
                                val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(url))
                                context.startActivity(intent)
                            }
                        }
                    )
                }
            }
        }
    }
}"""

replacement = """fun ExternalDictButton(viewModel: com.aidict.app.ui.viewmodels.SettingsViewModel, currentWord: String?) {
    val externalDictsStr by viewModel.getSettingFlow("EXTERNAL_DICTS", "Cambridge|https://dictionary.cambridge.org/dictionary/english/{{str}}").collectAsState()
    val dicts = remember(externalDictsStr) {
        if (externalDictsStr.isBlank()) emptyList()
        else externalDictsStr.split(",").mapNotNull { 
            val parts = it.split("|")
            if (parts.size >= 2) Triple(parts[0], parts[1], parts.getOrNull(2) ?: "") else null
        }
    }
    
    if (dicts.isNotEmpty()) {
        val context = androidx.compose.ui.platform.LocalContext.current
        var expanded by remember { mutableStateOf(false) }
        
        Box {
            androidx.compose.foundation.layout.Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically, modifier = Modifier.padding(end = 4.dp)) {
                IconButton(onClick = {
                    if (currentWord.isNullOrBlank()) {
                        android.widget.Toast.makeText(context, "Search a word first", android.widget.Toast.LENGTH_SHORT).show()
                        return@IconButton
                    }
                    val urlTemplate = dicts.first().second
                    val url = urlTemplate.replace("{{str}}", currentWord.trim()).replace("%s", currentWord.trim())
                    val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(url))
                    context.startActivity(intent)
                }) {
                    val firstIcon = dicts.first().third
                    if (firstIcon.isNotBlank()) {
                        coil.compose.AsyncImage(
                            model = firstIcon,
                            contentDescription = "External Dict",
                            modifier = Modifier.size(24.dp)
                        )
                    } else {
                        Icon(androidx.compose.material.icons.Icons.Default.Search, contentDescription = "External Dict")
                    }
                }
                
                if (dicts.size > 1) {
                    IconButton(onClick = { expanded = true }, modifier = Modifier.size(24.dp)) {
                        Icon(androidx.compose.material.icons.Icons.Default.ArrowDropDown, contentDescription = "More")
                    }
                }
            }
            
            androidx.compose.material3.DropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                dicts.forEach { (name, urlTemplate, iconUrl) ->
                    androidx.compose.material3.DropdownMenuItem(
                        text = { Text(name) },
                        leadingIcon = if (iconUrl.isNotBlank()) {
                            { coil.compose.AsyncImage(model = iconUrl, contentDescription = name, modifier = Modifier.size(24.dp)) }
                        } else null,
                        onClick = {
                            expanded = false
                            if (currentWord.isNullOrBlank()) {
                                android.widget.Toast.makeText(context, "Search a word first", android.widget.Toast.LENGTH_SHORT).show()
                            } else {
                                val url = urlTemplate.replace("{{str}}", currentWord.trim()).replace("%s", currentWord.trim())
                                val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(url))
                                context.startActivity(intent)
                            }
                        }
                    )
                }
            }
        }
    }
}"""

if "val urlTemplate = dicts.first().second" not in text:
    text = text.replace(target, replacement)
    with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
        f.write(text)

