sed -i 's/val quotes = listOf("None", "Shuffle", "Per studium ad sapientiam", "Labor omnia vincit", "Assiduitas mater scientiae", "Nulla dies sine linea", "Carpe diem", "Vincit qui se vincit")/val allQuotesList by viewModel.allQuotes.collectAsState()\n            val quotes = listOf("None", "Shuffle") + allQuotesList/' android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt

sed -i '/val quoteStyle by viewModel.quoteStyle.collectAsState()/i \
            var showAddQuoteDialog by remember { mutableStateOf(false) }\n\
            var newQuoteText by remember { mutableStateOf("") }\n\
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.End) {\n\
                Button(onClick = { showAddQuoteDialog = true }) {\n\
                    Text("Add Custom Quote")\n\
                }\n\
            }\n\
            if (showAddQuoteDialog) {\n\
                AlertDialog(\n\
                    onDismissRequest = { showAddQuoteDialog = false },\n\
                    title = { Text("Add Custom Quote") },\n\
                    text = {\n\
                        OutlinedTextField(value = newQuoteText, onValueChange = { newQuoteText = it }, label = { Text("Quote Text") }, modifier = Modifier.fillMaxWidth())\n\
                    },\n\
                    confirmButton = {\n\
                        Button(onClick = {\n\
                            if (newQuoteText.isNotBlank()) {\n\
                                viewModel.addCustomQuote(newQuoteText.trim())\n\
                                viewModel.saveSetting("QUOTE_MODE", newQuoteText.trim())\n\
                                newQuoteText = ""\n\
                                showAddQuoteDialog = false\n\
                            }\n\
                        }) { Text("Add") }\n\
                    },\n\
                    dismissButton = { TextButton(onClick = { showAddQuoteDialog = false }) { Text("Cancel") } }\n\
                )\n\
            }' android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt
