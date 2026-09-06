import re

screens = ['CompareScreen.kt', 'TranslateScreen.kt', 'ExplainScreen.kt']

for screen in screens:
    path = f'android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}'
    with open(path, 'r') as f:
        text = f.read()

    # 1. Add state variables if not exist
    state_vars = "    var isChatSearching by remember { mutableStateOf(false) }\n    var chatSearchQuery by remember { mutableStateOf(\"\") }"
    if "isChatSearching" not in text:
        text = text.replace("    val context = LocalContext.current", "    val context = LocalContext.current\n" + state_vars)

    # 2. Modify the Row
    target_row = """        state.word?.let { word ->
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = androidx.compose.foundation.layout.Arrangement.End) {
                Text(
                    text = "Searches: ${word.searchCount} | Views: ${word.viewCount}","""

    replacement_row = """        state.word?.let { word ->
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "${word.term}",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.weight(1f)
                )
                IconButton(onClick = { isChatSearching = !isChatSearching }) {
                    Icon(androidx.compose.material.icons.Icons.Default.Search, contentDescription = "Search in Chat")
                }
                Text(
                    text = "Searches: ${word.searchCount} | Views: ${word.viewCount}","""

    text = text.replace(target_row, replacement_row)

    # 3. Add search bar below the let block
    search_bar_ui = """        }
        if (isChatSearching) {
            OutlinedTextField(
                value = chatSearchQuery,
                onValueChange = { chatSearchQuery = it },
                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                placeholder = { Text("Find in chat...") },
                singleLine = true,
                trailingIcon = {
                    if (chatSearchQuery.isNotEmpty()) {
                        IconButton(onClick = { chatSearchQuery = "" }) {
                            Icon(androidx.compose.material.icons.Icons.Default.Clear, contentDescription = "Clear Search")
                        }
                    }
                }
            )
        }
        LazyColumn(modifier = Modifier.weight(1f)) {"""
    
    text = text.replace("        }\n        LazyColumn(modifier = Modifier.weight(1f)) {", search_bar_ui)

    with open(path, 'w') as f:
        f.write(text)

print("Updated other screens")
