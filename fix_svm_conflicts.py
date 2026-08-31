import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Fix sendFollowUpMessage
text = text.replace('val _uiState = getUiState(mode)\n        val _uiState = getUiState("dict") // fallback', 'val _uiState = getUiState(mode)')

# Fix loadWord (line 241)
text = re.sub(r'fun loadWord\(word: com.aidict.app.data.entities.Word\) \{', r'fun loadWord(word: com.aidict.app.data.entities.Word) {\n        val _uiState = getUiState(word.mode)', text)

# Fix editMessage (line 279)
text = re.sub(r'fun editMessage\(msg: com.aidict.app.data.entities.ChatMessage, newContent: String\) \{', r'fun editMessage(msg: com.aidict.app.data.entities.ChatMessage, newContent: String, mode: String) {\n        val _uiState = getUiState(mode)', text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

