sed -i '/val isUser = msg.role == "user"/i \
                var editingMsgId by remember { mutableStateOf<Int?>(null) }\n\
                var editingContent by remember { mutableStateOf("") }' android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt

cat << 'INNER' > patch_edit.txt
                            if (isUser) {
                                Text(text = msg.content, color = MaterialTheme.colorScheme.onPrimary)
                            } else {
                                if (editingMsgId == msg.id) {
                                    Column {
                                        OutlinedTextField(
                                            value = editingContent,
                                            onValueChange = { editingContent = it },
                                            modifier = Modifier.fillMaxWidth()
                                        )
                                        Row(horizontalArrangement = Arrangement.End, modifier = Modifier.fillMaxWidth()) {
                                            TextButton(onClick = { editingMsgId = null }) { Text("Cancel") }
                                            TextButton(onClick = { 
                                                viewModel.editMessage(msg, editingContent)
                                                editingMsgId = null 
                                            }) { Text("Save") }
                                        }
                                    }
                                } else {
                                    Text(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer)
                                }
                            }
INNER

sed -i '/if (isUser) {/,/}/c\
                            if (isUser) {\
                                Text(text = msg.content, color = MaterialTheme.colorScheme.onPrimary)\
                            } else {\
                                if (editingMsgId == msg.id) {\
                                    Column {\
                                        OutlinedTextField(\
                                            value = editingContent,\
                                            onValueChange = { editingContent = it },\
                                            modifier = Modifier.fillMaxWidth()\
                                        )\
                                        Row(horizontalArrangement = Arrangement.End, modifier = Modifier.fillMaxWidth()) {\
                                            TextButton(onClick = { editingMsgId = null }) { Text("Cancel", color = MaterialTheme.colorScheme.primary) }\
                                            TextButton(onClick = { \
                                                viewModel.editMessage(msg, editingContent)\
                                                editingMsgId = null \
                                            }) { Text("Save", color = MaterialTheme.colorScheme.primary) }\
                                        }\
                                    }\
                                } else {\
                                    Text(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer)\
                                }\
                            }' android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt

sed -i 's/IconButton(onClick = { viewModel.retryMessage(msg, false) }/IconButton(onClick = { editingMsgId = msg.id; editingContent = msg.content }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Edit, "Edit", modifier = Modifier.size(16.dp)) }\n                                IconButton(onClick = { viewModel.retryMessage(msg, false) }/g' android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt

