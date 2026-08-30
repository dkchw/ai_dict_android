with open('app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

state_vars = """
    var searchInput by mutableStateOf("")
    var translateInput by mutableStateOf("")
    var explainInput by mutableStateOf("")
    var compareInput by mutableStateOf("")
"""

idx = text.find(') : ViewModel() {')
if idx != -1:
    idx += len(') : ViewModel() {')
    text = text[:idx] + state_vars + text[idx:]
    with open('app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
        f.write(text)
