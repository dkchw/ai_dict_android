import re

with open('android_app/app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'r') as f:
    text = f.read()

update_code = """    @androidx.room.Update
    suspend fun updateWord(word: Word)
"""
if 'fun updateWord(word: Word)' not in text:
    text = text.replace('suspend fun insertWord(word: Word): Long\n', 'suspend fun insertWord(word: Word): Long\n\n' + update_code)

with open('android_app/app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'w') as f:
    f.write(text)

