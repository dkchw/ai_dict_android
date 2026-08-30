package com.aidict.app.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aidict.app.data.AppDatabase
import com.aidict.app.data.LlmRepository
import com.aidict.app.data.entities.ChatMessage
import com.aidict.app.data.entities.Word
import com.aidict.app.utils.MarkdownParser
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

data class SearchState(
    val isLoading: Boolean = false,
    val word: Word? = null,
    val chatMessages: List<ChatMessage> = emptyList(),
    val currentStream: String = "",
    val error: String? = null
)

class SearchViewModel(
    private val llmRepository: LlmRepository,
    private val database: AppDatabase
) : ViewModel() {

    private val _uiState = MutableStateFlow(SearchState())
    val uiState: StateFlow<SearchState> = _uiState.asStateFlow()


    val orderedLanguages = database.appDao().getSettingsFlow().map { s -> com.aidict.app.utils.LanguageManager.getOrderedLanguages(s.find { it.key == "STARRED_LANGUAGES" }?.value, s.find { it.key == "CUSTOM_LANGUAGES" }?.value) }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, com.aidict.app.utils.LanguageManager.getOrderedLanguages(null, null))

    fun searchWord(term: String, sourceLang: String, targetLang: String, profileId: Int) {
        viewModelScope.launch {
            _uiState.value = SearchState(isLoading = true, currentStream = "")
            
            try {
                llmRepository.streamExplanation(term, sourceLang, targetLang).collect { currentText ->
                    _uiState.value = _uiState.value.copy(currentStream = currentText)
                }

                val finalMarkdown = _uiState.value.currentStream
                val (language, lemma) = MarkdownParser.extractMetadata(finalMarkdown)
                
                // Save Word
                val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
                val sessionId = sdf.format(Date())
                val word = Word(profileId = profileId, term = term, language = language, lemma = lemma, sessionId = sessionId, mode = "dict")
                val wordId = database.appDao().insertWord(word).toInt()
                val savedWord = word.copy(id = wordId)

                // Save Assistant Message
                val assistantMsg = ChatMessage(wordId = wordId, role = "assistant", content = finalMarkdown)
                val msgId = database.appDao().insertChatMessage(assistantMsg).toInt()
                
                _uiState.value = SearchState(
                    isLoading = false, 
                    word = savedWord, 
                    chatMessages = listOf(assistantMsg.copy(id = msgId)),
                    currentStream = ""
                )

            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }

    fun deleteCurrentWord() {
        viewModelScope.launch {
            _uiState.value.word?.let {
                database.appDao().deleteWord(it)
                _uiState.value = SearchState() // Reset
            }
        }
    }

    fun updateWordColor(color: String) {
        viewModelScope.launch {
            _uiState.value.word?.let { word ->
                val updatedWord = word.copy(color = color)
                database.appDao().insertWord(updatedWord) // REPLACE strategy
                _uiState.value = _uiState.value.copy(word = updatedWord)
            }
        }
    }

    fun updateWordStars(stars: Int) {
        viewModelScope.launch {
            _uiState.value.word?.let { word ->
                val updatedWord = word.copy(stars = stars)
                database.appDao().insertWord(updatedWord)
                _uiState.value = _uiState.value.copy(word = updatedWord)
            }
        }
    }

    fun sendFollowUpMessage(content: String) {
        val word = _uiState.value.word ?: return
        viewModelScope.launch {
            val userMsg = ChatMessage(wordId = word.id, role = "user", content = content)
            val userMsgId = database.appDao().insertChatMessage(userMsg).toInt()
            
            val updatedMessages = _uiState.value.chatMessages + userMsg.copy(id = userMsgId)
            _uiState.value = _uiState.value.copy(chatMessages = updatedMessages, isLoading = true, currentStream = "")

            try {
                llmRepository.streamChat(updatedMessages).collect { currentText ->
                    _uiState.value = _uiState.value.copy(currentStream = currentText)
                }

                val finalMarkdown = _uiState.value.currentStream
                val assistantMsg = ChatMessage(wordId = word.id, role = "assistant", content = finalMarkdown)
                val assistantMsgId = database.appDao().insertChatMessage(assistantMsg).toInt()

                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    chatMessages = updatedMessages + assistantMsg.copy(id = assistantMsgId),
                    currentStream = ""
                )

            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }

    suspend fun getProfileSetting(profileId: Int, key: String): String? {
        return kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
            database.appDao().getSetting("PROFILE_${profileId}_$key")?.value
        }
    }

    fun saveProfileSetting(profileId: Int, key: String, value: String) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("PROFILE_${profileId}_$key", value))
        }
    }

    fun clearCurrentSearch() {
        _uiState.value = SearchState()
    }

    fun deleteMessage(msg: com.aidict.app.data.entities.ChatMessage) {
        viewModelScope.launch {
            database.appDao().deleteChatMessage(msg)
            val updated = database.appDao().getChatMessagesSync(msg.wordId)
            if (updated.isEmpty() || updated.none { it.role == "assistant" }) {
                deleteCurrentWord()
            } else {
                _uiState.value = _uiState.value.copy(chatMessages = updated)
            }
        }
    }

    fun editMessage(msg: com.aidict.app.data.entities.ChatMessage, newContent: String) {
        viewModelScope.launch {
            val updatedMsg = msg.copy(content = newContent)
            database.appDao().insertChatMessage(updatedMsg)
            val updated = database.appDao().getChatMessagesSync(msg.wordId)
            _uiState.value = _uiState.value.copy(chatMessages = updated)
        }
    }

    fun retryMessage(assistantMsg: com.aidict.app.data.entities.ChatMessage, forceFallback: Boolean) {
        viewModelScope.launch {
            // Delete the assistant message to restart generation from that point
            database.appDao().deleteChatMessage(assistantMsg)
            val historyBefore = database.appDao().getChatMessagesSync(assistantMsg.wordId)
            
            _uiState.value = _uiState.value.copy(
                chatMessages = historyBefore,
                isLoading = true,
                currentStream = ""
            )

            try {
                // Determine if this is the first message or a follow-up
                if (historyBefore.size == 1 && historyBefore.first().role == "user") {
                    val userMsg = historyBefore.first()
                    // Re-run searchWord logic essentially, or just stream chat
                    llmRepository.streamChat(historyBefore, forceFallback).collect { currentText ->
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                } else {
                    llmRepository.streamChat(historyBefore, forceFallback).collect { currentText ->
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMarkdown = _uiState.value.currentStream
                val newAssistantMsg = com.aidict.app.data.entities.ChatMessage(wordId = assistantMsg.wordId, role = "assistant", content = finalMarkdown)
                val newId = database.appDao().insertChatMessage(newAssistantMsg).toInt()

                val finalMessages = database.appDao().getChatMessagesSync(assistantMsg.wordId)
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    chatMessages = finalMessages,
                    currentStream = ""
                )

            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)

            }
        }
    }
    fun streamTranslation(text: String, source: String, target: String, profileId: Int) {
        viewModelScope.launch {
            _uiState.value = SearchState(isLoading = true, currentStream = "")
            try {
                llmRepository.streamTranslation(text, source, target).collect {
                    _uiState.value = _uiState.value.copy(currentStream = it)
                }
                val wordId = database.appDao().insertWord(com.aidict.app.data.entities.Word(profileId = profileId, term = text, language = "$source -> $target", sessionId = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date()), mode = "translate")).toInt()
                val msgId = database.appDao().insertChatMessage(com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = _uiState.value.currentStream)).toInt()
                _uiState.value = SearchState(isLoading = false, word = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = text, language = "$source -> $target", mode = "translate", sessionId = ""), chatMessages = listOf(com.aidict.app.data.entities.ChatMessage(id = msgId, wordId = wordId, role = "assistant", content = _uiState.value.currentStream)), currentStream = "")
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }

    fun streamExplain(text: String, profileId: Int) {
        viewModelScope.launch {
            _uiState.value = SearchState(isLoading = true, currentStream = "")
            try {
                llmRepository.streamExplain(text).collect { _uiState.value = _uiState.value.copy(currentStream = it) }
                val wordId = database.appDao().insertWord(com.aidict.app.data.entities.Word(profileId = profileId, term = text, sessionId = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date()), mode = "explain")).toInt()
                val msgId = database.appDao().insertChatMessage(com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = _uiState.value.currentStream)).toInt()
                _uiState.value = SearchState(isLoading = false, word = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = text, mode = "explain", sessionId = ""), chatMessages = listOf(com.aidict.app.data.entities.ChatMessage(id = msgId, wordId = wordId, role = "assistant", content = _uiState.value.currentStream)), currentStream = "")
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }

    fun streamCompare(words: String, profileId: Int) {
        viewModelScope.launch {
            _uiState.value = SearchState(isLoading = true, currentStream = "")
            try {
                llmRepository.streamCompare(words).collect { _uiState.value = _uiState.value.copy(currentStream = it) }
                val wordId = database.appDao().insertWord(com.aidict.app.data.entities.Word(profileId = profileId, term = words, sessionId = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date()), mode = "compare")).toInt()
                val msgId = database.appDao().insertChatMessage(com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = _uiState.value.currentStream)).toInt()
                _uiState.value = SearchState(isLoading = false, word = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = words, mode = "compare", sessionId = ""), chatMessages = listOf(com.aidict.app.data.entities.ChatMessage(id = msgId, wordId = wordId, role = "assistant", content = _uiState.value.currentStream)), currentStream = "")
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }





}
