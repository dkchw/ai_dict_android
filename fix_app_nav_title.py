import re
with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Replace the title block completely to align end (right) but gracefully next to actions
old_title_block = """                title = { 
                    Column(modifier = Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("AI Dict", style = MaterialTheme.typography.titleLarge)
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            Row(
                                verticalAlignment = Alignment.CenterVertically, 
                                modifier = Modifier.clickable { expanded = true }.padding(horizontal = 8.dp, vertical = 2.dp)
                            ) {
                                Text(appState.activeProfile?.name ?: "Default", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
                                Icon(Icons.Default.ArrowDropDown, contentDescription = "Select", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)
                            }
                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                appState.profiles.forEach { profile ->
                                    DropdownMenuItem(
                                        text = { Text(profile.name) },
                                        onClick = { 
                                            appViewModel.setActiveProfile(profile)
                                            expanded = false 
                                        }
                                    )
                                }
                            }
                        }
                    }
                },"""

new_title_block = """                title = { 
                    Column(modifier = Modifier.fillMaxWidth().padding(end = 8.dp), horizontalAlignment = Alignment.End) {
                        Text("AI Dict", style = MaterialTheme.typography.titleLarge)
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            Row(
                                verticalAlignment = Alignment.CenterVertically, 
                                modifier = Modifier.clickable { expanded = true }.padding(horizontal = 8.dp, vertical = 2.dp),
                                horizontalArrangement = Arrangement.End
                            ) {
                                Text(appState.activeProfile?.name ?: "Default", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
                                Icon(Icons.Default.ArrowDropDown, contentDescription = "Select", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)
                            }
                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                appState.profiles.forEach { profile ->
                                    DropdownMenuItem(
                                        text = { Text(profile.name) },
                                        onClick = { 
                                            appViewModel.setActiveProfile(profile)
                                            expanded = false 
                                        }
                                    )
                                }
                            }
                        }
                    }
                },"""

text = text.replace(old_title_block, new_title_block)
with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

