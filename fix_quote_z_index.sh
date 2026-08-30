# Remove the bad injection
sed -i '/val quoteMode by settingsViewModel.quoteMode.collectAsState()/,/        }/d' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt

# Insert it before Scaffold
sed -i '/Scaffold(/i \
        val quoteMode by settingsViewModel.quoteMode.collectAsState()\n\
        val quotesList = listOf("Per studium ad sapientiam", "Labor omnia vincit", "Assiduitas mater scientiae", "Nulla dies sine linea", "Carpe diem", "Vincit qui se vincit")\n\
        var shuffledQuote by remember { mutableStateOf(quotesList.random()) }\n\
        LaunchedEffect(currentMode) { if (quoteMode == "Shuffle") shuffledQuote = quotesList.random() }\n\
        val displayQuote = when (quoteMode) { "None" -> null; "Shuffle" -> shuffledQuote; else -> quoteMode }\n\
\n\
        if (displayQuote != null && currentScreen == Screen.MAIN) {\n\
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {\n\
                Text(\n\
                    text = displayQuote,\n\
                    style = MaterialTheme.typography.headlineMedium,\n\
                    color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.3f),\n\
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center,\n\
                    modifier = Modifier.padding(32.dp)\n\
                )\n\
            }\n\
        }' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt
