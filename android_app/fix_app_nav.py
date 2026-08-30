import re

with open('app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    nav = f.read()

replacement = """                Screen.HISTORY -> {
                    HistoryScreen(
                        appViewModel = appViewModel,
                        viewModel = historyViewModel,
                        windowSizeClass = windowSizeClass,
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
                        }
                    )
                }"""

pattern = r'                Screen\.HISTORY -> \{\n                    val modeStr = when \(currentMode\) \{\n                        0 -> "dict"\n                        1 -> "compare"\n                        2 -> "translate"\n                        3 -> "explain"\n                        else -> "dict"\n                    \}\n                    historyViewModel\.setMode\(modeStr\)\n                    HistoryScreen\(\n                        appViewModel = appViewModel,\n                        viewModel = historyViewModel,\n                        windowSizeClass = windowSizeClass\n                    \)\n                \}'

nav = re.sub(pattern, replacement, nav, flags=re.DOTALL)

with open('app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(nav)
