import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Fix the syntax error at bottomBar
broken_bottombar = """                Row(
                    modifier = Modifier.fillMaxWidth().height(48.dp).background(androidx.compose.ui.graphics.Color.Transparent),
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
                },
                            icon = { Icon(tab.icon, contentDescription = tab.title) },
                            label = { Text(tab.title) }
                        )
                    }
                }
            }
        }"""

fixed_bottombar = """                Row(
                    modifier = Modifier.fillMaxWidth().height(48.dp).background(androidx.compose.ui.graphics.Color.Transparent),
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
                }
            }
        }"""

text = text.replace(broken_bottombar, fixed_bottombar)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

