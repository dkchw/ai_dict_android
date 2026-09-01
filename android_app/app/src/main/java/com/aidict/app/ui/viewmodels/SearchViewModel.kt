package com.aidict.app.ui.viewmodels
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.serialization.json.Json
import kotlinx.serialization.decodeFromString
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.SharingStarted
import com.aidict.app.data.AppDatabase
import com.aidict.app.data.LlmRepository
import com.aidict.app.data.entities.ChatMessage
import com.aidict.app.data.entities.Word
import com.aidict.app.utils.MarkdownParser
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
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
    private var dictJob: kotlinx.coroutines.Job? = null
    private var translateJob: kotlinx.coroutines.Job? = null
    private var explainJob: kotlinx.coroutines.Job? = null
    private var compareJob: kotlinx.coroutines.Job? = null

    private val activeStreamJobs = mutableMapOf<String, kotlinx.coroutines.Job>()

    private var _searchInput = mutableStateOf("")
    var searchInput: String
        get() = _searchInput.value
        set(value) {
            _searchInput.value = value
            dictJob?.cancel()
            dictJob = viewModelScope.launch {
                kotlinx.coroutines.delay(300)
                database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("DICT_DRAFT", value))
            }
        }

    private var _translateInput = mutableStateOf("")
    var translateInput: String
        get() = _translateInput.value
        set(value) {
            _translateInput.value = value
            translateJob?.cancel()
            translateJob = viewModelScope.launch {
                kotlinx.coroutines.delay(300)
                database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("TRANSLATE_DRAFT", value))
            }
        }

    private var _explainInput = mutableStateOf("")
    var explainInput: String
        get() = _explainInput.value
        set(value) {
            _explainInput.value = value
            explainJob?.cancel()
            explainJob = viewModelScope.launch {
                kotlinx.coroutines.delay(300)
                database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("EXPLAIN_DRAFT", value))
            }
        }

    private var _compareInput = mutableStateOf("")
    var compareInput: String
        get() = _compareInput.value
        set(value) {
            _compareInput.value = value
            compareJob?.cancel()
            compareJob = viewModelScope.launch {
                kotlinx.coroutines.delay(300)
                database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("COMPARE_DRAFT", value))
            }
        }

    init {
        viewModelScope.launch {
            _searchInput.value = database.appDao().getSetting("DICT_DRAFT")?.value ?: ""
            _translateInput.value = database.appDao().getSetting("TRANSLATE_DRAFT")?.value ?: ""
            _explainInput.value = database.appDao().getSetting("EXPLAIN_DRAFT")?.value ?: ""
            _compareInput.value = database.appDao().getSetting("COMPARE_DRAFT")?.value ?: ""
        }
    }


    private val _dictState = MutableStateFlow(SearchState())
    val dictState: StateFlow<SearchState> = _dictState.asStateFlow()
    
    private val _compareState = MutableStateFlow(SearchState())
    val compareState: StateFlow<SearchState> = _compareState.asStateFlow()
    
    private val _translateState = MutableStateFlow(SearchState())
    val translateState: StateFlow<SearchState> = _translateState.asStateFlow()
    
    private val _explainState = MutableStateFlow(SearchState())
    val explainState: StateFlow<SearchState> = _explainState.asStateFlow()
    
    fun getUiState(mode: String): MutableStateFlow<SearchState> {
        return when (mode) {
            "dict" -> _dictState
            "compare" -> _compareState
            "translate" -> _translateState
            "explain" -> _explainState
            else -> _dictState
        }
    }


    val orderedLanguages = database.appDao().getSettingsFlow().map { s -> com.aidict.app.utils.LanguageManager.getOrderedLanguages(s.find { it.key == "STARRED_LANGUAGES" }?.value, s.find { it.key == "CUSTOM_LANGUAGES" }?.value) }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, com.aidict.app.utils.LanguageManager.getOrderedLanguages(null, null))
    fun searchWord(term: String, sourceLang: String, targetLang: String, profileId: Int) {
        val _uiState = _dictState
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            try {
                val sessionId = getOrCreateActiveSessionId(profileId)
                val existingWord = database.appDao().findWordExact(profileId, "dict", term, null)
                if (existingWord != null) {
                    database.appDao().incrementSearchCount(existingWord.id)
                    val updatedWord = existingWord.copy(searchCount = existingWord.searchCount + 1, sessionId = sessionId)
                    database.appDao().updateWord(updatedWord)
                    loadWord(updatedWord)
                    return@launch
                }
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = term, sessionId = sessionId, mode = "dict")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val savedWord = initialWord.copy(id = wordId)
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                val savedMsg = initialMsg.copy(id = msgId)
                
                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "")
                
                var currentText = ""
                llmRepository.streamExplanation(term, sourceLang, targetLang).collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMarkdown = currentText
                val (language, lemma) = MarkdownParser.extractMetadata(finalMarkdown)
                
                val finalWord = savedWord.copy(language = language, lemma = lemma)
                database.appDao().updateWord(finalWord)
                val finalMsg = savedMsg.copy(content = finalMarkdown)
                database.appDao().insertChatMessage(finalMsg)
                
                if (_uiState.value.word?.id == wordId) {
                    _uiState.value = SearchState(isLoading = false, word = finalWord, chatMessages = listOf(finalMsg), currentStream = "")
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.term == term) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }

    fun deleteCurrentWord(mode: String = "dict") {
        val _uiState = getUiState(mode)
        viewModelScope.launch {
            _uiState.value.word?.let {
                database.appDao().deleteWord(it)
                _uiState.value = SearchState() // Reset
            }
        }
    }

        fun renameWord(word: com.aidict.app.data.entities.Word, newTerm: String, mode: String) {
        val _uiState = getUiState(mode)
        viewModelScope.launch {
            val updatedWord = word.copy(term = newTerm)
            database.appDao().updateWord(updatedWord)
            if (_uiState.value.word?.id == word.id) {
                _uiState.value = _uiState.value.copy(word = updatedWord)
            }
        }
    }

    fun updateWordColor(color: String, mode: String = "dict") {
        val _uiState = getUiState(mode)
        viewModelScope.launch {
            _uiState.value.word?.let { word ->
                val updatedWord = word.copy(color = color)
                database.appDao().updateWord(updatedWord) // REPLACE strategy
                _uiState.value = _uiState.value.copy(word = updatedWord)
            }
        }
    }

    fun updateWordStars(stars: Int, mode: String = "dict") {
        val _uiState = getUiState(mode)
        viewModelScope.launch {
            _uiState.value.word?.let { word ->
                val updatedWord = word.copy(stars = stars)
                database.appDao().updateWord(updatedWord)
                _uiState.value = _uiState.value.copy(word = updatedWord)
            }
        }
    }
    fun sendFollowUpMessage(content: String, mode: String = "dict") {
        val _uiState = getUiState(mode)
        val word = _uiState.value.word ?: return
        val currentWordId = word.id
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            val userMsg = ChatMessage(wordId = word.id, role = "user", content = content)
            val userMsgId = database.appDao().insertChatMessage(userMsg).toInt()
            
            val updatedMessages = database.appDao().getChatMessagesSync(word.id)
            if (_uiState.value.word?.id == currentWordId) {
                _uiState.value = _uiState.value.copy(chatMessages = updatedMessages, isLoading = true, currentStream = "")
            }

            try {
                var currentText = ""
                llmRepository.streamChat(word, updatedMessages).collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == currentWordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }
                val assistantMsg = ChatMessage(wordId = word.id, role = "assistant", content = currentText)
                database.appDao().insertChatMessage(assistantMsg)
                
                val finalMessages = database.appDao().getChatMessagesSync(word.id)
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, chatMessages = finalMessages, currentStream = "")
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
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

    
    fun loadWord(word: com.aidict.app.data.entities.Word) {
        val _uiState = getUiState(word.mode)
        viewModelScope.launch {
            database.appDao().incrementViewCount(word.id)
            val updatedWord = word.copy(viewCount = word.viewCount + 1)
            val messages = database.appDao().getChatMessagesSync(word.id)
            _uiState.value = SearchState(
                word = updatedWord,
                isLoading = false,
                
                chatMessages = messages,
                currentStream = "",
                error = null
            )
        }
    }
    fun clearCurrentSearch() {
        _dictState.value = SearchState()
        _compareState.value = SearchState()
        _translateState.value = SearchState()
        _explainState.value = SearchState()
        
        searchInput = ""
        translateInput = ""
        compareInput = ""
        explainInput = ""
    }

    fun deleteMessage(msg: com.aidict.app.data.entities.ChatMessage, mode: String) {
        val _uiState = getUiState(mode)
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

    fun editMessage(msg: com.aidict.app.data.entities.ChatMessage, newContent: String, mode: String) {
        val _uiState = getUiState(mode)
        viewModelScope.launch {
            val updatedMsg = msg.copy(content = newContent)
            database.appDao().insertChatMessage(updatedMsg)
            val updated = database.appDao().getChatMessagesSync(msg.wordId)
            _uiState.value = _uiState.value.copy(chatMessages = updated)
        }
    }
    fun retryMessage(assistantMsg: com.aidict.app.data.entities.ChatMessage, forceFallback: Boolean, mode: String = "dict") {
        val _uiState = getUiState(mode)
        val word = _uiState.value.word ?: return
        val currentWordId = word.id
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            // Delete the assistant message to restart generation from that point
            database.appDao().deleteChatMessage(assistantMsg)
            val historyBefore = database.appDao().getChatMessagesSync(assistantMsg.wordId)
            
            if (_uiState.value.word?.id == currentWordId) {
                _uiState.value = _uiState.value.copy(
                    chatMessages = historyBefore,
                    isLoading = true,
                    currentStream = ""
                )
            }

            try {
                var currentText = ""
                // Determine if this is the first message or a follow-up
                val flow = if (historyBefore.size == 1 && historyBefore.first().role == "user") {
                    llmRepository.streamChat(word, historyBefore, forceFallback)
                } else {
                    llmRepository.streamChat(word, historyBefore, forceFallback)
                }
                
                flow.collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == currentWordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMarkdown = currentText
                val newAssistantMsg = com.aidict.app.data.entities.ChatMessage(wordId = assistantMsg.wordId, role = "assistant", content = finalMarkdown)
                database.appDao().insertChatMessage(newAssistantMsg)

                val finalMessages = database.appDao().getChatMessagesSync(assistantMsg.wordId)
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        chatMessages = finalMessages,
                        currentStream = ""
                    )
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }
    fun streamTranslation(text: String, source: String, target: String, profileId: Int) {
        val _uiState = _translateState
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            try {
                val sessionId = getOrCreateActiveSessionId(profileId)
                val langKey = "$source -> $target"
                val existingWord = database.appDao().findWordExact(profileId, "translate", text, langKey)
                if (existingWord != null) {
                    database.appDao().incrementSearchCount(existingWord.id)
                    val updatedWord = existingWord.copy(searchCount = existingWord.searchCount + 1, sessionId = sessionId)
                    database.appDao().updateWord(updatedWord)
                    loadWord(updatedWord)
                    return@launch
                }
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = text, language = langKey, sessionId = sessionId, mode = "translate")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val savedWord = initialWord.copy(id = wordId)
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                val savedMsg = initialMsg.copy(id = msgId)

                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "")

                var currentText = ""
                llmRepository.streamTranslation(text, source, target).collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMsg = savedMsg.copy(content = currentText)
                database.appDao().insertChatMessage(finalMsg)
                if (_uiState.value.word?.id == wordId) {
                    _uiState.value = SearchState(isLoading = false, word = savedWord, chatMessages = listOf(finalMsg), currentStream = "")
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.term == text) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }
    fun streamExplain(text: String, sourceLang: String, targetLang: String, profileId: Int) {
        val _uiState = _explainState
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            try {
                val sessionId = getOrCreateActiveSessionId(profileId)
                val langKey = "$sourceLang -> $targetLang"
                val existingWord = database.appDao().findWordExact(profileId, "explain", text, langKey)
                if (existingWord != null) {
                    database.appDao().incrementSearchCount(existingWord.id)
                    val updatedWord = existingWord.copy(searchCount = existingWord.searchCount + 1, sessionId = sessionId)
                    database.appDao().updateWord(updatedWord)
                    loadWord(updatedWord)
                    return@launch
                }
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = text, language = langKey, sessionId = sessionId, mode = "explain")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val savedWord = initialWord.copy(id = wordId)
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                val savedMsg = initialMsg.copy(id = msgId)

                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "")

                var currentText = ""
                llmRepository.streamExplain(text, sourceLang, targetLang).collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMsg = savedMsg.copy(content = currentText)
                database.appDao().insertChatMessage(finalMsg)
                if (_uiState.value.word?.id == wordId) {
                    _uiState.value = SearchState(isLoading = false, word = savedWord, chatMessages = listOf(finalMsg), currentStream = "")
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.term == text) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }
    fun streamCompare(words: String, sourceLang: String, targetLang: String, profileId: Int) {
        val _uiState = _compareState
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            try {
                val sessionId = getOrCreateActiveSessionId(profileId)
                val langKey = "$sourceLang -> $targetLang"
                val existingWord = database.appDao().findWordExact(profileId, "compare", words, langKey)
                if (existingWord != null) {
                    database.appDao().incrementSearchCount(existingWord.id)
                    val updatedWord = existingWord.copy(searchCount = existingWord.searchCount + 1, sessionId = sessionId)
                    database.appDao().updateWord(updatedWord)
                    loadWord(updatedWord)
                    return@launch
                }
                val initialWord = com.aidict.app.data.entities.Word(profileId = profileId, term = words, language = langKey, sessionId = sessionId, mode = "compare")
                val wordId = database.appDao().insertWord(initialWord).toInt()
                val savedWord = initialWord.copy(id = wordId)
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                val savedMsg = initialMsg.copy(id = msgId)

                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "")

                var currentText = ""
                llmRepository.streamCompare(words, sourceLang, targetLang).collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMsg = savedMsg.copy(content = currentText)
                database.appDao().insertChatMessage(finalMsg)
                if (_uiState.value.word?.id == wordId) {
                    _uiState.value = SearchState(isLoading = false, word = savedWord, chatMessages = listOf(finalMsg), currentStream = "")
                }
            } catch (e: Exception) {
                if (_uiState.value.word?.term == words) {
                    _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
                }
            }
        }
    }






    private suspend fun getOrCreateActiveSessionId(profileId: Int): String {
        val activeSessionId = database.appDao().getSetting("ACTIVE_SESSION_ID")?.value
        if (!activeSessionId.isNullOrBlank()) {
            val exists = database.appDao().getSessionsSync(profileId.toLong()).any { it.id == activeSessionId }
            if (exists) return activeSessionId
        }
        val timeName = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).format(java.util.Date())
        
        // Check if there's already a session with today's date for this profile
        val existingToday = database.appDao().getSessionsSync(profileId.toLong()).find { it.name == timeName }
        if (existingToday != null) {
            database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("ACTIVE_SESSION_ID", existingToday.id))
            return existingToday.id
        }
        
        val s = com.aidict.app.data.entities.Session(name = timeName, profileId = profileId.toLong())
        database.appDao().insertSession(s)
        database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("ACTIVE_SESSION_ID", s.id))
        return s.id
    }

}