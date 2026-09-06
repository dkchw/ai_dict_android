import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/NotesScreen.kt', 'r') as f:
    text = f.read()

target = """    var showDialog by remember { mutableStateOf(false) }"""
replacement = """    var showDialog by remember { mutableStateOf(false) }
    var searchQuery by remember { mutableStateOf("") }
    var isSearching by remember { mutableStateOf(false) }"""
text = text.replace(target, replacement)

target_row = """                IconButton(onClick = { selectionMode = true }) {
                    Icon(Icons.Default.Checklist, contentDescription = "Select")
                }
                IconButton(onClick = { 
                    currentNote = null
                    noteTitle = ""
                    noteContent = ""
                    showDialog = true 
                }) {
                    Icon(Icons.Default.Add, contentDescription = "Add Note")
                }
            }
        }"""
replacement_row = """                IconButton(onClick = { isSearching = !isSearching }) {
                    Icon(Icons.Default.Search, contentDescription = "Search")
                }
                IconButton(onClick = { selectionMode = true }) {
                    Icon(Icons.Default.Checklist, contentDescription = "Select")
                }
                IconButton(onClick = { 
                    currentNote = null
                    noteTitle = ""
                    noteContent = ""
                    showDialog = true 
                }) {
                    Icon(Icons.Default.Add, contentDescription = "Add Note")
                }
            }
        }
        
        if (isSearching) {
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                placeholder = { Text("Search notes...") },
                singleLine = true,
                trailingIcon = {
                    if (searchQuery.isNotEmpty()) {
                        IconButton(onClick = { searchQuery = "" }) {
                            Icon(Icons.Default.Clear, contentDescription = "Clear")
                        }
                    }
                }
            )
        }"""
text = text.replace(target_row, replacement_row)

target_list = """        LazyColumn(modifier = Modifier.weight(1f)) {
            items(notes) { note ->"""
replacement_list = """        val filteredNotes = if (searchQuery.isBlank()) notes else notes.filter { 
            it.title.contains(searchQuery, ignoreCase = true) || 
            it.content.contains(searchQuery, ignoreCase = true) 
        }
        
        LazyColumn(modifier = Modifier.weight(1f)) {
            items(filteredNotes) { note ->"""
text = text.replace(target_list, replacement_list)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/NotesScreen.kt', 'w') as f:
    f.write(text)

print("Added search to NotesScreen")
