import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# 1. Modify clearCurrentSearch to NOT cancel jobs
old_clear = """    fun clearCurrentSearch() {
        activeStreamJobs.values.forEach { it.cancel() }
        activeStreamJobs.clear()"""
new_clear = """    fun clearCurrentSearch() {
        // activeStreamJobs.values.forEach { it.cancel() } // Do not cancel, let them finish in background
        // activeStreamJobs.clear()"""
text = text.replace(old_clear, new_clear)

# We will completely replace searchWord, streamTranslation, streamExplain, streamCompare, and sendFollowUpMessage
# to ensure they all follow this pattern:
# 1. DB Insert early
# 2. Set UI State with wordId
# 3. collect { if (uiState.word.id == wordId) update UI }
# 4. Save to DB at the end

# Wait, this is a large change. I will just rewrite the functions using a python script with regex replacing the bodies.
