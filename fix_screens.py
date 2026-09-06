import re
import os

screens = {
    'SearchScreen.kt': ('viewModel.searchInput = ""', 'searchInput'),
    'CompareScreen.kt': ('viewModel.compareInput = ""', 'compareInput'),
    'TranslateScreen.kt': ('viewModel.translateInput = ""', 'translateInput'),
    'ExplainScreen.kt': ('viewModel.explainInput = ""', 'explainInput')
}

for screen, (clear_input_stmt, input_prop) in screens.items():
    path = f'android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}'
    with open(path, 'r') as f:
        text = f.read()

    target = "            placeholder ="
    
    # We also need suggestions state. Let's find `val state by viewModel.dictState.collectAsState()`
    # and add `val suggestions by viewModel.suggestions.collectAsState()`
    state_target = f"val state by viewModel.{'dict' if screen == 'SearchScreen.kt' else 'compare' if screen == 'CompareScreen.kt' else 'translate' if screen == 'TranslateScreen.kt' else 'explain'}State.collectAsState()"
    if "val suggestions by viewModel.suggestions.collectAsState()" not in text:
        text = text.replace(state_target, state_target + "\n    val suggestions by viewModel.suggestions.collectAsState()")
    
    replacement = f"""            suggestions = suggestions,
            onSuggestionClick = {{ word -> 
                viewModel.loadWord(word)
                {clear_input_stmt}
                viewModel.clearSuggestions()
            }},
            placeholder ="""
    
    text = text.replace(target, replacement)
    
    with open(path, 'w') as f:
        f.write(text)

print("Updated screens")
