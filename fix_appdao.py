import re

with open('android_app/app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'r') as f:
    text = f.read()

query = """    @Query("SELECT DISTINCT wordId FROM chat_message WHERE content LIKE '%' || :query || '%'")
    suspend fun getWordIdsMatchingContent(query: String): List<Int>

    @Query("SELECT * FROM word WHERE profileId = :profileId AND mode = :mode ORDER BY createdAt DESC")"""

text = text.replace('    @Query("SELECT * FROM word WHERE profileId = :profileId AND mode = :mode ORDER BY createdAt DESC")', query)

with open('android_app/app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'w') as f:
    f.write(text)

print("Added getWordIdsMatchingContent")
