import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

old_clear = """    fun clearCurrentSearch() {
        activeStreamJobs.values.forEach { it.cancel() }
        activeStreamJobs.clear()
        
        _dictState.value = SearchState()
        _compareState.value = SearchState()
        _translateState.value = SearchState()
        _explainState.value = SearchState()
    }"""

new_clear = """    fun clearCurrentSearch() {
        activeStreamJobs.values.forEach { it.cancel() }
        activeStreamJobs.clear()
        
        _dictState.value = SearchState()
        _compareState.value = SearchState()
        _translateState.value = SearchState()
        _explainState.value = SearchState()
        
        searchInput = ""
        translateInput = ""
        compareInput = ""
        explainInput = ""
    }"""

text = text.replace(old_clear, new_clear)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

