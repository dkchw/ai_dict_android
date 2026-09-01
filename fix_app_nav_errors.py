import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Fix the word reference
old_current_word = """                        val currentWord = searchViewModel.dictState.collectAsState().value.word?.word 
                            ?: searchViewModel.translateState.collectAsState().value.word?.word 
                            ?: searchViewModel.explainState.collectAsState().value.word?.word 
                            ?: searchViewModel.compareState.collectAsState().value.word?.word
                            ?: searchViewModel.searchInput"""

new_current_word = """                        val currentWord = searchViewModel.dictState.collectAsState().value.word?.term 
                            ?: searchViewModel.translateState.collectAsState().value.word?.term 
                            ?: searchViewModel.explainState.collectAsState().value.word?.term 
                            ?: searchViewModel.compareState.collectAsState().value.word?.term
                            ?: searchViewModel.searchInput"""

text = text.replace(old_current_word, new_current_word)

# Fix the icon
text = text.replace('Icons.Default.Language', 'Icons.Default.Public')

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

