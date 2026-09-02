import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

# Add Icon import
if "import androidx.compose.material.icons.automirrored.filled.ArrowForward" not in text:
    text = text.replace("import androidx.compose.material.icons.filled.Add", "import androidx.compose.material.icons.filled.Add\nimport androidx.compose.material.icons.automirrored.filled.ArrowForward")
if "import com.aidict.app.data.entities.Profile" not in text:
    text = text.replace("import com.aidict.app.data.entities.Word", "import com.aidict.app.data.entities.Word\nimport com.aidict.app.data.entities.Profile")

# Add state variables
state_vars = """    var showRenameWord by remember { mutableStateOf<com.aidict.app.data.entities.Word?>(null) }
    var showMoveToProfile by remember { mutableStateOf(false) }
    var moveTargetWord by remember { mutableStateOf<com.aidict.app.data.entities.Word?>(null) }"""

text = text.replace("    var showRenameWord by remember { mutableStateOf<com.aidict.app.data.entities.Word?>(null) }", state_vars)

# We need the profiles list! It's in appViewModel!
# val appState by appViewModel.uiState.collectAsState() is defined INSIDE listContent!
# Let's move it to the top level of HistoryScreen
text = text.replace("    val sessions by viewModel.sessions.collectAsState()", "    val appState by appViewModel.uiState.collectAsState()\n    val sessions by viewModel.sessions.collectAsState()")
text = text.replace("            val appState by appViewModel.uiState.collectAsState()\n", "")

# Now add the Move button in individual word row
# In `!isSelectionMode` block:
target_individual_buttons = """                                        IconButton(onClick = {
                                            wordNameInput = word.term
                                            showRenameWord = word
                                        }) {
                                            Icon(Icons.Default.Edit, contentDescription = "Rename", modifier = Modifier.size(20.dp))
                                        }
                                        IconButton(onClick = { viewModel.deleteWord(word) }) {"""

replacement_individual_buttons = """                                        IconButton(onClick = {
                                            wordNameInput = word.term
                                            showRenameWord = word
                                        }) {
                                            Icon(Icons.Default.Edit, contentDescription = "Rename", modifier = Modifier.size(20.dp))
                                        }
                                        IconButton(onClick = { moveTargetWord = word; showMoveToProfile = true }) {
                                            Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = "Move to Profile", modifier = Modifier.size(20.dp))
                                        }
                                        IconButton(onClick = { viewModel.deleteWord(word) }) {"""

text = text.replace(target_individual_buttons, replacement_individual_buttons)

# Also add it to the selection mode top bar
target_selection_buttons = """                    IconButton(onClick = {
                        viewModel.deleteSelectedSessions(selectedSessionIds)
                        viewModel.deleteSelectedWords(selectedWordIds)
                        isSelectionMode = false
                        selectedSessionIds = emptySet()
                        selectedWordIds = emptySet()
                    }) {
                        Icon(Icons.Default.Delete, contentDescription = "Delete Selected", tint = MaterialTheme.colorScheme.error)
                    }
                }"""

replacement_selection_buttons = """                    IconButton(onClick = { showMoveToProfile = true }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = "Move Selected to Profile", tint = MaterialTheme.colorScheme.primary)
                    }
                    IconButton(onClick = {
                        viewModel.deleteSelectedSessions(selectedSessionIds)
                        viewModel.deleteSelectedWords(selectedWordIds)
                        isSelectionMode = false
                        selectedSessionIds = emptySet()
                        selectedWordIds = emptySet()
                    }) {
                        Icon(Icons.Default.Delete, contentDescription = "Delete Selected", tint = MaterialTheme.colorScheme.error)
                    }
                }"""

text = text.replace(target_selection_buttons, replacement_selection_buttons)

# Finally add the Dialog to the very end of HistoryScreen
dialog_code = """
    if (showMoveToProfile) {
        var selectedProfileId by remember { mutableStateOf(appState.activeProfile?.id ?: 1) }
        AlertDialog(
            onDismissRequest = { showMoveToProfile = false; moveTargetWord = null },
            title = { Text("Move to Profile") },
            text = {
                Column {
                    Text("Select a profile to move the selected items to:")
                    Spacer(modifier = Modifier.height(8.dp))
                    appState.profiles.filter { it.id != (appState.activeProfile?.id ?: -1) }.forEach { profile ->
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { selectedProfileId = profile.id }.padding(8.dp)) {
                            RadioButton(selected = selectedProfileId == profile.id, onClick = { selectedProfileId = profile.id })
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(profile.name)
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    if (moveTargetWord != null) {
                        viewModel.moveWord(moveTargetWord!!, selectedProfileId)
                    } else if (isSelectionMode) {
                        viewModel.moveSelected(selectedSessionIds, selectedWordIds, selectedProfileId)
                        isSelectionMode = false
                        selectedSessionIds = emptySet()
                        selectedWordIds = emptySet()
                    }
                    showMoveToProfile = false
                    moveTargetWord = null
                }) { Text("Move") }
            },
            dismissButton = {
                TextButton(onClick = { showMoveToProfile = false; moveTargetWord = null }) { Text("Cancel") }
            }
        )
    }
}"""

# Replace the very last closing brace with dialog_code
text = text.rsplit('}', 1)
text = text[0] + dialog_code

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

print("Added move dialog and buttons to HistoryScreen")
