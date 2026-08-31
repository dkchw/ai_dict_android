import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# 1. Fix TopAppBar (which I missed earlier)
old_topbar = r'TopAppBar\(\s*colors = TopAppBarDefaults\.topAppBarColors.*?IconButton\(onClick = \{ currentScreen = Screen\.SETTINGS \}\) \{\s*Icon\(Icons\.Default\.Settings, contentDescription = "Settings"\)\s*\}\s*\} else \{\s*Spacer\(modifier = Modifier\.width\(48\.dp\)\) // Balance the title centering\s*\}\s*\}\s*\)'

new_topbar = """Row(
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
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
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
                        IconButton(onClick = { currentScreen = Screen.NOTES }) {
                            Icon(Icons.Default.EditNote, contentDescription = "Notes")
                        }
                        IconButton(onClick = { currentScreen = Screen.SETTINGS }) {
                            Icon(Icons.Default.Settings, contentDescription = "Settings")
                        }
                    } else {
                        Spacer(modifier = Modifier.width(48.dp))
                    }
                }
            }"""
text = re.sub(old_topbar, new_topbar, text, flags=re.DOTALL)

# 2. Fix NavigationBar to custom Row
old_bottombar = r'NavigationBar\(containerColor = androidx\.compose\.ui\.graphics\.Color\.Transparent\) \{.*?\}\s*\}'
new_bottombar = """Row(
                    modifier = Modifier.fillMaxWidth().height(56.dp).background(androidx.compose.ui.graphics.Color.Transparent),
                    horizontalArrangement = Arrangement.SpaceEvenly,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    modes.forEachIndexed { index, tab ->
                        val isSelected = currentMode == index
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier
                                .clickable {
                                    if (currentMode != index) {
                                        coroutineScope.launch { pagerState.animateScrollToPage(index) }
                                        searchViewModel.clearCurrentSearch()
                                    }
                                }
                                .padding(horizontal = 16.dp, vertical = 4.dp)
                        ) {
                            Icon(
                                tab.icon, 
                                contentDescription = tab.title, 
                                tint = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.size(24.dp)
                            )
                            Text(
                                tab.title, 
                                style = MaterialTheme.typography.labelSmall,
                                color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }"""
text = re.sub(old_bottombar, new_bottombar, text, flags=re.DOTALL)

# 3. Fix Pull-to-Refresh threshold and add visual indicator
old_pull = r'if \(pullRefreshState\.progress > maxProgress\) \{.*?if \(pullRefreshState\.isRefreshing\) \{.*?\}'
new_pull = """if (pullRefreshState.progress > maxProgress) {
                        maxProgress = pullRefreshState.progress
                    }
                    if (pullRefreshState.progress == 0f && !pullRefreshState.isRefreshing) {
                        maxProgress = 0f
                    }
                    
                    if (pullRefreshState.isRefreshing) {
                        LaunchedEffect(Unit) {
                            if (maxProgress > 1.3f) {
                                currentScreen = Screen.SETTINGS
                            } else {
                                appViewModel.clearHistoryUnseen()
                                currentScreen = Screen.HISTORY
                            }
                            pullRefreshState.endRefresh()
                            maxProgress = 0f
                        }
                    }"""
text = re.sub(old_pull, new_pull, text, flags=re.DOTALL)

# Add visual feedback overlay
old_pull_container = r'androidx\.compose\.material3\.pulltorefresh\.PullToRefreshContainer\(\s*state = pullRefreshState,\s*modifier = Modifier\.align\(Alignment\.TopCenter\)\s*\)'
new_pull_container = """androidx.compose.material3.pulltorefresh.PullToRefreshContainer(
                            state = pullRefreshState,
                            modifier = Modifier.align(Alignment.TopCenter)
                        )
                        if (pullRefreshState.progress > 0f) {
                            val isHardPull = pullRefreshState.progress > 1.3f
                            Box(modifier = Modifier.align(Alignment.TopCenter).padding(top = 90.dp).background(if (isHardPull) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant, androidx.compose.foundation.shape.RoundedCornerShape(12.dp)).padding(horizontal = 16.dp, vertical = 8.dp)) {
                                Text(
                                    text = if (isHardPull) "Release for Settings" else "Pull further for Settings",
                                    color = if (isHardPull) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant,
                                    style = MaterialTheme.typography.labelMedium
                                )
                            }
                        }"""
text = text.replace(old_pull_container, new_pull_container)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

