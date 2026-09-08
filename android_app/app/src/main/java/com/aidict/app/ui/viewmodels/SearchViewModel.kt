package com.aidict.app.ui.viewmodels

import com.aidict.app.AiDictApplication
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
    private val bgScope = kotlinx.coroutines.CoroutineScope(
        kotlinx.coroutines.Dispatchers.IO + kotlinx.coroutines.SupervisorJob() + kotlinx.coroutines.CoroutineExceptionHandler { _, throwable ->
            android.util.Log.e("SearchViewModel", "Background task exception caught safely", throwable)
        }
    )

    private val _suggestions = MutableStateFlow<List<com.aidict.app.data.entities.Word>>(emptyList())
    val suggestions: StateFlow<List<com.aidict.app.data.entities.Word>> = _suggestions.asStateFlow()

    val isRestartingWordId = MutableStateFlow<Int?>(null)

    fun clearError(mode: String) {
        val _uiState = getUiState(mode)
        _uiState.value = _uiState.value.copy(error = null)
    }

    private fun formatFailureMarkdown(errorDetail: String): String {
        return "⚠️ **Generation Failed**\n\n*Error details:* $errorDetail\n\n*Please check your network connection, API key in Settings, or try with the Fallback Model.*"
    }

    private suspend fun updateSuggestions(mode: String, query: String) {
        if (query.isBlank()) {
            _suggestions.value = emptyList()
            return
        }
        val profileIdStr = database.appDao().getSetting("ACTIVE_PROFILE_ID")?.value
        val profileId = profileIdStr?.toIntOrNull() ?: 1
        _suggestions.value = database.appDao().getWordSuggestions(profileId, mode, query)
    }

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
                updateSuggestions("dict", value)
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
                updateSuggestions("translate", value)
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
                updateSuggestions("explain", value)
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
                updateSuggestions("compare", value)
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
        val cleanTerm = term.trim()
        if (cleanTerm.isBlank()) return
        val _uiState = _dictState
        bgScope.launch {
            var savedMsg: com.aidict.app.data.entities.ChatMessage? = null
            var savedWord: com.aidict.app.data.entities.Word? = null
            try {
                val sessionId = getOrCreateActiveSessionId(profileId)
                val existingWord = database.appDao().findWordExact(profileId, "dict", cleanTerm, null)
                if (existingWord != null) {
                    val existingMsgs = database.appDao().getChatMessagesSync(existingWord.id)
                    val hasValidOutput = existingMsgs.any { it.role == "assistant" && it.content.isNotBlank() && !it.content.startsWith("Generating") && !it.content.contains("Generation Failed") }
                    if (hasValidOutput) {
                        database.appDao().incrementSearchCount(existingWord.id)
                        val updatedWord = existingWord.copy(searchCount = existingWord.searchCount + 1, sessionId = sessionId)
                        database.appDao().updateWord(updatedWord)
                        loadWord(updatedWord)
                        return@launch
                    }
                    savedWord = existingWord
                }
                val wordId = savedWord?.id ?: database.appDao().insertWord(
                    com.aidict.app.data.entities.Word(profileId = profileId, term = cleanTerm, sessionId = sessionId, mode = "dict")
                ).toInt()
                if (savedWord == null) {
                    savedWord = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = cleanTerm, sessionId = sessionId, mode = "dict")
                }
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "Generating...")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                savedMsg = initialMsg.copy(id = msgId)
                
                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "", error = null)
                
                var currentText = ""
                llmRepository.streamExplanation(cleanTerm, sourceLang, targetLang, profileId).collect { chunk ->
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
                val errorDetail = e.localizedMessage?.takeIf { it.isNotBlank() }
                    ?: e.message?.takeIf { it.isNotBlank() }
                    ?: "Network timeout or connection error (${e.javaClass.simpleName})"
                val failureMarkdown = formatFailureMarkdown(errorDetail)
                val wordId = savedWord?.id ?: _uiState.value.word?.id
                if (wordId != null) {
                    try {
                        val userMsg = savedMsg?.copy(content = failureMarkdown)
                            ?: com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = failureMarkdown)
                        database.appDao().insertChatMessage(userMsg)
                    } catch (ignored: Exception) {}
                    val updated = database.appDao().getChatMessagesSync(wordId)
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(isLoading = false, chatMessages = updated, currentStream = "", error = errorDetail)
                    }
                } else {
                    _uiState.value = _uiState.value.copy(isLoading = false, currentStream = "", error = errorDetail)
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
        val cleanContent = content.trim()
        if (cleanContent.isBlank()) return
        val _uiState = getUiState(mode)
        val word = _uiState.value.word ?: return
        val currentWordId = word.id
        bgScope.launch {
            val updatedWordForGen = word.copy(generationCount = word.generationCount + 1)
            database.appDao().updateWord(updatedWordForGen)
            if (_uiState.value.word?.id == currentWordId) {
                _uiState.value = _uiState.value.copy(word = updatedWordForGen)
            }
            val userMsg = ChatMessage(wordId = word.id, role = "user", content = cleanContent)
            database.appDao().insertChatMessage(userMsg)
            
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
                val errorDetail = e.localizedMessage?.takeIf { it.isNotBlank() }
                    ?: e.message?.takeIf { it.isNotBlank() }
                    ?: "Network timeout or connection error (${e.javaClass.simpleName})"
                val failureMarkdown = formatFailureMarkdown(errorDetail)
                try {
                    val errorMsg = ChatMessage(wordId = word.id, role = "assistant", content = failureMarkdown)
                    database.appDao().insertChatMessage(errorMsg)
                } catch (ignored: Exception) {}
                val finalMessages = database.appDao().getChatMessagesSync(word.id)
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false, chatMessages = finalMessages, currentStream = "", error = errorDetail)
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
    fun clearSuggestions() {
        _suggestions.value = emptyList()
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
                deleteCurrentWord(mode)
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
    fun retryMessage(
        assistantMsg: com.aidict.app.data.entities.ChatMessage? = null,
        forceFallback: Boolean = false,
        mode: String = "dict",
        targetWord: com.aidict.app.data.entities.Word? = null
    ) {
        val _uiState = getUiState(mode)
        bgScope.launch {
            val word = targetWord
                ?: _uiState.value.word
                ?: (assistantMsg?.wordId?.let { database.appDao().getWord(it) })
                ?: return@launch
            val currentWordId = word.id
            isRestartingWordId.value = currentWordId

            val updatedWordForGen = word.copy(generationCount = word.generationCount + 1)
            database.appDao().updateWord(updatedWordForGen)

            // Delete the assistant message to restart generation from that point if one was specified
            if (assistantMsg != null) {
                database.appDao().deleteChatMessage(assistantMsg)
            }
            val allHistory = database.appDao().getChatMessagesSync(currentWordId)
            val historyBefore = allHistory.filter {
                it.content.isNotBlank() &&
                !it.content.startsWith("Generating") &&
                !it.content.contains("Generation Failed")
            }
            val loadingMsg = com.aidict.app.data.entities.ChatMessage(
                wordId = currentWordId,
                role = "assistant",
                content = "Generating..."
            )
            val loadingId = database.appDao().insertChatMessage(loadingMsg).toInt()
            val activeLoadingMsg = loadingMsg.copy(id = loadingId)

            val initialDisplay = database.appDao().getChatMessagesSync(currentWordId)
            _uiState.value = _uiState.value.copy(
                word = updatedWordForGen,
                chatMessages = initialDisplay,
                isLoading = true,
                currentStream = "",
                error = null
            )

            try {
                var currentText = ""
                val flow = llmRepository.streamChat(word, historyBefore, forceFallback)

                flow.collect { chunk ->
                    currentText = chunk
                    if (_uiState.value.word?.id == currentWordId) {
                        _uiState.value = _uiState.value.copy(currentStream = currentText)
                    }
                }

                val finalMarkdown = currentText
                val newAssistantMsg = activeLoadingMsg.copy(content = finalMarkdown)
                database.appDao().insertChatMessage(newAssistantMsg)

                val finalMessages = database.appDao().getChatMessagesSync(currentWordId)
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        chatMessages = finalMessages,
                        currentStream = "",
                        error = null
                    )
                }
            } catch (e: Exception) {
                val errorDetail = e.localizedMessage?.takeIf { it.isNotBlank() }
                    ?: e.message?.takeIf { it.isNotBlank() }
                    ?: "Network timeout or connection error (${e.javaClass.simpleName})"
                val failureMarkdown = formatFailureMarkdown(errorDetail)
                try {
                    val errorMsg = activeLoadingMsg.copy(content = failureMarkdown)
                    database.appDao().insertChatMessage(errorMsg)
                } catch (ignored: Exception) {}
                val finalMessages = database.appDao().getChatMessagesSync(currentWordId)
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        chatMessages = finalMessages,
                        currentStream = "",
                        error = errorDetail
                    )
                }
            } finally {
                isRestartingWordId.value = null
                if (_uiState.value.word?.id == currentWordId) {
                    _uiState.value = _uiState.value.copy(isLoading = false)
                }
            }
        }
    }

    fun streamTranslation(text: String, source: String, target: String, profileId: Int) {
        val cleanText = text.trim()
        if (cleanText.isBlank()) return
        val _uiState = _translateState
        bgScope.launch {
            var savedMsg: com.aidict.app.data.entities.ChatMessage? = null
            var savedWord: com.aidict.app.data.entities.Word? = null
            try {
                val sessionId = getOrCreateActiveSessionId(profileId)
                val langKey = "$source -> $target"
                val existingWord = database.appDao().findWordExact(profileId, "translate", cleanText, langKey)
                if (existingWord != null) {
                    val existingMsgs = database.appDao().getChatMessagesSync(existingWord.id)
                    val hasValidOutput = existingMsgs.any { it.role == "assistant" && it.content.isNotBlank() && !it.content.startsWith("Generating") && !it.content.contains("Generation Failed") }
                    if (hasValidOutput) {
                        database.appDao().incrementSearchCount(existingWord.id)
                        val updatedWord = existingWord.copy(searchCount = existingWord.searchCount + 1, sessionId = sessionId)
                        database.appDao().updateWord(updatedWord)
                        loadWord(updatedWord)
                        return@launch
                    }
                    savedWord = existingWord
                }
                val wordId = savedWord?.id ?: database.appDao().insertWord(
                    com.aidict.app.data.entities.Word(profileId = profileId, term = cleanText, language = langKey, sessionId = sessionId, mode = "translate")
                ).toInt()
                if (savedWord == null) {
                    savedWord = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = cleanText, language = langKey, sessionId = sessionId, mode = "translate")
                }
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "Generating...")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                savedMsg = initialMsg.copy(id = msgId)

                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "", error = null)

                var currentText = ""
                llmRepository.streamTranslation(cleanText, source, target, profileId).collect { chunk ->
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
                val errorDetail = e.localizedMessage?.takeIf { it.isNotBlank() }
                    ?: e.message?.takeIf { it.isNotBlank() }
                    ?: "Network timeout or connection error (${e.javaClass.simpleName})"
                val failureMarkdown = formatFailureMarkdown(errorDetail)
                val wordId = savedWord?.id ?: _uiState.value.word?.id
                if (wordId != null) {
                    try {
                        val userMsg = savedMsg?.copy(content = failureMarkdown)
                            ?: com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = failureMarkdown)
                        database.appDao().insertChatMessage(userMsg)
                    } catch (ignored: Exception) {}
                    val updated = database.appDao().getChatMessagesSync(wordId)
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(isLoading = false, chatMessages = updated, currentStream = "", error = errorDetail)
                    }
                } else {
                    _uiState.value = _uiState.value.copy(isLoading = false, currentStream = "", error = errorDetail)
                }
            }
        }
    }
    fun streamExplain(text: String, sourceLang: String, targetLang: String, profileId: Int) {
        val cleanText = text.trim()
        if (cleanText.isBlank()) return
        val _uiState = _explainState
        bgScope.launch {
            var savedMsg: com.aidict.app.data.entities.ChatMessage? = null
            var savedWord: com.aidict.app.data.entities.Word? = null
            try {
                val sessionId = getOrCreateActiveSessionId(profileId)
                val langKey = "$sourceLang -> $targetLang"
                val existingWord = database.appDao().findWordExact(profileId, "explain", cleanText, langKey)
                if (existingWord != null) {
                    val existingMsgs = database.appDao().getChatMessagesSync(existingWord.id)
                    val hasValidOutput = existingMsgs.any { it.role == "assistant" && it.content.isNotBlank() && !it.content.startsWith("Generating") && !it.content.contains("Generation Failed") }
                    if (hasValidOutput) {
                        database.appDao().incrementSearchCount(existingWord.id)
                        val updatedWord = existingWord.copy(searchCount = existingWord.searchCount + 1, sessionId = sessionId)
                        database.appDao().updateWord(updatedWord)
                        loadWord(updatedWord)
                        return@launch
                    }
                    savedWord = existingWord
                }
                val wordId = savedWord?.id ?: database.appDao().insertWord(
                    com.aidict.app.data.entities.Word(profileId = profileId, term = cleanText, language = langKey, sessionId = sessionId, mode = "explain")
                ).toInt()
                if (savedWord == null) {
                    savedWord = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = cleanText, language = langKey, sessionId = sessionId, mode = "explain")
                }
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "Generating...")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                savedMsg = initialMsg.copy(id = msgId)

                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "", error = null)

                var currentText = ""
                llmRepository.streamExplain(cleanText, sourceLang, targetLang, profileId).collect { chunk ->
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
                val errorDetail = e.localizedMessage?.takeIf { it.isNotBlank() }
                    ?: e.message?.takeIf { it.isNotBlank() }
                    ?: "Network timeout or connection error (${e.javaClass.simpleName})"
                val failureMarkdown = formatFailureMarkdown(errorDetail)
                val wordId = savedWord?.id ?: _uiState.value.word?.id
                if (wordId != null) {
                    try {
                        val userMsg = savedMsg?.copy(content = failureMarkdown)
                            ?: com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = failureMarkdown)
                        database.appDao().insertChatMessage(userMsg)
                    } catch (ignored: Exception) {}
                    val updated = database.appDao().getChatMessagesSync(wordId)
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(isLoading = false, chatMessages = updated, currentStream = "", error = errorDetail)
                    }
                } else {
                    _uiState.value = _uiState.value.copy(isLoading = false, currentStream = "", error = errorDetail)
                }
            }
        }
    }
    fun streamCompare(words: String, sourceLang: String, targetLang: String, profileId: Int) {
        val cleanWords = words.trim()
        if (cleanWords.isBlank()) return
        val _uiState = _compareState
        bgScope.launch {
            var savedMsg: com.aidict.app.data.entities.ChatMessage? = null
            var savedWord: com.aidict.app.data.entities.Word? = null
            try {
                val sessionId = getOrCreateActiveSessionId(profileId)
                val langKey = "$sourceLang -> $targetLang"
                val existingWord = database.appDao().findWordExact(profileId, "compare", cleanWords, langKey)
                if (existingWord != null) {
                    val existingMsgs = database.appDao().getChatMessagesSync(existingWord.id)
                    val hasValidOutput = existingMsgs.any { it.role == "assistant" && it.content.isNotBlank() && !it.content.startsWith("Generating") && !it.content.contains("Generation Failed") }
                    if (hasValidOutput) {
                        database.appDao().incrementSearchCount(existingWord.id)
                        val updatedWord = existingWord.copy(searchCount = existingWord.searchCount + 1, sessionId = sessionId)
                        database.appDao().updateWord(updatedWord)
                        loadWord(updatedWord)
                        return@launch
                    }
                    savedWord = existingWord
                }
                val wordId = savedWord?.id ?: database.appDao().insertWord(
                    com.aidict.app.data.entities.Word(profileId = profileId, term = cleanWords, language = langKey, sessionId = sessionId, mode = "compare")
                ).toInt()
                if (savedWord == null) {
                    savedWord = com.aidict.app.data.entities.Word(id = wordId, profileId = profileId, term = cleanWords, language = langKey, sessionId = sessionId, mode = "compare")
                }
                val initialMsg = com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = "Generating...")
                val msgId = database.appDao().insertChatMessage(initialMsg).toInt()
                savedMsg = initialMsg.copy(id = msgId)

                _uiState.value = SearchState(isLoading = true, word = savedWord, chatMessages = listOf(savedMsg), currentStream = "", error = null)

                var currentText = ""
                llmRepository.streamCompare(cleanWords, sourceLang, targetLang, profileId).collect { chunk ->
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
                val errorDetail = e.localizedMessage?.takeIf { it.isNotBlank() }
                    ?: e.message?.takeIf { it.isNotBlank() }
                    ?: "Network timeout or connection error (${e.javaClass.simpleName})"
                val failureMarkdown = formatFailureMarkdown(errorDetail)
                val wordId = savedWord?.id ?: _uiState.value.word?.id
                if (wordId != null) {
                    try {
                        val userMsg = savedMsg?.copy(content = failureMarkdown)
                            ?: com.aidict.app.data.entities.ChatMessage(wordId = wordId, role = "assistant", content = failureMarkdown)
                        database.appDao().insertChatMessage(userMsg)
                    } catch (ignored: Exception) {}
                    val updated = database.appDao().getChatMessagesSync(wordId)
                    if (_uiState.value.word?.id == wordId) {
                        _uiState.value = _uiState.value.copy(isLoading = false, chatMessages = updated, currentStream = "", error = errorDetail)
                    }
                } else {
                    _uiState.value = _uiState.value.copy(isLoading = false, currentStream = "", error = errorDetail)
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