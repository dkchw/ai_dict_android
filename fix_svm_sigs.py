import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

text = re.sub(r'fun deleteMessage\(msg: com.aidict.app.data.entities.ChatMessage\) \{', r'fun deleteMessage(msg: com.aidict.app.data.entities.ChatMessage, mode: String) {\n        val _uiState = getUiState(mode)', text)
text = re.sub(r'fun retryMessage\(msg: com.aidict.app.data.entities.ChatMessage, useFallback: Boolean = false\) \{', r'fun retryMessage(msg: com.aidict.app.data.entities.ChatMessage, useFallback: Boolean = false, mode: String) {\n        val _uiState = getUiState(mode)', text)

# Double check sendFollowUpMessage
text = re.sub(r'fun sendFollowUpMessage\(userMsgContent: String\) \{', r'fun sendFollowUpMessage(userMsgContent: String, mode: String) {\n        val _uiState = getUiState(mode)', text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

