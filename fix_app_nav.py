import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# I need to add ExternalDictButton composable definition outside AppNavigation, or inside. Let's put it outside.
external_dict_btn = """
@Composable
fun ExternalDictButton(viewModel: com.aidict.app.ui.viewmodels.SettingsViewModel, currentWord: String?) {
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
                    Icon(androidx.compose.material.icons.Icons.Default.Language, contentDescription = "External Dict")
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
}
"""

if "fun ExternalDictButton" not in text:
    text = text.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.runtime.collectAsState\nimport androidx.compose.runtime.getValue\nimport androidx.compose.runtime.setValue\nimport androidx.compose.runtime.mutableStateOf\nimport androidx.compose.runtime.remember")
    text += "\n" + external_dict_btn

# Insert into Row
target = """                        IconButton(onClick = { showManualDialog = true }) {"""

# We need to know current word. 
# Inside AppNavigation, `searchViewModel.dictState.collectAsState().value.word` is good?
# Actually `searchViewModel.searchInput` might have text, or the currently viewed word.
# Let's check how state is collected.
# AppNavigation has `val dictState by searchViewModel.dictState.collectAsState()`? Wait, `dictState` is only in DictScreen.
# I can just access `searchViewModel.dictState.value.word?.word` or similar. Wait, does `SearchViewModel` expose `dictState`? Let's check `SearchViewModel`.

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

