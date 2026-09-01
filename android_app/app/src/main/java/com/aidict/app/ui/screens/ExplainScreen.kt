package com.aidict.app.ui.screens

import androidx.compose.material.icons.filled.Check
import androidx.compose.foundation.layout.wrapContentWidth


import androidx.compose.foundation.layout.*
import androidx.compose.foundation.gestures.Orientation
import androidx.compose.foundation.gestures.scrollable
import androidx.compose.foundation.rememberScrollState

import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Warning
import androidx.compose.ui.platform.LocalContext
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import android.content.Intent
import android.net.Uri
import androidx.compose.ui.platform.LocalContext
import com.aidict.app.ui.components.MarkdownText
import androidx.compose.ui.unit.dp

@Composable
fun ExplainScreen(
    viewModel: com.aidict.app.ui.viewmodels.SearchViewModel, profileId: Int,
    autoNewSearch: Boolean = false,
    onToggleAutoNewSearch: () -> Unit = {},
    enterToSend: Boolean = false,
    modifier: Modifier = Modifier
) {
    val state by viewModel.explainState.collectAsState()

    var sourceLang by remember { mutableStateOf("Auto Detect") }
    var targetLang by remember { mutableStateOf("English") }
    LaunchedEffect(profileId) {
        sourceLang = viewModel.getProfileSetting(profileId, "EXPLAIN_SOURCE") ?: "Auto Detect"
        targetLang = viewModel.getProfileSetting(profileId, "EXPLAIN_TARGET") ?: "English"
    }
    
    val context = LocalContext.current
    val clipboardManager = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager

    Column(modifier = modifier.fillMaxSize().padding(16.dp)) {
        Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
            if (state.isLoading && state.currentStream.isEmpty()) {
                com.aidict.app.ui.components.PulsingDots(modifier = Modifier.align(androidx.compose.ui.Alignment.Center))
            } else {
                androidx.compose.foundation.lazy.LazyColumn(modifier = Modifier.fillMaxSize()) {
                    if (state.chatMessages.isEmpty()) {
                        item { Spacer(modifier = Modifier.fillParentMaxSize()) }
                    }
                    items(state.chatMessages) { msg ->
                        var isEditing by remember { mutableStateOf(false) }
                        var editingContent by remember { mutableStateOf("") }
                        val isUser = msg.role == "user"
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
                        ) {
                            Column(modifier = Modifier.fillMaxWidth(if (isUser) 0.85f else 1f)) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth(if (isUser) 1f else 0.85f)
                                        .padding(vertical = 4.dp)
                                        .background(
                                            color = if (isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.secondaryContainer,
                                            shape = RoundedCornerShape(12.dp)
                                        )
                                        .padding(12.dp)
                                ) {
                                    if (isUser) {
                                        com.aidict.app.ui.components.MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onPrimary)
                                    } else {
                                        if (isEditing) {
                                            Column {
                                                OutlinedTextField(
                                                    value = editingContent,
                                                    onValueChange = { editingContent = it },
                                                    modifier = Modifier.fillMaxWidth()
                                                )
                                                Row(horizontalArrangement = Arrangement.End, modifier = Modifier.fillMaxWidth()) {
                                                    TextButton(onClick = { isEditing = false }) { Text("Cancel", color = MaterialTheme.colorScheme.primary) }
                                                    TextButton(onClick = { 
                                                        viewModel.editMessage(msg, editingContent, "explain")
                                                        isEditing = false 
                                                    }) { Text("Save", color = MaterialTheme.colorScheme.primary) }
                                                }
                                            }
                                        } else {
                                            com.aidict.app.ui.components.MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer)
                                        }
                                    }
                                }
                                if (!isUser && !isEditing) {
                                    Row(modifier = Modifier.fillMaxWidth(0.85f), horizontalArrangement = Arrangement.Start) {
                                        IconButton(onClick = {
                                            val clip = ClipData.newPlainText("AI Dict", msg.content)
                                            clipboardManager.setPrimaryClip(clip)
                                            Toast.makeText(context, "Copied to clipboard", Toast.LENGTH_SHORT).show()
                                        }) { Icon(Icons.Default.ContentCopy, contentDescription = "Copy", modifier = Modifier.size(16.dp)) }
                                        IconButton(onClick = { 
                                            editingContent = msg.content
                                            isEditing = true 
                                        }) { Icon(Icons.Default.Edit, contentDescription = "Edit", modifier = Modifier.size(16.dp)) }
                                        IconButton(onClick = { viewModel.retryMessage(msg, false, "explain") }) { Icon(Icons.Default.Refresh, contentDescription = "Retry", modifier = Modifier.size(16.dp)) }
                                        IconButton(onClick = { viewModel.deleteMessage(msg, "explain") }) { Icon(Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(16.dp)) }
                                    }
                                }
                            }
                        }
                    }
                    if (state.isLoading && state.currentStream.isNotEmpty()) {
                        item {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth(0.85f)
                                    .padding(vertical = 4.dp)
                                    .background(MaterialTheme.colorScheme.secondaryContainer, RoundedCornerShape(12.dp))
                                    .padding(12.dp)
                            ) {
                                com.aidict.app.ui.components.MarkdownText(text = state.currentStream, color = MaterialTheme.colorScheme.onSecondaryContainer)
                            }
                        }
                    }
                    state.error?.let {
                        item { Text(text = "Error: $it", color = MaterialTheme.colorScheme.error) }
                    }
                }
            }
        }

        com.aidict.app.ui.components.ChatInputBar(
            availableLanguages = viewModel.orderedLanguages.collectAsState().value,
            inputTerm = viewModel.explainInput,
            onValueChange = { viewModel.explainInput = it },
            onSend = {
                val query = viewModel.explainInput
                if (autoNewSearch && state.word != null) {
                    viewModel.clearCurrentSearch()
                    viewModel.explainInput = query
                    viewModel.streamExplain(query, sourceLang, targetLang, profileId)
                } else if (state.word != null) {
                    viewModel.sendFollowUpMessage(query, "explain")
                } else {
                    viewModel.streamExplain(query, sourceLang, targetLang, profileId)
                }
                viewModel.explainInput = ""
            },
            isLoading = state.isLoading,
            autoNewSearch = autoNewSearch,
            onToggleAutoNewSearch = onToggleAutoNewSearch,
            enterToSend = enterToSend,
            isFollowUp = state.word != null,
            sourceLang = if (state.word == null) sourceLang else null,
            targetLang = if (state.word == null) targetLang else null,
            onSourceLangChange = if (state.word == null) { { sourceLang = it; viewModel.saveProfileSetting(profileId, "EXPLAIN_SOURCE", it) } } else null,
            onTargetLangChange = if (state.word == null) { { targetLang = it; viewModel.saveProfileSetting(profileId, "EXPLAIN_TARGET", it) } } else null,
            onClear = { viewModel.clearCurrentSearch() },
            placeholder = if (state.word != null && !autoNewSearch) "Enter your question..." else "Paste sentence/paragraph to explain..."
        )
    }
}
