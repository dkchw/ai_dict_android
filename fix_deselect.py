import re

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
    text = f.read()

text = text.replace("""                        Surface(
                            modifier = Modifier
                                .fillMaxWidth()
                                .heightIn(max = 600.dp)
                                .clickable(
                                    interactionSource = remember { MutableInteractionSource() },
                                    indication = null
                                ) { /* Prevent clicks inside from closing */ },""", """                        val focusManager = androidx.compose.ui.platform.LocalFocusManager.current
                        Surface(
                            modifier = Modifier
                                .fillMaxWidth()
                                .heightIn(max = 600.dp)
                                .clickable(
                                    interactionSource = remember { MutableInteractionSource() },
                                    indication = null
                                ) { focusManager.clearFocus() },""")

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
    f.write(text)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

text = text.replace("""@Composable
fun AppNavigation(
    appViewModel: com.aidict.app.ui.viewmodels.AppViewModel,
    searchViewModel: com.aidict.app.ui.viewmodels.SearchViewModel,
    historyViewModel: com.aidict.app.ui.viewmodels.HistoryViewModel,
    settingsViewModel: com.aidict.app.ui.viewmodels.SettingsViewModel,
    windowSizeClass: androidx.compose.material3.windowsizeclass.WindowSizeClass,
    initialMode: Int = 0
) {""", """@Composable
fun AppNavigation(
    appViewModel: com.aidict.app.ui.viewmodels.AppViewModel,
    searchViewModel: com.aidict.app.ui.viewmodels.SearchViewModel,
    historyViewModel: com.aidict.app.ui.viewmodels.HistoryViewModel,
    settingsViewModel: com.aidict.app.ui.viewmodels.SettingsViewModel,
    windowSizeClass: androidx.compose.material3.windowsizeclass.WindowSizeClass,
    initialMode: Int = 0
) {
    val focusManager = androidx.compose.ui.platform.LocalFocusManager.current""")

# Now find the Box inside AppNavigation to add clickable
box_target = """    Box(modifier = Modifier.fillMaxSize()) {"""
box_replace = """    Box(modifier = Modifier.fillMaxSize().clickable(
        interactionSource = remember { MutableInteractionSource() },
        indication = null
    ) { focusManager.clearFocus() }) {"""
text = text.replace(box_target, box_replace)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Added deselect logic")
