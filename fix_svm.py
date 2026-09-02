import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# In retryMessage, after getting currentWordId, we can update the generationCount
# Let's find `val currentWordId = word.id`
target = """        val currentWordId = word.id
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {"""

replacement = """        val currentWordId = word.id
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            val updatedWordForGen = word.copy(generationCount = word.generationCount + 1)
            database.appDao().updateWord(updatedWordForGen)
            if (_uiState.value.word?.id == currentWordId) {
                _uiState.value = _uiState.value.copy(word = updatedWordForGen)
            }"""

text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

print("Updated SearchViewModel")
