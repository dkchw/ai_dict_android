import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

start_idx = text.find('                Screen.MAIN -> {')
end_idx = text.find('    }\n}\n', start_idx) + 6 # until the end of the file

new_main = """                Screen.MAIN -> {
                    val pid = appState.activeProfile?.id ?: 1
                    
                    val pullRefreshState = androidx.compose.material3.pulltorefresh.rememberPullToRefreshState()
                    
                    if (pullRefreshState.isRefreshing) {
                        LaunchedEffect(Unit) {
                            appViewModel.clearHistoryUnseen()
                            currentScreen = Screen.HISTORY
                            pullRefreshState.endRefresh()
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

