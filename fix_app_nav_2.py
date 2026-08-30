with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    nav = f.read()

replacement = """                    HistoryScreen(
                        appViewModel = appViewModel,
                        onNavigateToChat = { word ->
                            searchViewModel.loadWord(word)
                            val modeInt = when (word.mode) {
                                "dict" -> 0
                                "compare" -> 1
                                "translate" -> 2
                                "explain" -> 3
                                else -> 0
                            }
                            currentMode = modeInt
                            currentScreen = Screen.MAIN
                        },
                        viewModel = historyViewModel,
                        windowSizeClass = windowSizeClass
                    )"""

nav = nav.replace('HistoryScreen(appViewModel, historyViewModel, windowSizeClass)', replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(nav)
