import re

with open('android_app/app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'r') as f:
    text = f.read()

query = """    @Query("SELECT * FROM word WHERE profileId = :profileId AND mode = :mode AND term LIKE '%' || :query || '%' ORDER BY createdAt DESC LIMIT 5")
    suspend fun getWordSuggestions(profileId: Int, mode: String, query: String): List<Word>

    @Query("SELECT * FROM word WHERE profileId = :profileId AND mode = :mode ORDER BY createdAt DESC")"""

text = text.replace('    @Query("SELECT * FROM word WHERE profileId = :profileId AND mode = :mode ORDER BY createdAt DESC")', query)

with open('android_app/app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'w') as f:
    f.write(text)
print("Added getWordSuggestions")
