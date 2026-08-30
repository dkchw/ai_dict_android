sed -i '/val starredLanguages by viewModel.starredLanguages.collectAsState()/i \
            var showAddLangDialog by remember { mutableStateOf(false) }\n\
            var newLangName by remember { mutableStateOf("") }\n\
            var newLangFlag by remember { mutableStateOf("") }\n\
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.End) {\n\
                Button(onClick = { showAddLangDialog = true }) { Text("Add Custom Language") }\n\
            }\n\
            if (showAddLangDialog) {\n\
                AlertDialog(\n\
                    onDismissRequest = { showAddLangDialog = false },\n\
                    title = { Text("Add Custom Language") },\n\
                    text = {\n\
                        Column {\n\
                            OutlinedTextField(value = newLangName, onValueChange = { newLangName = it }, label = { Text("Name (e.g. Sindarin)") }, modifier = Modifier.fillMaxWidth())\n\
                            OutlinedTextField(value = newLangFlag, onValueChange = { newLangFlag = it }, label = { Text("Flag/Code (e.g. 🧝 SI)") }, modifier = Modifier.fillMaxWidth())\n\
                        }\n\
                    },\n\
                    confirmButton = {\n\
                        Button(onClick = {\n\
                            if (newLangName.isNotBlank() && newLangFlag.isNotBlank()) {\n\
                                viewModel.addCustomLanguage(newLangName, newLangFlag)\n\
                                newLangName = ""\n\
                                newLangFlag = ""\n\
                                showAddLangDialog = false\n\
                            }\n\
                        }) { Text("Add") }\n\
                    },\n\
                    dismissButton = { TextButton(onClick = { showAddLangDialog = false }) { Text("Cancel") } }\n\
                )\n\
            }' android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt
