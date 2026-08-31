import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Replace TopAppBar with a custom Row
old_topbar = """        topBar = {
            TopAppBar(
colors = TopAppBarDefaults.topAppBarColors(containerColor = androidx.compose.ui.graphics.Color.Transparent),

                navigationIcon = {
                    if (currentScreen == Screen.MAIN) {
                        IconButton(onClick = { 
                            appViewModel.clearHistoryUnseen()
                            currentScreen = Screen.HISTORY 
                        }) {
                            if (appState.unseenHistoryItems > 0) {
                                BadgedBox(badge = { Badge { Text(appState.unseenHistoryItems.toString()) } }) {
                                    Icon(Icons.Default.History, contentDescription = "History")
                                }
                            } else {
                                Icon(Icons.Default.History, contentDescription = "History")
                            }
                        }
                    } else {
                        IconButton(onClick = { currentScreen = Screen.MAIN }) {
                            Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                        }
                    }
                },
                title = { 
                    Column(modifier = Modifier.fillMaxWidth().padding(start = 8.dp), horizontalAlignment = Alignment.Start) {
                        Text("AI Dict", style = MaterialTheme.typography.titleLarge)
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            Row(
                                verticalAlignment = Alignment.CenterVertically, 
                                modifier = Modifier.clickable { expanded = true }.padding(vertical = 2.dp),
                                horizontalArrangement = Arrangement.Start
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
                                            searchViewModel.clearCurrentSearch()
                                            historyViewModel.setActiveSession(null)
                                            expanded = false 
                                        }
                                    )
                                }
                            }
                        }
                    }
                },
                actions = {

                    if (currentScreen == Screen.MAIN) {
                        androidx.compose.material3.Text(
                            text = modes[currentMode].title,
                            style = androidx.compose.material3.MaterialTheme.typography.titleMedium,
                            modifier = androidx.compose.ui.Modifier.padding(end = 8.dp).align(androidx.compose.ui.Alignment.CenterVertically),
                            color = androidx.compose.material3.MaterialTheme.colorScheme.primary.copy(alpha = 0.7f)
                        )
                    }
                    IconButton(onClick = { currentScreen = Screen.SETTINGS }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                }
            )
        }"""

new_topbar = """        topBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp)
                    .background(androidx.compose.ui.graphics.Color.Transparent)
                    .padding(horizontal = 4.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (currentScreen == Screen.MAIN) {
                        IconButton(onClick = { 
                            appViewModel.clearHistoryUnseen()
                            currentScreen = Screen.HISTORY 
                        }) {
                            if (appState.unseenHistoryItems > 0) {
                                BadgedBox(badge = { Badge { Text(appState.unseenHistoryItems.toString()) } }) {
                                    Icon(Icons.Default.History, contentDescription = "History")
                                }
                            } else {
                                Icon(Icons.Default.History, contentDescription = "History")
                            }
                        }
                    } else {
                        IconButton(onClick = { currentScreen = Screen.MAIN }) {
                            Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                        }
                    }
                    
                    Column(modifier = Modifier.padding(start = 4.dp), horizontalAlignment = Alignment.Start) {
                        Text("AI Dict", style = MaterialTheme.typography.titleMedium)
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            Row(
                                verticalAlignment = Alignment.CenterVertically, 
                                modifier = Modifier.clickable { expanded = true }.padding(vertical = 2.dp),
                                horizontalArrangement = Arrangement.Start
                            ) {
                                Text(appState.activeProfile?.name ?: "Default", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                                Icon(Icons.Default.ArrowDropDown, contentDescription = "Select", modifier = Modifier.size(14.dp), tint = MaterialTheme.colorScheme.primary)
                            }
                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                appState.profiles.forEach { profile ->
                                    DropdownMenuItem(
                                        text = { Text(profile.name) },
                                        onClick = { 
                                            appViewModel.setActiveProfile(profile)
                                            searchViewModel.clearCurrentSearch()
                                            historyViewModel.setActiveSession(null)
                                            expanded = false 
                                        }
                                    )
                                }
                            }
                        }
                    }
                }
                
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (currentScreen == Screen.MAIN) {
                        androidx.compose.material3.Text(
                            text = modes[currentMode].title,
                            style = androidx.compose.material3.MaterialTheme.typography.titleSmall,
                            modifier = androidx.compose.ui.Modifier.padding(end = 8.dp),
                            color = androidx.compose.material3.MaterialTheme.colorScheme.primary.copy(alpha = 0.7f)
                        )
                    }
                    IconButton(onClick = { currentScreen = Screen.SETTINGS }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                }
            }
        }"""

text = text.replace(old_topbar, new_topbar)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

