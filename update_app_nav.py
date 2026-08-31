import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Replace quotes logic
old_logic = """        val quotesList by settingsViewModel.allQuotes.collectAsState()

        var shuffledQuote by remember { mutableStateOf(quotesList.random()) }

        LaunchedEffect(currentMode) { if (quoteMode == "Shuffle") shuffledQuote = quotesList.random() }"""

new_logic = """        val quotesList by settingsViewModel.allQuotes.collectAsState()
        val shuffleEnabledQuotes by settingsViewModel.shuffleEnabledQuotes.collectAsState()
        
        val activeShuffleList = shuffleEnabledQuotes?.filter { it in quotesList }?.takeIf { it.isNotEmpty() } ?: quotesList

        var shuffledQuote by remember { mutableStateOf(activeShuffleList.randomOrNull() ?: "") }

        LaunchedEffect(currentMode, activeShuffleList) { if (quoteMode == "Shuffle") shuffledQuote = activeShuffleList.randomOrNull() ?: "" }"""

text = text.replace(old_logic, new_logic)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

