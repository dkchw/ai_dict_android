package com.aidict.app.data.dao

import androidx.room.*
import com.aidict.app.data.entities.AppSetting
import com.aidict.app.data.entities.ChatMessage
import com.aidict.app.data.entities.Profile
import com.aidict.app.data.entities.Word
import kotlinx.coroutines.flow.Flow

@Dao
interface AppDao {
    @Query("SELECT * FROM profile ORDER BY rank ASC")
    fun getProfiles(): Flow<List<Profile>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertProfile(profile: Profile): Long

    @Query("SELECT * FROM profile WHERE isDefault = 1 LIMIT 1")
    suspend fun getDefaultProfile(): Profile?

    @Query("SELECT * FROM app_setting WHERE `key` = :key")
    suspend fun getSetting(key: String): AppSetting?
    
    @Query("SELECT * FROM app_setting")
    fun getSettingsFlow(): Flow<List<AppSetting>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSetting(setting: AppSetting)

    @Query("SELECT * FROM word WHERE profileId = :profileId AND mode = :mode ORDER BY createdAt DESC")
    fun getWordsByMode(profileId: Int, mode: String): Flow<List<Word>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertWord(word: Word): Long

    @Query("SELECT * FROM word WHERE id = :wordId")
    suspend fun getWord(wordId: Int): Word?

    @Query("SELECT * FROM chat_message WHERE wordId = :wordId ORDER BY createdAt ASC")
    fun getChatMessages(wordId: Int): Flow<List<ChatMessage>>
    @Query("SELECT * FROM chat_message WHERE wordId = :wordId ORDER BY createdAt ASC")
    suspend fun getChatMessagesSync(wordId: Int): List<ChatMessage>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertChatMessage(chatMessage: ChatMessage): Long

    @Delete
    suspend fun deleteWord(word: Word)
    @androidx.room.Delete
    suspend fun deleteChatMessage(msg: com.aidict.app.data.entities.ChatMessage)

    @Delete
    suspend fun deleteProfile(profile: Profile)

    @Query("SELECT * FROM session WHERE profileId = :profileId ORDER BY createdAt DESC")
    fun getSessions(profileId: Long): Flow<List<com.aidict.app.data.entities.Session>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSession(session: com.aidict.app.data.entities.Session)

    @Delete
    suspend fun deleteSession(session: com.aidict.app.data.entities.Session)

    @Query("SELECT * FROM app_setting")
    suspend fun getAllSettings(): List<AppSetting>

    @Query("SELECT * FROM profile")
    suspend fun getAllProfiles(): List<Profile>

    @Query("SELECT * FROM word")
    suspend fun getAllWords(): List<Word>

    @Query("SELECT * FROM chat_message")
    suspend fun getAllChatMessages(): List<ChatMessage>

    @Query("DELETE FROM app_setting")
    suspend fun clearSettings()

    @Query("DELETE FROM profile")
    suspend fun clearProfiles()

    @Query("DELETE FROM word")
    suspend fun clearWords()

    @Query("DELETE FROM chat_message")
    suspend fun clearChatMessages()
}
