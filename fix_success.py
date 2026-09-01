import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

target = 'val newAssistantMsg = com.aidict.app.data.entities.ChatMessage(wordId = assistantMsg.wordId, role = "assistant", content = finalMarkdown)'
replacement = 'val newAssistantMsg = loadingMsg.copy(content = finalMarkdown)'

text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

print("Fixed success branch")
