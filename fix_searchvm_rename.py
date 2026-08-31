import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

new_method = """    fun renameWord(word: com.aidict.app.data.entities.Word, newTerm: String, mode: String) {
        val _uiState = getUiState(mode)
        viewModelScope.launch {
            val updatedWord = word.copy(term = newTerm)
            database.appDao().insertWord(updatedWord)
            if (_uiState.value.word?.id == word.id) {
                _uiState.value = _uiState.value.copy(word = updatedWord)
            }
        }
    }

"""

if 'fun renameWord' not in text:
    text = text.replace('fun updateWordColor', new_method + '    fun updateWordColor')
    with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
        f.write(text)

