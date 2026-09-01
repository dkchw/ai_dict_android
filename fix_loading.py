import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# We need to insert `val loadingMsg = assistantMsg.copy(content = "Generating...") \n database.appDao().insertChatMessage(loadingMsg)`
# right after `val historyBefore = database.appDao().getChatMessagesSync(assistantMsg.wordId)` inside `retryMessage`.

def replace_history_before(match):
    return match.group(0) + """\n            val loadingMsg = assistantMsg.copy(content = "Generating...")\n            database.appDao().insertChatMessage(loadingMsg)"""

text = re.sub(r'val historyBefore = database\.appDao\(\)\.getChatMessagesSync\(assistantMsg\.wordId\)', replace_history_before, text, count=1)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

print("Inserted loadingMsg")
