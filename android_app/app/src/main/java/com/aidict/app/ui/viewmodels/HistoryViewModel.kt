package com.aidict.app.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aidict.app.data.AppDatabase
import com.aidict.app.data.entities.Word
import com.aidict.app.data.entities.Session
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.map
import com.aidict.app.data.entities.AppSetting
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import kotlinx.coroutines.ExperimentalCoroutinesApi

class HistoryViewModel(private val database: AppDatabase) : ViewModel() {
    private val searchQuery = MutableStateFlow("")
    private val selectedColor = MutableStateFlow<String?>(null)
    private val selectedStars = MutableStateFlow<Int?>(null)
    val currentMode = MutableStateFlow("dict")
    
    val colorFilter: StateFlow<String?> = selectedColor
    val starsFilter: StateFlow<Int?> = selectedStars

    @OptIn(ExperimentalCoroutinesApi::class)
    private val activeProfileId = kotlinx.coroutines.flow.MutableStateFlow(1)
    fun setActiveProfileId(id: Int) { activeProfileId.value = id }

    @OptIn(ExperimentalCoroutinesApi::class)
    private val allHistory = kotlinx.coroutines.flow.combine(currentMode, activeProfileId) { m, p -> Pair(m, p) }.flatMapLatest { (mode, pid) ->
        database.appDao().getWordsByMode(pid, mode)
    }.stateIn(viewModelScope, SharingStarted.Lazily, emptyList())
        
    val sessions = activeProfileId.flatMapLatest { pid -> database.appDao().getSessions(pid.toLong()) }
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())
    
    val activeSessionId = database.appDao().getSettingsFlow().map { settings ->
        settings.find { it.key == "ACTIVE_SESSION_ID" }?.value
    }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, null)

    fun setActiveSession(id: String?) {
        viewModelScope.launch {
            if (id == null) {
                database.appDao().insertSetting(AppSetting("ACTIVE_SESSION_ID", ""))
            } else {
                database.appDao().insertSetting(AppSetting("ACTIVE_SESSION_ID", id))
            }
        }
    }

    val historyState: StateFlow<List<Word>> = combine(
        allHistory, 
        searchQuery, 
        selectedColor, 
        selectedStars
    ) { history, query, color, stars ->
        history.filter { word ->
            val matchQuery = if (query.isBlank()) true else word.term.contains(query, ignoreCase = true)
            val matchColor = if (color == null) true else word.color == color
            val matchStars = if (stars == null) true else word.stars == stars
            matchQuery && matchColor && matchStars
        }
    }.stateIn(viewModelScope, SharingStarted.Lazily, emptyList())
    
    fun setMode(mode: String) {
        currentMode.value = mode
    }

    fun updateSearchQuery(query: String) {
        searchQuery.value = query
    }

    fun setFilterColor(color: String?) {
        selectedColor.value = if (selectedColor.value == color) null else color
    }

    fun setFilterStars(stars: Int?) {
        selectedStars.value = if (selectedStars.value == stars) null else stars
    }
    
    fun createSession(name: String) {
        viewModelScope.launch {
            val s = Session(name = name, profileId = activeProfileId.value.toLong())
            database.appDao().insertSession(s)
            setActiveSession(s.id)
        }
    }
    
    fun renameSession(session: Session, newName: String) {
        viewModelScope.launch {
            database.appDao().insertSession(session.copy(name = newName))
        }
    }
    
    fun deleteSession(session: Session) {
        viewModelScope.launch {
            database.appDao().deleteSession(session)
        }
    }
    
    fun renameWord(word: com.aidict.app.data.entities.Word, newTerm: String) {
        viewModelScope.launch {
            database.appDao().insertWord(word.copy(term = newTerm))
        }
    }
    
    fun deleteWord(word: com.aidict.app.data.entities.Word) {
        viewModelScope.launch {
            database.appDao().deleteWord(word)
        }
    }
    
    val splitFraction = kotlinx.coroutines.flow.MutableStateFlow(0.5f)
    init {
        viewModelScope.launch {
            val saved = database.appDao().getSetting("HISTORY_SPLIT_FRACTION")?.value?.toFloatOrNull()
            if (saved != null) {
                splitFraction.value = saved
            }
        }
    }
    
    fun updateSplitFraction(fraction: Float) {
        splitFraction.value = fraction
        viewModelScope.launch {
            database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("HISTORY_SPLIT_FRACTION", fraction.toString()))
        }
    }

    private val selectedWordId = MutableStateFlow<Int?>(null)
    @OptIn(ExperimentalCoroutinesApi::class)
    val selectedChatMessages = selectedWordId.flatMapLatest { wordId ->
        if (wordId == null) kotlinx.coroutines.flow.flowOf(emptyList())
        else database.appDao().getChatMessages(wordId)
    }.stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    fun setSelectedWordId(wordId: Int?) {
        selectedWordId.value = wordId
    }
}