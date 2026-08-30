import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    content = f.read()

replacement = """
                Screen.MAIN -> {
                    val pid = appState.activeProfile?.id ?: 1
                    LaunchedEffect(currentMode) {
                        searchViewModel.clearCurrentSearch()
                    }
"""

pattern = r'                Screen\.MAIN -> \{\n                    val pid = appState\.activeProfile\?\.id \?: 1'
content = re.sub(pattern, replacement.strip('\n'), content)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(content)
