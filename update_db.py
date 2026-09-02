import re

# 1. Update Entities.kt
with open('android_app/app/src/main/java/com/aidict/app/data/entities/Entities.kt', 'r') as f:
    text = f.read()

text = text.replace("val viewCount: Int = 0,", "val viewCount: Int = 0,\n    val generationCount: Int = 1,")

with open('android_app/app/src/main/java/com/aidict/app/data/entities/Entities.kt', 'w') as f:
    f.write(text)

# 2. Update AppDatabase.kt
with open('android_app/app/src/main/java/com/aidict/app/data/AppDatabase.kt', 'r') as f:
    text = f.read()

# Change version = 6 to version = 7
text = text.replace("version = 6,", "version = 7,")

migration_6_7 = """        private val MIGRATION_6_7 = object : androidx.room.migration.Migration(6, 7) {
            override fun migrate(db: androidx.sqlite.db.SupportSQLiteDatabase) {
                db.execSQL("ALTER TABLE word ADD COLUMN generationCount INTEGER NOT NULL DEFAULT 1")
            }
        }
        fun getDatabase"""

text = text.replace("fun getDatabase", migration_6_7)
text = text.replace("MIGRATION_4_5, MIGRATION_5_6)", "MIGRATION_4_5, MIGRATION_5_6, MIGRATION_6_7)")

with open('android_app/app/src/main/java/com/aidict/app/data/AppDatabase.kt', 'w') as f:
    f.write(text)

print("DB migration applied")
