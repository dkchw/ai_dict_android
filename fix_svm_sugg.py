import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Add _suggestions and suggestions properties
sugg_code = """    private val _suggestions = MutableStateFlow<List<com.aidict.app.data.entities.Word>>(emptyList())
    val suggestions: StateFlow<List<com.aidict.app.data.entities.Word>> = _suggestions.asStateFlow()

    private suspend fun updateSuggestions(mode: String, query: String) {
        if (query.isBlank()) {
            _suggestions.value = emptyList()
            return
        }
        val profileIdStr = database.appDao().getSetting("ACTIVE_PROFILE_ID")?.value
        val profileId = profileIdStr?.toIntOrNull() ?: 1
        _suggestions.value = database.appDao().getWordSuggestions(profileId, mode, query)
    }

    private var dictJob: kotlinx.coroutines.Job? = null"""

text = text.replace("    private var dictJob: kotlinx.coroutines.Job? = null", sugg_code)

# Add updateSuggestions calls
text = text.replace('database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("DICT_DRAFT", value))', 
                    'database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("DICT_DRAFT", value))\n                updateSuggestions("dict", value)')

text = text.replace('database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("TRANSLATE_DRAFT", value))', 
                    'database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("TRANSLATE_DRAFT", value))\n                updateSuggestions("translate", value)')

text = text.replace('database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("EXPLAIN_DRAFT", value))', 
                    'database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("EXPLAIN_DRAFT", value))\n                updateSuggestions("explain", value)')

text = text.replace('database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("COMPARE_DRAFT", value))', 
                    'database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("COMPARE_DRAFT", value))\n                updateSuggestions("compare", value)')

# Also add a clear method
clear_method = """    fun clearSuggestions() {
        _suggestions.value = emptyList()
    }
"""
text = text.replace("    fun clearCurrentSearch() {", clear_method + "    fun clearCurrentSearch() {")

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

print("Added suggestions to SearchViewModel")
