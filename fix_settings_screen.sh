cat << 'INNER' >> android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt

@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun MultiSelectSearchableDropdown(
    label: String,
    currentCsv: String,
    options: List<String>,
    onCsvChange: (String) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    var searchText by remember { mutableStateOf("") }
    
    val selectedItems = currentCsv.split(",").map { it.trim() }.filter { it.isNotBlank() }

    Column(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = { expanded = !expanded }
        ) {
            OutlinedTextField(
                value = searchText,
                onValueChange = { searchText = it; expanded = true },
                label = { Text(label) },
                modifier = Modifier.menuAnchor().fillMaxWidth(),
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                colors = ExposedDropdownMenuDefaults.outlinedTextFieldColors()
            )
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                val filtered = options.filter { it.contains(searchText, ignoreCase = true) }.take(10)
                filtered.forEach { option ->
                    DropdownMenuItem(
                        text = { Text(option) },
                        onClick = {
                            val newItems = if (selectedItems.contains(option)) {
                                selectedItems - option
                            } else {
                                selectedItems + option
                            }
                            onCsvChange(newItems.joinToString(", "))
                            searchText = ""
                            expanded = false
                        }
                    )
                }
            }
        }
        
        // Display selected items as chips
        @OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
        androidx.compose.foundation.layout.FlowRow(modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) {
            selectedItems.forEach { item ->
                InputChip(
                    selected = true,
                    onClick = {
                        onCsvChange((selectedItems - item).joinToString(", "))
                    },
                    label = { Text(com.aidict.app.utils.LanguageManager.getDisplayFlag(item)) },
                    trailingIcon = { Icon(Icons.Default.Delete, contentDescription = "Remove", modifier = Modifier.size(16.dp)) },
                    modifier = Modifier.padding(end = 4.dp, bottom = 4.dp)
                )
            }
        }
    }
}
INNER
