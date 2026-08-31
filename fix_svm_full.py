import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Make sure we don't double replace
text = text.replace("val _uiState = _dictState", "")
text = text.replace("val _uiState = _compareState", "")
text = text.replace("val _uiState = _translateState", "")
text = text.replace("val _uiState = _explainState", "")

# searchWord
text = re.sub(r'(fun searchWord\([^)]+\) \{)', r'\1\n        val _uiState = _dictState', text)
# compareWords
text = re.sub(r'(fun compareWords\([^)]+\) \{)', r'\1\n        val _uiState = _compareState', text)
# translateWord
text = re.sub(r'(fun translateWord\([^)]+\) \{)', r'\1\n        val _uiState = _translateState', text)
# explainWord
text = re.sub(r'(fun explainWord\([^)]+\) \{)', r'\1\n        val _uiState = _explainState', text)

# For other functions, we need to add `mode: String` to the signature and do `val _uiState = getUiState(mode)`
# loadWord
text = re.sub(r'(fun loadWord\(word: Word\) \{)', r'\1\n        val _uiState = getUiState(word.mode)', text)

# clearCurrentSearch
text = text.replace("""    fun clearCurrentSearch() {
        searchInput = ""
        translateInput = ""
        explainInput = ""
        compareInput = ""
        _uiState.value = SearchState()
    }""", """    fun clearCurrentSearch() {
        // we keep drafts but reset state outputs if explicitly requested, but maybe not?
        // Actually, we should probably reset all states? No, only reset when switching if desired.
        // Wait, the prompt says output bleeds. Let's just leave clearCurrentSearch as is but resetting all states.
        _dictState.value = SearchState()
        _compareState.value = SearchState()
        _translateState.value = SearchState()
        _explainState.value = SearchState()
    }""")

# toggleStar
text = re.sub(r'fun toggleStar\(\) \{', r'fun toggleStar(mode: String) {\n        val _uiState = getUiState(mode)', text)

# updateWordStars
text = re.sub(r'fun updateWordStars\(updatedWord: Word\) \{', r'fun updateWordStars(updatedWord: Word, mode: String) {\n        val _uiState = getUiState(mode)', text)

# sendFollowUpMessage
text = re.sub(r'fun sendFollowUpMessage\(userMsgContent: String\) \{', r'fun sendFollowUpMessage(userMsgContent: String, mode: String) {\n        val _uiState = getUiState(mode)', text)

# stopStream
text = re.sub(r'fun stopStream\(\) \{', r'fun stopStream(mode: String) {\n        val _uiState = getUiState(mode)', text)

# resumeChat
text = re.sub(r'fun resumeChat\(userMsgContent: String\) \{', r'fun resumeChat(userMsgContent: String, mode: String) {\n        val _uiState = getUiState(mode)', text)

# deleteMessage
text = re.sub(r'fun deleteMessage\(msg: ChatMessage\) \{', r'fun deleteMessage(msg: ChatMessage, mode: String) {\n        val _uiState = getUiState(mode)', text)

# retryMessage
text = re.sub(r'fun retryMessage\(msg: ChatMessage, useFallback: Boolean = false\) \{', r'fun retryMessage(msg: ChatMessage, useFallback: Boolean = false, mode: String) {\n        val _uiState = getUiState(mode)', text)


with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

print("Updated SearchViewModel")
