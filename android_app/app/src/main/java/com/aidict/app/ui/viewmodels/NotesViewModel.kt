package com.aidict.app.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aidict.app.data.AppDatabase
import com.aidict.app.data.entities.Note
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class NotesViewModel(private val database: AppDatabase) : ViewModel() {
    val notes = database.appDao().getNotesFlow().stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    fun addNote(title: String, content: String) {
        viewModelScope.launch {
            database.appDao().insertNote(Note(title = title, content = content))
        }
    }

    fun updateNote(note: Note) {
        viewModelScope.launch {
            database.appDao().updateNote(note)
        }
    }

    fun deleteNote(note: Note) {
        viewModelScope.launch {
            database.appDao().deleteNote(note)
        }
    }

    fun deleteNotes(ids: List<Int>) {
        viewModelScope.launch {
            database.appDao().deleteNotesByIds(ids)
        }
    }
}
