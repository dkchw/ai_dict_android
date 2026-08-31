import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

old_load = """    fun loadWord(word: com.aidict.app.data.entities.Word) {
        val _uiState = getUiState(word.mode)
        viewModelScope.launch {
            database.appDao().incrementViewCount(word.id)
            val updatedWord = word.copy(viewCount = word.viewCount + 1)
            database.appDao().insertWord(updatedWord)
            val messages = database.appDao().getChatMessagesSync(word.id)"""
            
new_load = """    fun loadWord(word: com.aidict.app.data.entities.Word) {
        val _uiState = getUiState(word.mode)
        viewModelScope.launch {
            database.appDao().incrementViewCount(word.id)
            val updatedWord = word.copy(viewCount = word.viewCount + 1)
            val messages = database.appDao().getChatMessagesSync(word.id)"""

text = text.replace(old_load, new_load)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

