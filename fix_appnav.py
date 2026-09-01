import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

target = """                        onNavigateToChat = { word ->
                            searchViewModel.loadWord(word)
                            val modeInt = when (word.mode) {
                                "dict" -> 0
                                "compare" -> 1
                                "translate" -> 2
                                "explain" -> 3
                                else -> 0
                            }
                            coroutineScope.launch { pagerState.scrollToPage(modeInt) }
                            currentScreen = Screen.MAIN
                        },"""

replacement = """                        onNavigateToChat = { word ->
                            searchViewModel.loadWord(word)
                            val modeInt = when (word.mode) {
                                "dict" -> 0
                                "compare" -> 1
                                "translate" -> 2
                                "explain" -> 3
                                else -> 0
                            }
                            coroutineScope.launch { pagerState.scrollToPage(modeInt) }
                            currentScreen = Screen.MAIN
                        },
                        onRestartChat = { word, msg, fallback ->
                            searchViewModel.loadWord(word)
                            val modeInt = when (word.mode) {
                                "dict" -> 0
                                "compare" -> 1
                                "translate" -> 2
                                "explain" -> 3
                                else -> 0
                            }
                            coroutineScope.launch { pagerState.scrollToPage(modeInt) }
                            currentScreen = Screen.MAIN
                            searchViewModel.retryMessage(msg, fallback, word.mode)
                        },"""

text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Updated AppNavigation.kt")
