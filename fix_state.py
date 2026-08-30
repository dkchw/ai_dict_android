import re

# 1. Update SearchViewModel.kt to hold input states
with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    svm_content = f.read()

state_vars = """
    var searchInput by mutableStateOf("")
    var translateInput by mutableStateOf("")
    var explainInput by mutableStateOf("")
    var compareInput by mutableStateOf("")
"""

svm_content = svm_content.replace('class SearchViewModel(private val database: AppDatabase, private val llmRepository: LlmRepository) : ViewModel() {', 'class SearchViewModel(private val database: AppDatabase, private val llmRepository: LlmRepository) : ViewModel() {' + state_vars)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(svm_content)


# 2. Update SearchScreen.kt
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'r') as f:
    ss_content = f.read()
ss_content = ss_content.replace('var inputTerm by remember { mutableStateOf("") }', '')
ss_content = ss_content.replace('inputTerm = ""', 'viewModel.searchInput = ""')
ss_content = ss_content.replace('inputTerm', 'viewModel.searchInput')
ss_content = ss_content.replace('onClear = if (isFollowUp) { { viewModel.clearCurrentSearch() } } else null', 'onClear = { viewModel.clearCurrentSearch(); viewModel.searchInput = "" }')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'w') as f:
    f.write(ss_content)

# 3. Update TranslateScreen.kt
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'r') as f:
    ts_content = f.read()
ts_content = ts_content.replace('var sourceText by remember { mutableStateOf("") }', '')
ts_content = ts_content.replace('sourceText = ""', 'viewModel.translateInput = ""')
ts_content = ts_content.replace('sourceText', 'viewModel.translateInput')
ts_content = ts_content.replace('onClear = if (isFollowUp) { { viewModel.clearCurrentSearch() } } else null', 'onClear = { viewModel.clearCurrentSearch(); viewModel.translateInput = "" }')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'w') as f:
    f.write(ts_content)

# 4. Update ExplainScreen.kt
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'r') as f:
    es_content = f.read()
es_content = es_content.replace('var textToExplain by remember { mutableStateOf("") }', '')
es_content = es_content.replace('textToExplain = ""', 'viewModel.explainInput = ""')
es_content = es_content.replace('textToExplain', 'viewModel.explainInput')
es_content = es_content.replace('onClear = if (isFollowUp) { { viewModel.clearCurrentSearch() } } else null', 'onClear = { viewModel.clearCurrentSearch(); viewModel.explainInput = "" }')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'w') as f:
    f.write(es_content)

# 5. Update CompareScreen.kt
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'r') as f:
    cs_content = f.read()
cs_content = cs_content.replace('var words by remember { mutableStateOf("") }', '')
cs_content = cs_content.replace('words = ""', 'viewModel.compareInput = ""')
cs_content = cs_content.replace('words', 'viewModel.compareInput')
cs_content = cs_content.replace('onClear = if (isFollowUp) { { viewModel.clearCurrentSearch() } } else null', 'onClear = { viewModel.clearCurrentSearch(); viewModel.compareInput = "" }')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'w') as f:
    f.write(cs_content)

