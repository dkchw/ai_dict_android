import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Replace _uiState in searchWord
text = re.sub(r'fun searchWord\((.*?)\) \{', r'fun searchWord(\1) { val _uiState = _dictState', text, count=1, flags=re.DOTALL)
text = re.sub(r'fun compareWords\((.*?)\) \{', r'fun compareWords(\1) { val _uiState = _compareState', text, count=1, flags=re.DOTALL)
text = re.sub(r'fun translateWord\((.*?)\) \{', r'fun translateWord(\1) { val _uiState = _translateState', text, count=1, flags=re.DOTALL)
text = re.sub(r'fun explainWord\((.*?)\) \{', r'fun explainWord(\1) { val _uiState = _explainState', text, count=1, flags=re.DOTALL)

# For resumeChat, sendFollowUpMessage, stopStream, toggleStar, retryMessage, deleteMessage, we need a mode parameter.
# But wait! If they are called from a specific screen, we need to pass the mode to them.
# Let's check how they are called.
