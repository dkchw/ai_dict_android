import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

target = "                        IconButton(onClick = { showManualDialog = true }) {"

injection = """                        val currentWord = searchViewModel.dictState.collectAsState().value.word?.word 
                            ?: searchViewModel.translateState.collectAsState().value.word?.word 
                            ?: searchViewModel.explainState.collectAsState().value.word?.word 
                            ?: searchViewModel.compareState.collectAsState().value.word?.word
                            ?: searchViewModel.searchInput

                        ExternalDictButton(settingsViewModel, currentWord)
                        """

text = text.replace(target, injection + target)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

