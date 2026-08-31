import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

old_state_pattern = r'    private val _uiState = MutableStateFlow\(SearchState\(\)\)\n    val uiState: StateFlow<SearchState> = _uiState.asStateFlow\(\)'

new_states = """    private val _dictState = MutableStateFlow(SearchState())
    val dictState: StateFlow<SearchState> = _dictState.asStateFlow()
    
    private val _compareState = MutableStateFlow(SearchState())
    val compareState: StateFlow<SearchState> = _compareState.asStateFlow()
    
    private val _translateState = MutableStateFlow(SearchState())
    val translateState: StateFlow<SearchState> = _translateState.asStateFlow()
    
    private val _explainState = MutableStateFlow(SearchState())
    val explainState: StateFlow<SearchState> = _explainState.asStateFlow()
    
    fun getUiState(mode: String): MutableStateFlow<SearchState> {
        return when (mode) {
            "dict" -> _dictState
            "compare" -> _compareState
            "translate" -> _translateState
            "explain" -> _explainState
            else -> _dictState
        }
    }"""

text = re.sub(old_state_pattern, new_states, text)

# Now fix the screens that had Too many arguments for retryMessage and deleteMessage
# Wait, I changed deleteMessage(msg) to deleteMessage(msg, mode) in screens, let's make sure SearchViewModel has the correct signature.
# Check deleteMessage in SearchViewModel
text = re.sub(r'fun deleteMessage\(msg: ChatMessage\) \{', r'fun deleteMessage(msg: ChatMessage, mode: String) {\n        val _uiState = getUiState(mode)', text)
text = re.sub(r'fun retryMessage\(msg: ChatMessage, useFallback: Boolean = false\) \{', r'fun retryMessage(msg: ChatMessage, useFallback: Boolean = false, mode: String) {\n        val _uiState = getUiState(mode)', text)

# I should also fix the Unresolved reference `content` in TranslateScreen:
# TranslateScreen had: deleteMessage(msg, "translate") which is fine, but in SearchScreen it had:
# `viewModel.deleteMessage(msg, "dict")` -> Wait, the compiler said:
# Too many arguments for public final fun deleteMessage(msg: ChatMessage)
# Because I didn't successfully update the signature of deleteMessage in SearchViewModel!

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

