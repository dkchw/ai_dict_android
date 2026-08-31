import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()
text = text.replace('database.appDao().insertWord(word.copy(term = newTerm))', 'database.appDao().updateWord(word.copy(term = newTerm))')
with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Replace all database.appDao().insertWord(updatedWord) with updateWord
text = text.replace('database.appDao().insertWord(updatedWord)', 'database.appDao().updateWord(updatedWord)')
text = text.replace('database.appDao().insertWord(finalWord)', 'database.appDao().updateWord(finalWord)')

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

