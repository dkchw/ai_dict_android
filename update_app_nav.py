import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

sig_start = """    val appTheme by settingsViewModel.appTheme.collectAsState()"""

sig_new = """    val appTheme by settingsViewModel.appTheme.collectAsState()
    val autoNewSearchStr by settingsViewModel.autoNewSearch.collectAsState()
    val autoNewSearch = autoNewSearchStr.toBooleanStrictOrNull() ?: false
    val enterToSendStr by settingsViewModel.enterToSend.collectAsState()
    val enterToSend = enterToSendStr.toBooleanStrictOrNull() ?: false
    
    val toggleAutoNewSearch = {
        settingsViewModel.saveSetting("AUTO_NEW_SEARCH", (!autoNewSearch).toString())
    }"""

text = text.replace(sig_start, sig_new)

calls_old = """                            when (page) {
                                0 -> SearchScreen(searchViewModel, pid)
                                1 -> CompareScreen(searchViewModel, pid)
                                2 -> TranslateScreen(searchViewModel, pid)
                                3 -> ExplainScreen(searchViewModel, pid)
                            }"""

calls_new = """                            when (page) {
                                0 -> SearchScreen(searchViewModel, pid, autoNewSearch = autoNewSearch, onToggleAutoNewSearch = toggleAutoNewSearch, enterToSend = enterToSend)
                                1 -> CompareScreen(searchViewModel, pid, autoNewSearch = autoNewSearch, onToggleAutoNewSearch = toggleAutoNewSearch, enterToSend = enterToSend)
                                2 -> TranslateScreen(searchViewModel, pid, autoNewSearch = autoNewSearch, onToggleAutoNewSearch = toggleAutoNewSearch, enterToSend = enterToSend)
                                3 -> ExplainScreen(searchViewModel, pid, autoNewSearch = autoNewSearch, onToggleAutoNewSearch = toggleAutoNewSearch, enterToSend = enterToSend)
                            }"""

text = text.replace(calls_old, calls_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

