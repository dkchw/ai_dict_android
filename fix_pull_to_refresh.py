import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

old_pull = """                    val pullRefreshState = androidx.compose.material3.pulltorefresh.rememberPullToRefreshState()
                    if (pullRefreshState.isRefreshing) {
                        LaunchedEffect(Unit) {
                            appViewModel.clearHistoryUnseen()
                            currentScreen = Screen.HISTORY
                            pullRefreshState.endRefresh()
                        }
                    }"""

new_pull = """                    val pullRefreshState = androidx.compose.material3.pulltorefresh.rememberPullToRefreshState()
                    var maxProgress by remember { mutableStateOf(0f) }
                    
                    if (pullRefreshState.progress > maxProgress) {
                        maxProgress = pullRefreshState.progress
                    }
                    if (pullRefreshState.progress == 0f && !pullRefreshState.isRefreshing) {
                        maxProgress = 0f
                    }
                    
                    if (pullRefreshState.isRefreshing) {
                        LaunchedEffect(Unit) {
                            if (maxProgress > 1.8f) {
                                currentScreen = Screen.SETTINGS
                            } else {
                                appViewModel.clearHistoryUnseen()
                                currentScreen = Screen.HISTORY
                            }
                            pullRefreshState.endRefresh()
                            maxProgress = 0f
                        }
                    }"""

text = text.replace(old_pull, new_pull)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

