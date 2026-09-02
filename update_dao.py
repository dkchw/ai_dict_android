import re

with open('android_app/app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'r') as f:
    text = f.read()

queries = """    @Query("UPDATE session SET profileId = :profileId WHERE id IN (:sessionIds)")
    suspend fun moveSessionsByIds(sessionIds: List<String>, profileId: Long)

    @Query("UPDATE word SET profileId = :profileId WHERE sessionId IN (:sessionIds)")
    suspend fun moveWordsBySessionIds(sessionIds: List<String>, profileId: Int)

    @Query("UPDATE word SET profileId = :profileId WHERE id IN (:wordIds)")
    suspend fun moveWordsByIds(wordIds: List<Int>, profileId: Int)
"""

text = text.replace('    @Query("DELETE FROM word WHERE id IN (:wordIds)")', queries + '\n    @Query("DELETE FROM word WHERE id IN (:wordIds)")')

with open('android_app/app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'w') as f:
    f.write(text)

print("Added move queries to AppDao")
