package com.aidict.app.ui.screens

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Clear

import androidx.compose.material.icons.outlined.StarBorder
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import android.content.Intent
import android.net.Uri
import androidx.compose.ui.platform.LocalContext
import com.aidict.app.ui.components.MarkdownText
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.aidict.app.ui.viewmodels.SearchViewModel

@Composable
fun SearchScreen(
    viewModel: SearchViewModel, profileId: Int,
    modifier: Modifier = Modifier
) {
    val state by viewModel.dictState.collectAsState()
    
    val context = LocalContext.current

    val colors = listOf(
        "Red" to Color(0xFFEF4444),
        "Orange" to Color(0xFFF97316),
        "Yellow" to Color(0xFFEAB308),
        "Green" to Color(0xFF22C55E),
        "Blue" to Color(0xFF3B82F6)
    )

    var sourceLang by remember { mutableStateOf("Auto Detect") }
    var targetLang by remember { mutableStateOf("English") }
    LaunchedEffect(profileId) {
        sourceLang = viewModel.getProfileSetting(profileId, "SEARCH_SOURCE") ?: "Auto Detect"
        targetLang = viewModel.getProfileSetting(profileId, "SEARCH_TARGET") ?: "English"
    }

    Column(modifier = modifier.fillMaxSize().padding(horizontal = 16.dp, vertical = 8.dp)) {

        // Error
        state.error?.let {
            Text(text = "Error: $it", color = MaterialTheme.colorScheme.error)
            Spacer(modifier = Modifier.height(8.dp))
        }

        // Action Bar (Only if word is saved)
        state.word?.let { word ->
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(8.dp))
                    .padding(8.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = "${word.term} ${word.language?.let { "($it)" } ?: ""}",
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.weight(1f)
                    )

                    IconButton(onClick = {
                        val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                        val clip = ClipData.newPlainText("AI Dict", state.chatMessages.firstOrNull()?.content ?: "")
                        clipboard.setPrimaryClip(clip)
                        Toast.makeText(context, "Copied to clipboard", Toast.LENGTH_SHORT).show()
                    }) {
                        Icon(Icons.Default.ContentCopy, contentDescription = "Copy")
                    }

                    IconButton(onClick = { viewModel.deleteCurrentWord() }) {
                        Icon(Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                    }
                }
                
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(top = 4.dp)) {
                    // Colors
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        colors.forEach { (name, colorValue) ->
                            Box(
                                modifier = Modifier
                                    .size(24.dp)
                                    .background(color = colorValue, shape = CircleShape)
                                    .clickable { viewModel.updateWordColor(if (word.color == name) "" else name) }
                                    .padding(2.dp)
                            ) {
                                if (word.color == name) {
                                    Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.5f), CircleShape))
                                }
                            }
                        }
                    }
                    
                    Spacer(Modifier.weight(1f))
                    
                    // Stars
                    Row(horizontalArrangement = Arrangement.spacedBy(2.dp)) {
                        (1..5).forEach { star ->
                            Icon(
                                imageVector = if (word.stars >= star) Icons.Default.Star else Icons.Outlined.StarBorder,
                                contentDescription = "Star $star",
                                tint = if (word.stars >= star) Color(0xFFFFC107) else MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier
                                    .size(24.dp)
                                    .clickable { viewModel.updateWordStars(if (word.stars == star) 0 else star) }
                            )
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(8.dp))
        }

        // Chat History & Streaming
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
                                                viewModel.editMessage(msg, editingContent, "dict")
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
                                IconButton(onClick = { viewModel.retryMessage(msg, false, "dict") }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Refresh, "Retry", modifier = Modifier.size(16.dp)) }
                                IconButton(onClick = { viewModel.retryMessage(msg, true, "dict") }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Warning, "Retry Fallback", modifier = Modifier.size(16.dp)) }
                                IconButton(onClick = { viewModel.deleteMessage(msg, "dict") }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Delete, "Delete", modifier = Modifier.size(16.dp)) }
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

        // Unified Input Bar (Search or Follow Up)
        val isFollowUp = state.word != null


        com.aidict.app.ui.components.ChatInputBar(availableLanguages = viewModel.orderedLanguages.collectAsState().value, 
            inputTerm = viewModel.searchInput,
            onValueChange = { viewModel.searchInput = it },
            onSend = {
                if (isFollowUp) {
                    viewModel.sendFollowUpMessage(viewModel.searchInput, "dict")
                } else {
                    viewModel.searchWord(viewModel.searchInput, sourceLang, targetLang, profileId)
                }
                viewModel.searchInput = ""
            },
            isLoading = state.isLoading,
            placeholder = if (isFollowUp) "Enter your question..." else "Search word...",
            isFollowUp = isFollowUp,
            sourceLang = if (!isFollowUp) sourceLang else null,
            targetLang = if (!isFollowUp) targetLang else null,
            onSourceLangChange = if (!isFollowUp) { { sourceLang = it; viewModel.saveProfileSetting(profileId, "SEARCH_SOURCE", it) } } else null,
            onTargetLangChange = if (!isFollowUp) { { targetLang = it; viewModel.saveProfileSetting(profileId, "SEARCH_TARGET", it) } } else null,
            onClear = { viewModel.clearCurrentSearch(); viewModel.searchInput = "" }
        )
    }
}
