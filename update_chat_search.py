import os

screens = ['SearchScreen.kt', 'CompareScreen.kt', 'TranslateScreen.kt', 'ExplainScreen.kt']

for screen in screens:
    path = f'android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}'
    with open(path, 'r') as f:
        text = f.read()

    # 1. Add state variables
    state_vars = "    var isChatSearching by remember { mutableStateOf(false) }\n    var chatSearchQuery by remember { mutableStateOf(\"\") }"
    if "isChatSearching" not in text:
        text = text.replace("    val context = LocalContext.current", "    val context = LocalContext.current\n" + state_vars)

    # 2. Add Search Icon to Action Bar
    search_icon = """                    IconButton(onClick = { isChatSearching = !isChatSearching }) {
                        Icon(Icons.Default.Search, contentDescription = "Search in Chat")
                    }"""
    if "Icon(Icons.Default.Search, contentDescription = \"Search in Chat\")" not in text:
        text = text.replace('                        Icon(Icons.Default.Refresh, contentDescription = "Restart with Current Model", tint = MaterialTheme.colorScheme.primary)\n                    }', search_icon + '\n                    IconButton(onClick = {\n                        val lastUserMsg = state.chatMessages.findLast { it.role == "assistant" }\n                        if (lastUserMsg != null) viewModel.retryMessage(lastUserMsg, false, "' + ('dict' if screen == 'SearchScreen.kt' else 'compare' if screen == 'CompareScreen.kt' else 'translate' if screen == 'TranslateScreen.kt' else 'explain') + '")\n                    }) {\n                        Icon(Icons.Default.Refresh, contentDescription = "Restart with Current Model", tint = MaterialTheme.colorScheme.primary)\n                    }')

    # 3. Add Search Bar UI below Action Bar
    search_bar_ui = """                if (isChatSearching) {
                    OutlinedTextField(
                        value = chatSearchQuery,
                        onValueChange = { chatSearchQuery = it },
                        modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                        placeholder = { Text("Find in chat...") },
                        singleLine = true,
                        trailingIcon = {
                            if (chatSearchQuery.isNotEmpty()) {
                                IconButton(onClick = { chatSearchQuery = "" }) {
                                    Icon(Icons.Default.Clear, contentDescription = "Clear Search")
                                }
                            }
                        }
                    )
                }"""
    # Insert it right before the Colors row or before Spacer(modifier = Modifier.height(8.dp))
    if "if (isChatSearching)" not in text:
        if "                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(top = 4.dp)) {" in text:
            text = text.replace("                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(top = 4.dp)) {", search_bar_ui + "\n                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(top = 4.dp)) {")
        elif "                Spacer(modifier = Modifier.height(8.dp))" in text:
            text = text.replace("                Spacer(modifier = Modifier.height(8.dp))", search_bar_ui + "\n                Spacer(modifier = Modifier.height(8.dp))")
        else:
            print(f"Could not find insert point for {screen}")

    # 4. Pass chatSearchQuery to MarkdownText
    if 'searchQuery = chatSearchQuery' not in text:
        text = text.replace("MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onPrimary)", "MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onPrimary, searchQuery = chatSearchQuery)")
        text = text.replace("MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer)", "MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer, searchQuery = chatSearchQuery)")
        # for ExplainScreen
        text = text.replace("com.aidict.app.ui.components.MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onPrimary)", "com.aidict.app.ui.components.MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onPrimary, searchQuery = chatSearchQuery)")
        text = text.replace("com.aidict.app.ui.components.MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer)", "com.aidict.app.ui.components.MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer, searchQuery = chatSearchQuery)")
        text = text.replace("com.aidict.app.ui.components.MarkdownText(text = state.currentStream, color = MaterialTheme.colorScheme.onSecondaryContainer)", "com.aidict.app.ui.components.MarkdownText(text = state.currentStream, color = MaterialTheme.colorScheme.onSecondaryContainer, searchQuery = chatSearchQuery)")

    with open(path, 'w') as f:
        f.write(text)
print("Updated all 4 mode screens")
