package com.aidict.app.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aidict.app.data.AppDatabase
import com.aidict.app.data.LlmRepository
import com.aidict.app.data.entities.ChatMessage
import com.aidict.app.data.entities.Word
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class ExplainViewModel(private val repository: LlmRepository, private val database: AppDatabase) : ViewModel() {
    private val _uiState = MutableStateFlow(SearchState())
    val uiState: StateFlow<SearchState> = _uiState.asStateFlow()

    fun streamExplain(text: String, profileId: Int) {
        viewModelScope.launch {
            _uiState.value = SearchState(isLoading = true, currentStream = "")
            try {
                repository.streamExplain(text).collect {
                    _uiState.value = _uiState.value.copy(currentStream = it)
                }

                val finalMarkdown = _uiState.value.currentStream
                val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
                val sessionId = sdf.format(Date())
                val word = Word(profileId = profileId, term = text, sessionId = sessionId, mode = "explain")
                val wordId = database.appDao().insertWord(word).toInt()
                val savedWord = word.copy(id = wordId)

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
}
