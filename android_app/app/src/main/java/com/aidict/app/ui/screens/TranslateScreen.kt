package com.aidict.app.ui.screens
import androidx.compose.material.icons.Icons




import androidx.compose.foundation.layout.*

import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
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
import androidx.compose.material3.Icon
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import com.aidict.app.ui.components.MarkdownText
import androidx.compose.ui.Alignment
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.ui.unit.dp

@Composable
fun TranslateScreen(
    viewModel: com.aidict.app.ui.viewmodels.SearchViewModel, profileId: Int,
    modifier: Modifier = Modifier
) {
    val state by viewModel.translateState.collectAsState()
    
    val context = LocalContext.current
    val clipboardManager = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    var sourceLang by remember { mutableStateOf("Auto Detect") }
    var targetLang by remember { mutableStateOf("English") }
    LaunchedEffect(profileId) {
        sourceLang = viewModel.getProfileSetting(profileId, "TRANSLATE_SOURCE") ?: "Auto Detect"
        targetLang = viewModel.getProfileSetting(profileId, "TRANSLATE_TARGET") ?: "English"
    }
    
    Column(modifier = modifier.fillMaxSize().padding(16.dp)) {
        // Chat History & Streaming
        state.error?.let {
            Text(text = "Error: $it", color = MaterialTheme.colorScheme.error)
            Spacer(modifier = Modifier.height(8.dp))
        }
        LazyColumn(modifier = Modifier.weight(1f)) {
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
                                                viewModel.editMessage(msg, editingContent, "translate")
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
                                IconButton(onClick = { viewModel.retryMessage(msg, false, "translate") }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Refresh, "Retry", modifier = Modifier.size(16.dp)) }
                                IconButton(onClick = { viewModel.retryMessage(msg, true, "translate") }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Warning, "Retry Fallback", modifier = Modifier.size(16.dp)) }
                                IconButton(onClick = { viewModel.deleteMessage(msg, "translate") }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Delete, "Delete", modifier = Modifier.size(16.dp)) }
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
                item { CircularProgressIndicator(modifier = Modifier.padding(16.dp)) }
            }
        }

        // Bottom Input Bar

        com.aidict.app.ui.components.ChatInputBar(availableLanguages = viewModel.orderedLanguages.collectAsState().value, 
            inputTerm = viewModel.translateInput,
            onValueChange = { viewModel.translateInput = it },
            onSend = {
                if (state.word != null) {
                    viewModel.sendFollowUpMessage(viewModel.translateInput, "translate")
                } else {
                    viewModel.streamTranslation(viewModel.translateInput, sourceLang, targetLang, profileId)
                }
                viewModel.translateInput = ""
            },
            isLoading = state.isLoading,
            isFollowUp = state.word != null,
            onClear = { viewModel.clearCurrentSearch() },
            placeholder = if (state.word != null) "Enter your question..." else "Text to translate...",
            sourceLang = sourceLang,
            targetLang = targetLang,
            onSourceLangChange = { sourceLang = it; viewModel.saveProfileSetting(profileId, "TRANSLATE_SOURCE", it) },
            onTargetLangChange = { targetLang = it; viewModel.saveProfileSetting(profileId, "TRANSLATE_TARGET", it) }
        )
    }
}
