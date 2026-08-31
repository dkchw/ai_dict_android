import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

back_handler_old = """    androidx.activity.compose.BackHandler(enabled = currentScreen != Screen.MAIN || currentMode != 0 || searchViewModel.uiState.value.word != null) {

        if (currentScreen != Screen.MAIN) {

            currentScreen = Screen.MAIN

        } else if (currentMode != 0) {
            currentMode = 0
        } else if (searchViewModel.uiState.value.word != null) {
            searchViewModel.clearCurrentSearch()
        }
    }"""

back_handler_new = """    val currentSearchState = when (currentMode) {
        0 -> searchViewModel.dictState.collectAsState().value
        1 -> searchViewModel.compareState.collectAsState().value
        2 -> searchViewModel.translateState.collectAsState().value
        3 -> searchViewModel.explainState.collectAsState().value
        else -> searchViewModel.dictState.collectAsState().value
    }

    androidx.activity.compose.BackHandler(enabled = currentScreen != Screen.MAIN || currentMode != 0 || currentSearchState.word != null) {

        if (currentScreen != Screen.MAIN) {

            currentScreen = Screen.MAIN

        } else if (currentMode != 0) {
            currentMode = 0
        } else if (currentSearchState.word != null) {
            searchViewModel.clearCurrentSearch()
        }
    }"""

text = text.replace(back_handler_old, back_handler_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Updated AppNavigation back handler")
