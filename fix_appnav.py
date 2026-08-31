with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Fix alignment
old_title = """                title = { 
                    Column(modifier = Modifier.fillMaxWidth().padding(end = 8.dp), horizontalAlignment = Alignment.End) {
                        Text("AI Dict", style = MaterialTheme.typography.titleLarge)
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            Row(
                                verticalAlignment = Alignment.CenterVertically, 
                                modifier = Modifier.clickable { expanded = true }.padding(horizontal = 8.dp, vertical = 2.dp),
                                horizontalArrangement = Arrangement.End
                            ) {"""

new_title = """                title = { 
                    Column(modifier = Modifier.fillMaxWidth().padding(start = 8.dp), horizontalAlignment = Alignment.Start) {
                        Text("AI Dict", style = MaterialTheme.typography.titleLarge)
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            Row(
                                verticalAlignment = Alignment.CenterVertically, 
                                modifier = Modifier.clickable { expanded = true }.padding(vertical = 2.dp),
                                horizontalArrangement = Arrangement.Start
                            ) {"""
text = text.replace(old_title, new_title)

# Fix bottom bar onclick
old_onclick = """                            onClick = { currentMode = index },"""
new_onclick = """                            onClick = { 
                                if (currentMode != index) {
                                    currentMode = index
                                    searchViewModel.clearCurrentSearch()
                                }
                            },"""
text = text.replace(old_onclick, new_onclick)

# Remove LaunchedEffect
old_launched_effect = """                Screen.MAIN -> {
                    val pid = appState.activeProfile?.id ?: 1
                    LaunchedEffect(currentMode) {
                        searchViewModel.clearCurrentSearch()
                    }"""
new_launched_effect = """                Screen.MAIN -> {
                    val pid = appState.activeProfile?.id ?: 1"""
text = text.replace(old_launched_effect, new_launched_effect)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)
