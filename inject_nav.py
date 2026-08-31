import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

sig_start = """    val appState by appViewModel.uiState.collectAsState()"""
sig_new = """    val appState by appViewModel.uiState.collectAsState()

    val autoNewSearchStr by settingsViewModel.autoNewSearch.collectAsState()
    val autoNewSearch = autoNewSearchStr.toBooleanStrictOrNull() ?: false
    val enterToSendStr by settingsViewModel.enterToSend.collectAsState()
    val enterToSend = enterToSendStr.toBooleanStrictOrNull() ?: false
    
    val toggleAutoNewSearch = {
        settingsViewModel.saveSetting("AUTO_NEW_SEARCH", (!autoNewSearch).toString())
    }"""
text = text.replace(sig_start, sig_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

