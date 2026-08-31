import re

files = [
    'android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt'
]

# 1. Action buttons: Remove Refresh (Retry without fallback). Rename Warning to Refresh.
old_buttons = r'IconButton\(onClick = \{ viewModel\.retryMessage\(msg, false, ".*?"\) \}, modifier = Modifier\.size\(32\.dp\)\) \{ Icon\(Icons\.Default\.Refresh, "Retry", modifier = Modifier\.size\(16\.dp\)\) \}\s*IconButton\(onClick = \{ viewModel\.retryMessage\(msg, true, ".*?"\) \}, modifier = Modifier\.size\(32\.dp\)\) \{ Icon\(Icons\.Default\.Warning, "Retry Fallback", modifier = Modifier\.size\(16\.dp\)\) \}'
def replace_buttons(match):
    # Just return the fallback button with Refresh icon
    mode_match = re.search(r'"(.*?)"', match.group(0))
    mode = mode_match.group(1) if mode_match else "dict"
    return f'IconButton(onClick = {{ viewModel.retryMessage(msg, true, "{mode}") }}, modifier = Modifier.size(32.dp)) {{ Icon(Icons.Default.Refresh, "Regenerate", modifier = Modifier.size(16.dp)) }}'

# 2. Loading UI: Replace CircularProgressIndicator with PulsingDots
old_loading1 = r'CircularProgressIndicator\(modifier = Modifier\.padding\(16\.dp\)\)'
new_loading1 = r'com.aidict.app.ui.components.PulsingDots(modifier = Modifier.fillMaxWidth().wrapContentWidth(Alignment.CenterHorizontally))'

old_loading2 = r'CircularProgressIndicator\(modifier = Modifier\.align\(androidx\.compose\.ui\.Alignment\.Center\)\)'
new_loading2 = r'com.aidict.app.ui.components.PulsingDots(modifier = Modifier.align(androidx.compose.ui.Alignment.Center))'


# 3. Edit title: 
# Currently: Text(text = word.term, style = MaterialTheme.typography.headlineMedium)
# We want to replace it with an inline editor.
# We also need to add state variables at the top of the composable.
# But adding state variables inside `state.word?.let` is fine, we just use `var isEditingTitle...`

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace buttons
    content = re.sub(old_buttons, replace_buttons, content)
    
    # Replace loading
    content = re.sub(old_loading1, new_loading1, content)
    content = re.sub(old_loading2, new_loading2, content)
    
    # Replace title text
    if 'Text(text = word.term, style = MaterialTheme.typography.headlineMedium)' in content:
        title_repl = """
                var isEditingTitle by remember { mutableStateOf(false) }
                var titleInput by remember { mutableStateOf(word.term) }
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                    if (isEditingTitle) {
                        OutlinedTextField(
                            value = titleInput,
                            onValueChange = { titleInput = it },
                            modifier = Modifier.weight(1f),
                            singleLine = true
                        )
                        IconButton(onClick = {
                            viewModel.renameWord(word, titleInput, word.mode)
                            isEditingTitle = false
                        }) {
                            Icon(Icons.Default.Check, "Save")
                        }
                    } else {
                        Text(text = word.term, style = MaterialTheme.typography.headlineMedium, modifier = Modifier.weight(1f))
                        IconButton(onClick = { isEditingTitle = true; titleInput = word.term }) {
                            Icon(Icons.Default.Edit, "Edit Title")
                        }
                    }
                }"""
        content = content.replace('Text(text = word.term, style = MaterialTheme.typography.headlineMedium)', title_repl.strip())

    if 'Text(text = word.term, style = MaterialTheme.typography.headlineSmall)' in content:
        title_repl = """
                var isEditingTitle by remember { mutableStateOf(false) }
                var titleInput by remember { mutableStateOf(word.term) }
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                    if (isEditingTitle) {
                        OutlinedTextField(
                            value = titleInput,
                            onValueChange = { titleInput = it },
                            modifier = Modifier.weight(1f),
                            singleLine = true
                        )
                        IconButton(onClick = {
                            viewModel.renameWord(word, titleInput, word.mode)
                            isEditingTitle = false
                        }) {
                            Icon(Icons.Default.Check, "Save")
                        }
                    } else {
                        Text(text = word.term, style = MaterialTheme.typography.headlineSmall, modifier = Modifier.weight(1f))
                        IconButton(onClick = { isEditingTitle = true; titleInput = word.term }) {
                            Icon(Icons.Default.Edit, "Edit Title")
                        }
                    }
                }"""
        content = content.replace('Text(text = word.term, style = MaterialTheme.typography.headlineSmall)', title_repl.strip())
        
    with open(file_path, 'w') as f:
        f.write(content)

