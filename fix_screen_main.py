import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Replace the whole block starting from Screen.MAIN -> {
start_idx = text.find('                Screen.MAIN -> {')
end_idx = text.find('    }\n}\n', start_idx) + 6 # until the end of the file

new_main = """                Screen.MAIN -> {
                    val pid = appState.activeProfile?.id ?: 1
                    
                    val pullRefreshState = androidx.compose.material3.pulltorefresh.rememberPullToRefreshState()
                    var maxProgress by remember { mutableStateOf(0f) }
                    
                    if (pullRefreshState.progress > maxProgress) {
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
                    }
                    
                    Box(modifier = Modifier.fillMaxSize().nestedScroll(pullRefreshState.nestedScrollConnection)) {
                        androidx.compose.foundation.pager.HorizontalPager(
                            state = pagerState,
                            modifier = Modifier.fillMaxSize(),
                            beyondBoundsPageCount = 1
                        ) { page ->
                            when (page) {
                                0 -> SearchScreen(searchViewModel, pid)
                                1 -> CompareScreen(searchViewModel, pid)
                                2 -> TranslateScreen(searchViewModel, pid)
                                3 -> ExplainScreen(searchViewModel, pid)
                            }
                        }
                        
                        androidx.compose.material3.pulltorefresh.PullToRefreshContainer(
                            state = pullRefreshState,
                            modifier = Modifier.align(Alignment.TopCenter)
                        )
                        
                        if (pullRefreshState.progress > 0f) {
                            val isHardPull = pullRefreshState.progress > 1.3f
                            Box(modifier = Modifier
                                .align(Alignment.TopCenter)
                                .padding(top = 90.dp)
                                .background(
                                    color = if (isHardPull) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant, 
                                    shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp)
                                )
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                            ) {
                                Text(
                                    text = if (isHardPull) "Release for Settings" else "Pull further for Settings",
                                    color = if (isHardPull) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant,
                                    style = MaterialTheme.typography.labelMedium
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

text = text[:start_idx] + new_main

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

