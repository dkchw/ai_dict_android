import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()

# Add moveWord and moveSelected functions
move_functions = """    fun moveWord(word: com.aidict.app.data.entities.Word, targetProfileId: Int) {
        viewModelScope.launch {
            database.appDao().updateWord(word.copy(profileId = targetProfileId))
        }
    }

    fun moveSelected(sessionIds: Set<String>, wordIds: Set<Int>, targetProfileId: Int) {
        viewModelScope.launch {
            if (sessionIds.isNotEmpty()) {
                database.appDao().moveSessionsByIds(sessionIds.toList(), targetProfileId.toLong())
                // All words within these sessions should ALSO be moved!
                database.appDao().moveWordsBySessionIds(sessionIds.toList(), targetProfileId)
            }
            if (wordIds.isNotEmpty()) {
                database.appDao().moveWordsByIds(wordIds.toList(), targetProfileId)
            }
        }
    }
"""

# Insert right before deleteSelectedWords
text = text.replace("    fun deleteSelectedWords(wordIds: Set<Int>) {", move_functions + "\n    fun deleteSelectedWords(wordIds: Set<Int>) {")

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)

print("Added move logic to HistoryViewModel")
