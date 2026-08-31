import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

text = re.sub(r'(fun streamTranslation\([^)]+\) \{)', r'\1\n        val _uiState = _translateState', text)
text = re.sub(r'(fun streamExplain\([^)]+\) \{)', r'\1\n        val _uiState = _explainState', text)
text = re.sub(r'(fun streamCompare\([^)]+\) \{)', r'\1\n        val _uiState = _compareState', text)

text = re.sub(r'(fun sendFollowUpMessage\([^)]+\) \{)', r'\1\n        val _uiState = getUiState("dict") // fallback', text) # Wait, sendFollowUpMessage already had my replacement?
text = re.sub(r'fun retryMessage\(assistantMsg: com.aidict.app.data.entities.ChatMessage, forceFallback: Boolean\) \{', r'fun retryMessage(assistantMsg: com.aidict.app.data.entities.ChatMessage, forceFallback: Boolean, mode: String = "dict") {\n        val _uiState = getUiState(mode)', text)

# I see unresolved references for `_uiState` in other places, I'll just find them manually if there are still compile errors.
# Let's fix the sendFollowUpMessage which had too many arguments:
# "Too many arguments for public final fun sendFollowUpMessage(content: String)"
text = text.replace("fun sendFollowUpMessage(content: String) {", "fun sendFollowUpMessage(content: String, mode: String = \"dict\") {\n        val _uiState = getUiState(mode)")
# deleteCurrentWord
text = text.replace("fun deleteCurrentWord() {", "fun deleteCurrentWord(mode: String = \"dict\") {\n        val _uiState = getUiState(mode)")
text = text.replace("fun updateWordColor(color: String) {", "fun updateWordColor(color: String, mode: String = \"dict\") {\n        val _uiState = getUiState(mode)")
text = text.replace("fun updateWordStars(stars: Int) {", "fun updateWordStars(stars: Int, mode: String = \"dict\") {\n        val _uiState = getUiState(mode)")

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

