import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Define coroutine scope and replace currentMode var
text = text.replace('var currentMode by remember { mutableStateOf(0) }', 'val coroutineScope = rememberCoroutineScope()\n    val currentMode = pagerState.targetPage')

# Remove LaunchedEffects for sync
le_sync = """    LaunchedEffect(currentMode) {
        if (pagerState.currentPage != currentMode) {
            pagerState.animateScrollToPage(currentMode)
        }
    }
    LaunchedEffect(pagerState.currentPage) {
        if (currentMode != pagerState.currentPage) {
            currentMode = pagerState.currentPage
        }
    }"""
text = text.replace(le_sync, "")

# Replace backhandler
back_old = """        } else if (currentMode != 0) {
            currentMode = 0
        } else if (currentSearchState.word != null) {"""
back_new = """        } else if (currentMode != 0) {
            coroutineScope.launch { pagerState.animateScrollToPage(0) }
        } else if (currentSearchState.word != null) {"""
text = text.replace(back_old, back_new)

# Replace navigation bar click
nav_old = """                            onClick = { 
                                if (currentMode != index) {
                                    currentMode = index
                                    searchViewModel.clearCurrentSearch()
                                }
                            },"""
nav_new = """                            onClick = { 
                                if (currentMode != index) {
                                    coroutineScope.launch { pagerState.animateScrollToPage(index) }
                                    searchViewModel.clearCurrentSearch()
                                }
                            },"""
text = text.replace(nav_old, nav_new)

# Replace history click
hist_old = """                            }
                            currentMode = modeInt
                            currentScreen = Screen.MAIN"""
hist_new = """                            }
                            coroutineScope.launch { pagerState.scrollToPage(modeInt) }
                            currentScreen = Screen.MAIN"""
text = text.replace(hist_old, hist_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

