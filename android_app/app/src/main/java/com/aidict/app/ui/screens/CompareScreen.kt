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
import androidx.compose.ui.platform.LocalContext
import com.aidict.app.ui.components.MarkdownText
import androidx.compose.ui.unit.dp

@Composable
fun CompareScreen(
    viewModel: com.aidict.app.ui.viewmodels.SearchViewModel, profileId: Int,
    autoNewSearch: Boolean = false,
    onToggleAutoNewSearch: () -> Unit = {},
    enterToSend: Boolean = false,
    modifier: Modifier = Modifier
) {
    val state by viewModel.compareState.collectAsState()
    var sourceLang by remember { mutableStateOf("Auto Detect") }
    var targetLang by remember { mutableStateOf("English") }
    LaunchedEffect(profileId) {
        sourceLang = viewModel.getProfileSetting(profileId, "COMPARE_SOURCE") ?: "Auto Detect"
        targetLang = viewModel.getProfileSetting(profileId, "COMPARE_TARGET") ?: "English"
    }
    
    val context = LocalContext.current
    val clipboardManager = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager

    Column(modifier = modifier.fillMaxSize().padding(16.dp)) {
        // Chat History & Streaming
        state.error?.let {
            Text(text = "Error: $it", color = MaterialTheme.colorScheme.error)
            Spacer(modifier = Modifier.height(8.dp))
        }
        state.word?.let { word ->
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = androidx.compose.foundation.layout.Arrangement.End) {
                Text(
                    text = "Searches: ${word.searchCount} | Views: ${word.viewCount}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        LazyColumn(modifier = Modifier.weight(1f)) {
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
                                MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onPrimary)
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
                                                viewModel.editMessage(msg, editingContent, "compare")
                                                isEditing = false 
                                            }) { Text("Save", color = MaterialTheme.colorScheme.primary) }
                                        }
                                    }
                                } else {
                                    MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer)
                                }
                            }
                        }
                        if (!isUser && !isEditing) {
                            Row(modifier = Modifier.fillMaxWidth(0.85f), horizontalArrangement = Arrangement.Start) {
                                IconButton(onClick = {
                                    val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                                    clipboard.setPrimaryClip(ClipData.newPlainText("AI Dict", msg.content))
                                    Toast.makeText(context, "Copied", Toast.LENGTH_SHORT).show()
                                }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.ContentCopy, "Copy", modifier = Modifier.size(16.dp)) }
                                IconButton(onClick = { isEditing = true; editingContent = msg.content }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Edit, "Edit", modifier = Modifier.size(16.dp)) }
                                IconButton(onClick = { viewModel.retryMessage(msg, true, "compare") }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Refresh, "Regenerate", modifier = Modifier.size(16.dp)) }
                                IconButton(onClick = { viewModel.deleteMessage(msg, "compare") }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Delete, "Delete", modifier = Modifier.size(16.dp)) }
                            }
                        }
                    }
                }
            }
            
            // Current stream
            if (state.isLoading && state.currentStream.isNotEmpty()) {
                item {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Start) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth(0.85f)
                                .padding(vertical = 4.dp)
                                .background(color = MaterialTheme.colorScheme.secondaryContainer, shape = RoundedCornerShape(12.dp))
                                .padding(12.dp)
                        ) {
                            Text(text = state.currentStream, color = MaterialTheme.colorScheme.onSecondaryContainer)
                        }
                    }
                }
            }
            
            if (state.isLoading && state.currentStream.isEmpty()) {
                item { com.aidict.app.ui.components.PulsingDots(modifier = Modifier.fillMaxWidth().wrapContentWidth(androidx.compose.ui.Alignment.CenterHorizontally)) }
            }
        }

        com.aidict.app.ui.components.ChatInputBar(
            availableLanguages = viewModel.orderedLanguages.collectAsState().value,
            inputTerm = viewModel.compareInput,
            onValueChange = { viewModel.compareInput = it },
            onSend = { 
                val query = viewModel.compareInput
                if (autoNewSearch && state.word != null) { 
                    viewModel.clearCurrentSearch()
                    viewModel.streamCompare(query, sourceLang, targetLang, profileId) 
                } else if (state.word != null) {
                    viewModel.sendFollowUpMessage(query, "compare") 
                } else {
                    viewModel.streamCompare(query, sourceLang, targetLang, profileId)
                }
                viewModel.compareInput = "" 
            },
            isLoading = state.isLoading,
            autoNewSearch = autoNewSearch,
            onToggleAutoNewSearch = onToggleAutoNewSearch,
            enterToSend = enterToSend,
            isFollowUp = state.word != null,
            sourceLang = if (state.word == null) sourceLang else null,
            targetLang = if (state.word == null) targetLang else null,
            onSourceLangChange = if (state.word == null) { { sourceLang = it; viewModel.saveProfileSetting(profileId, "COMPARE_SOURCE", it) } } else null,
            onTargetLangChange = if (state.word == null) { { targetLang = it; viewModel.saveProfileSetting(profileId, "COMPARE_TARGET", it) } } else null,
            onClear = { viewModel.clearCurrentSearch() },
            placeholder = if (state.word != null) "Enter your question..." else "Words to compare (comma separated)..."
        )
    }
}
