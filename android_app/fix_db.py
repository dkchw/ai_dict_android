with open('app/src/main/java/com/aidict/app/data/AppDatabase.kt', 'r') as f:
    text = f.read()

text = text.replace('import com.aidict.app.data.entities.Word', 'import com.aidict.app.data.entities.Word\nimport com.aidict.app.data.entities.Note')
text = text.replace('Session::class]', 'Session::class, Note::class]')
text = text.replace('version = 4,', 'version = 5,')

mig_4_5 = """
        private val MIGRATION_4_5 = object : androidx.room.migration.Migration(4, 5) {
            override fun migrate(db: androidx.sqlite.db.SupportSQLiteDatabase) {
                db.execSQL("CREATE TABLE IF NOT EXISTS `note` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `title` TEXT NOT NULL, `content` TEXT NOT NULL, `createdAt` INTEGER NOT NULL)")
            }
        }
        fun getDatabase
"""
text = text.replace('fun getDatabase', mig_4_5)
text = text.replace('addMigrations(MIGRATION_1_2, MIGRATION_2_3, MIGRATION_3_4)', 'addMigrations(MIGRATION_1_2, MIGRATION_2_3, MIGRATION_3_4, MIGRATION_4_5)')

with open('app/src/main/java/com/aidict/app/data/AppDatabase.kt', 'w') as f:
    f.write(text)

with open('app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'r') as f:
    dao = f.read()

dao = dao.replace('import com.aidict.app.data.entities.Word', 'import com.aidict.app.data.entities.Word\nimport com.aidict.app.data.entities.Note')

note_dao = """
    @androidx.room.Query("SELECT * FROM note ORDER BY createdAt DESC")
    fun getNotesFlow(): kotlinx.coroutines.flow.Flow<List<Note>>

    @androidx.room.Insert
    suspend fun insertNote(note: Note): Long

    @androidx.room.Update
    suspend fun updateNote(note: Note)

    @androidx.room.Delete
    suspend fun deleteNote(note: Note)

    @androidx.room.Query("DELETE FROM note WHERE id IN (:ids)")
    suspend fun deleteNotesByIds(ids: List<Int>)
}
"""
dao = dao.replace('}', note_dao)

with open('app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'w') as f:
    f.write(dao)

