import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Replace single _uiState with 4 states
old_state = """    private val _uiState = MutableStateFlow(SearchState())
    val uiState: StateFlow<SearchState> = _uiState.asStateFlow()"""

new_state = """    private val _dictState = MutableStateFlow(SearchState())
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
text = text.replace(old_state, new_state)

# Now we must update every function in SearchViewModel to use the correct state!
# searchWord -> _dictState
# compareWords -> _compareState
# translateWord -> _translateState
# explainWord -> _explainState

text = text.replace("fun searchWord(", "fun searchWord(\n        originalText: String, sourceLang: String, targetLang: String, profileId: Int\n    ) { val _uiState = _dictState; \n//")
text = text.replace("    fun searchWord(\n        text: String,", "    fun searchWord(\n        text: String,")
# Wait, let's use regex to surgically inject `val _uiState = ...` at the top of these functions.
