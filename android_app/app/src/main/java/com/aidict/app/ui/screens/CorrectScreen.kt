package com.aidict.app.ui.screens

import androidx.compose.material.icons.filled.Check
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.ContentPaste
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Autorenew
import androidx.compose.material.icons.automirrored.filled.CompareArrows
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.outlined.StarBorder
import androidx.compose.ui.platform.LocalContext
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import android.speech.tts.TextToSpeech
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.CloudDownload
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.Language
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import com.aidict.app.ui.components.ManageOfflineModelsDialog
import com.aidict.app.ui.components.MarkdownText
import com.aidict.app.ui.components.PulsingDots
import com.aidict.app.ui.components.MoveModeDialog
import com.aidict.app.ui.components.ChatInputBar

@Composable
fun CorrectScreen(
    viewModel: com.aidict.app.ui.viewmodels.SearchViewModel,
    profileId: Int,
    autoNewSearch: Boolean = false,
    onToggleAutoNewSearch: () -> Unit = {},
    enterToSend: Boolean = false,
    onMoveToMode: (com.aidict.app.data.entities.Word, String) -> Unit = { _, _ -> },
    modifier: Modifier = Modifier
) {
    val state by viewModel.correctState.collectAsState()
    val suggestions by viewModel.suggestions.collectAsState()

    var sourceLang by remember { mutableStateOf("Auto Detect") }
    var targetLang by remember { mutableStateOf("English") }
    var correctType by remember { mutableStateOf("both") }
    var mtTier by remember { mutableStateOf(com.aidict.app.data.LocalTranslationEngine.Tier.NORMAL) }

    LaunchedEffect(profileId) {
        sourceLang = viewModel.getProfileSetting(profileId, "CORRECT_SOURCE") ?: "Auto Detect"
        targetLang = viewModel.getProfileSetting(profileId, "CORRECT_TARGET") ?: "English"
        correctType = viewModel.getProfileSetting(profileId, "CORRECT_TYPE") ?: "both"
        val tierStr = viewModel.getProfileSetting(profileId, "CORRECT_MT_TIER") ?: "normal"
        mtTier = if (tierStr == "strong") com.aidict.app.data.LocalTranslationEngine.Tier.STRONG else com.aidict.app.data.LocalTranslationEngine.Tier.NORMAL
    }

    val context = LocalContext.current
    var isChatSearching by remember { mutableStateOf(false) }
    var chatSearchQuery by remember { mutableStateOf("") }
    var showMoveToModeDialog by remember { mutableStateOf(false) }
    var showRenameDialog by remember { mutableStateOf(false) }
    val clipboardManager = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager

    var tts by remember { mutableStateOf<TextToSpeech?>(null) }
    var isTtsReady by remember { mutableStateOf(false) }

    DisposableEffect(context) {
        val ttsInstance = TextToSpeech(context) { status ->
            if (status == TextToSpeech.SUCCESS) {
                isTtsReady = true
            }
        }
        tts = ttsInstance
        onDispose {
            ttsInstance.stop()
            ttsInstance.shutdown()
        }
    }

    fun speakText(text: String, langName: String) {
        if (!isTtsReady || tts == null || text.isBlank()) return
        val tag = com.aidict.app.data.LocalTranslationEngine.getLanguageTag(langName) ?: "en"
        val locale = java.util.Locale.forLanguageTag(tag)
        tts?.language = locale
        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "correct_tts_${System.currentTimeMillis()}")
    }

    val colors = listOf(
        "Red" to Color(0xFFEF4444),
        "Orange" to Color(0xFFF97316),
        "Yellow" to Color(0xFFEAB308),
        "Green" to Color(0xFF22C55E),
        "Blue" to Color(0xFF3B82F6),
        "Purple" to Color(0xFFA855F7)
    )

    Column(modifier = modifier.fillMaxSize().padding(16.dp)) {
        if (correctType == "machine_translate") {
            NormalTranslatorView(
                viewModel = viewModel,
                profileId = profileId,
                sourceLang = sourceLang,
                targetLang = targetLang,
                mtTier = mtTier,
                onSourceLangChange = {
                    sourceLang = it
                    viewModel.saveProfileSetting(profileId, "CORRECT_SOURCE", it)
                },
                onTargetLangChange = {
                    targetLang = it
                    viewModel.saveProfileSetting(profileId, "CORRECT_TARGET", it)
                },
                onMtTierChange = {
                    mtTier = it
                    viewModel.saveProfileSetting(profileId, "CORRECT_MT_TIER", it.id)
                },
                onSwitchMode = { newType ->
                    correctType = newType
                    viewModel.saveProfileSetting(profileId, "CORRECT_TYPE", newType)
                },
                onDeepenWithLlm = {
                    correctType = "both"
                    viewModel.saveProfileSetting(profileId, "CORRECT_TYPE", "both")
                    viewModel.streamCorrect(viewModel.mtSourceText, sourceLang, targetLang, profileId, isCorrectionOnly = false)
                },
                onSpeak = { text, lang -> speakText(text, lang) }
            )
        } else {
            // Error Banner
            state.error?.let { errorMsg ->
            Card(
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer),
                shape = RoundedCornerShape(8.dp),
                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Warning, contentDescription = "Error", tint = MaterialTheme.colorScheme.error)
                        Spacer(Modifier.width(8.dp))
                        Text(
                            text = errorMsg,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onErrorContainer,
                            modifier = Modifier.weight(1f)
                        )
                        IconButton(onClick = { viewModel.clearError("correct") }, modifier = Modifier.size(24.dp)) {
                            Icon(Icons.Default.Clear, contentDescription = "Dismiss", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                    Spacer(Modifier.height(8.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(
                            onClick = {
                                val lastAssistantMsg = state.chatMessages.findLast { it.role == "assistant" }
                                Toast.makeText(context, "Restarting with Current Model...", Toast.LENGTH_SHORT).show()
                                viewModel.retryMessage(lastAssistantMsg, false, "correct", state.word)
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                            modifier = Modifier.height(30.dp)
                        ) {
                            Text("Retry", style = MaterialTheme.typography.labelSmall)
                        }
                        OutlinedButton(
                            onClick = {
                                val lastAssistantMsg = state.chatMessages.findLast { it.role == "assistant" }
                                Toast.makeText(context, "Restarting with Fallback Model...", Toast.LENGTH_SHORT).show()
                                viewModel.retryMessage(lastAssistantMsg, true, "correct", state.word)
                            },
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                            modifier = Modifier.height(30.dp)
                        ) {
                            Text("Retry (Fallback)", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.error)
                        }
                    }
                }
            }
        }

        // Header / Action Bar
        state.word?.let { word ->
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(8.dp))
                    .padding(8.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    com.aidict.app.ui.components.ChatHeaderTitle(
                        word = word,
                        onClick = { showRenameDialog = true },
                        modifier = Modifier.weight(1f)
                    )

                    IconButton(onClick = {
                        val clip = ClipData.newPlainText("AI Dict", state.chatMessages.firstOrNull()?.content ?: "")
                        clipboardManager.setPrimaryClip(clip)
                        Toast.makeText(context, "Copied to clipboard", Toast.LENGTH_SHORT).show()
                    }) {
                        Icon(Icons.Default.ContentCopy, contentDescription = "Copy")
                    }

                    IconButton(onClick = { isChatSearching = !isChatSearching }) {
                        Icon(Icons.Default.Search, contentDescription = "Search in Chat")
                    }

                    IconButton(onClick = {
                        val lastAssistantMsg = state.chatMessages.findLast { it.role == "assistant" }
                        Toast.makeText(context, "Restarting with Current Model...", Toast.LENGTH_SHORT).show()
                        viewModel.retryMessage(lastAssistantMsg, false, "correct", state.word)
                    }) {
                        if (state.isLoading) {
                            CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp, color = MaterialTheme.colorScheme.primary)
                        } else {
                            Icon(Icons.Default.Refresh, contentDescription = "Restart with Current Model", tint = MaterialTheme.colorScheme.primary)
                        }
                    }

                    IconButton(onClick = {
                        val lastAssistantMsg = state.chatMessages.findLast { it.role == "assistant" }
                        Toast.makeText(context, "Restarting with Fallback Model...", Toast.LENGTH_SHORT).show()
                        viewModel.retryMessage(lastAssistantMsg, true, "correct", state.word)
                    }) {
                        if (state.isLoading) {
                            CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp, color = MaterialTheme.colorScheme.error)
                        } else {
                            Icon(Icons.Default.Autorenew, contentDescription = "Restart with Fallback Model", tint = MaterialTheme.colorScheme.error)
                        }
                    }

                    IconButton(onClick = { showMoveToModeDialog = true }) {
                        Icon(Icons.AutoMirrored.Filled.CompareArrows, contentDescription = "Move Mode & Regenerate", tint = MaterialTheme.colorScheme.primary)
                    }

                    IconButton(onClick = { viewModel.deleteCurrentWord("correct") }) {
                        Icon(Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                    }
                }

                if (showMoveToModeDialog && state.word != null) {
                    MoveModeDialog(
                        currentMode = "correct",
                        onDismiss = { showMoveToModeDialog = false },
                        onSelectMode = { targetMode ->
                            onMoveToMode(state.word!!, targetMode)
                        }
                    )
                }

                if (showRenameDialog && state.word != null) {
                    com.aidict.app.ui.components.RenameWordDialog(
                        word = state.word!!,
                        onDismiss = { showRenameDialog = false },
                        onConfirm = { newName ->
                            viewModel.renameWord(state.word!!, newName, "correct")
                        }
                    )
                }

                if (isChatSearching) {
                    OutlinedTextField(
                        value = chatSearchQuery,
                        onValueChange = { chatSearchQuery = it },
                        modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                        placeholder = { Text("Find in chat...") },
                        singleLine = true,
                        trailingIcon = {
                            if (chatSearchQuery.isNotEmpty()) {
                                IconButton(onClick = { chatSearchQuery = "" }) {
                                    Icon(Icons.Default.Clear, contentDescription = "Clear Search")
                                }
                            }
                        }
                    )
                }

                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(top = 4.dp)) {
                    // Colors
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        colors.forEach { (name, colorValue) ->
                            Box(
                                modifier = Modifier
                                    .size(24.dp)
                                    .background(color = colorValue, shape = CircleShape)
                                    .clickable { viewModel.updateWordColor(if (word.color == name) "" else name, "correct") }
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
                                    .clickable { viewModel.updateWordStars(if (word.stars == star) 0 else star, "correct") }
                            )
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(8.dp))
        }

        // Chat Message List
        LazyColumn(modifier = Modifier.weight(1f)) {
            if (state.chatMessages.isEmpty()) {
                item { Spacer(modifier = Modifier.fillParentMaxSize()) }
            }
            items(state.chatMessages) { msg ->
                var isEditing by remember { mutableStateOf(false) }
                var editingContent by remember { mutableStateOf("") }
                val isUser = msg.role == "user"
                val isGenerating = !isUser && msg.content == "Generating..."
                val isError = !isUser && msg.content.startsWith("### ⚠️ Generation Failed")
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
                                    color = when {
                                        isUser -> MaterialTheme.colorScheme.primary
                                        isError -> MaterialTheme.colorScheme.errorContainer
                                        else -> MaterialTheme.colorScheme.secondaryContainer
                                    },
                                    shape = RoundedCornerShape(12.dp)
                                )
                                .padding(12.dp)
                        ) {
                            if (isUser) {
                                MarkdownText(text = msg.content, color = MaterialTheme.colorScheme.onPrimary, searchQuery = chatSearchQuery)
                            } else if (isGenerating) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    PulsingDots()
                                    Spacer(Modifier.width(8.dp))
                                    Text(if (state.isLoading) "Analyzing & correcting..." else "Generation interrupted", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSecondaryContainer)
                                }
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
                                                viewModel.editMessage(msg, editingContent, "correct")
                                                isEditing = false
                                            }) { Text("Save", color = MaterialTheme.colorScheme.primary) }
                                        }
                                    }
                                } else {
                                    Column {
                                        MarkdownText(
                                            text = msg.content,
                                            color = if (isError) MaterialTheme.colorScheme.onErrorContainer else MaterialTheme.colorScheme.onSecondaryContainer,
                                            searchQuery = chatSearchQuery
                                        )
                                        if (msg.content.contains("Machine Translation") && !isError) {
                                            Spacer(Modifier.height(8.dp))
                                            FilledTonalButton(
                                                onClick = {
                                                    state.word?.let { w ->
                                                        viewModel.streamCorrect(w.term, sourceLang, targetLang, profileId, isCorrectionOnly = false)
                                                    }
                                                },
                                                contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
                                                modifier = Modifier.padding(top = 2.dp)
                                            ) {
                                                Icon(Icons.Default.Autorenew, contentDescription = null, modifier = Modifier.size(14.dp))
                                                Spacer(Modifier.width(6.dp))
                                                Text("✨ Deepen with AI LLM", style = MaterialTheme.typography.labelSmall)
                                            }
                                        }
                                        if (isError) {
                                            Spacer(Modifier.height(8.dp))
                                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                                Button(
                                                    onClick = {
                                                        Toast.makeText(context, "Restarting with Current Model...", Toast.LENGTH_SHORT).show()
                                                        viewModel.retryMessage(msg, false, "correct", state.word)
                                                    },
                                                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
                                                    contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                                                    modifier = Modifier.height(30.dp)
                                                ) {
                                                    Icon(Icons.Default.Refresh, contentDescription = null, modifier = Modifier.size(14.dp))
                                                    Spacer(Modifier.width(4.dp))
                                                    Text("Retry", style = MaterialTheme.typography.labelSmall)
                                                }
                                                OutlinedButton(
                                                    onClick = {
                                                        Toast.makeText(context, "Restarting with Fallback Model...", Toast.LENGTH_SHORT).show()
                                                        viewModel.retryMessage(msg, true, "correct", state.word)
                                                    },
                                                    contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                                                    modifier = Modifier.height(30.dp)
                                                ) {
                                                    Icon(Icons.Default.Autorenew, contentDescription = null, modifier = Modifier.size(14.dp))
                                                    Spacer(Modifier.width(4.dp))
                                                    Text("Fallback", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.error)
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        if (!isUser && !isEditing && (!isGenerating || !state.isLoading)) {
                            Row(modifier = Modifier.fillMaxWidth(0.85f), horizontalArrangement = Arrangement.Start) {
                                IconButton(onClick = {
                                    val clip = ClipData.newPlainText("AI Dict", msg.content)
                                    clipboardManager.setPrimaryClip(clip)
                                    Toast.makeText(context, "Copied to clipboard", Toast.LENGTH_SHORT).show()
                                }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.ContentCopy, contentDescription = "Copy", modifier = Modifier.size(16.dp)) }
                                IconButton(onClick = {
                                    editingContent = msg.content
                                    isEditing = true
                                }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Edit, contentDescription = "Edit", modifier = Modifier.size(16.dp)) }
                                IconButton(onClick = {
                                    Toast.makeText(context, "Restarting with Current Model...", Toast.LENGTH_SHORT).show()
                                    viewModel.retryMessage(msg, false, "correct", state.word)
                                }, modifier = Modifier.size(32.dp)) {
                                    if (state.isLoading) {
                                        CircularProgressIndicator(modifier = Modifier.size(14.dp), strokeWidth = 2.dp, color = MaterialTheme.colorScheme.primary)
                                    } else {
                                        Icon(Icons.Default.Refresh, "Regenerate (Current)", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                                    }
                                }
                                IconButton(onClick = {
                                    Toast.makeText(context, "Restarting with Fallback Model...", Toast.LENGTH_SHORT).show()
                                    viewModel.retryMessage(msg, true, "correct", state.word)
                                }, modifier = Modifier.size(32.dp)) {
                                    if (state.isLoading) {
                                        CircularProgressIndicator(modifier = Modifier.size(14.dp), strokeWidth = 2.dp, color = MaterialTheme.colorScheme.error)
                                    } else {
                                        Icon(Icons.Default.Autorenew, "Regenerate (Fallback)", tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(16.dp))
                                    }
                                }
                                IconButton(onClick = { viewModel.deleteMessage(msg, "correct") }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(16.dp)) }
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
                        MarkdownText(text = state.currentStream, color = MaterialTheme.colorScheme.onSecondaryContainer, searchQuery = chatSearchQuery)
                    }
                }
            }
            if (state.isLoading && state.currentStream.isEmpty()) {
                item {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(16.dp),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        PulsingDots()
                        Spacer(Modifier.width(8.dp))
                        Text("Analyzing & correcting...", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.primary)
                    }
                }
            }
        }

        val isFollowUp = state.word != null && !state.isLoading
        ChatInputBar(
            availableLanguages = viewModel.orderedLanguages.collectAsState().value,
            inputTerm = viewModel.correctInput,
            onValueChange = { viewModel.correctInput = it },
            onSend = {
                val query = viewModel.correctInput
                if (autoNewSearch || !isFollowUp) {
                    if (correctType == "machine_translate") {
                        viewModel.translateLocalMachine(query, sourceLang, targetLang, profileId, mtTier)
                    } else {
                        val isOnly = correctType == "correction_only"
                        viewModel.streamCorrect(query, sourceLang, targetLang, profileId, isOnly)
                    }
                } else {
                    viewModel.sendFollowUpMessage(query, "correct")
                }
                viewModel.correctInput = ""
            },
            isLoading = state.isLoading,
            autoNewSearch = autoNewSearch,
            onToggleAutoNewSearch = onToggleAutoNewSearch,
            enterToSend = enterToSend,
            isFollowUp = isFollowUp,
            sourceLang = if (!isFollowUp || autoNewSearch) sourceLang else null,
            targetLang = if (!isFollowUp || autoNewSearch) targetLang else null,
            onSourceLangChange = if (!isFollowUp || autoNewSearch) { { sourceLang = it; viewModel.saveProfileSetting(profileId, "CORRECT_SOURCE", it) } } else null,
            onTargetLangChange = if (!isFollowUp || autoNewSearch) { { targetLang = it; viewModel.saveProfileSetting(profileId, "CORRECT_TARGET", it) } } else null,
            extraContent = if (!isFollowUp || autoNewSearch) {
                {
                    Column(
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 4.dp, vertical = 2.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.Center,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            FilterChip(
                                selected = correctType == "both",
                                onClick = {
                                    correctType = "both"
                                    viewModel.saveProfileSetting(profileId, "CORRECT_TYPE", "both")
                                },
                                label = { Text("Correction & Translation", style = MaterialTheme.typography.labelSmall) },
                                leadingIcon = if (correctType == "both") {
                                    { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(14.dp)) }
                                } else null,
                                colors = FilterChipDefaults.filterChipColors(
                                    selectedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                                    selectedLabelColor = MaterialTheme.colorScheme.onPrimaryContainer
                                ),
                                modifier = Modifier.padding(end = 4.dp)
                            )
                            FilterChip(
                                selected = correctType == "correction_only",
                                onClick = {
                                    correctType = "correction_only"
                                    viewModel.saveProfileSetting(profileId, "CORRECT_TYPE", "correction_only")
                                },
                                label = { Text("Correction Only", style = MaterialTheme.typography.labelSmall) },
                                leadingIcon = if (correctType == "correction_only") {
                                    { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(14.dp)) }
                                } else null,
                                colors = FilterChipDefaults.filterChipColors(
                                    selectedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                                    selectedLabelColor = MaterialTheme.colorScheme.onPrimaryContainer
                                ),
                                modifier = Modifier.padding(horizontal = 2.dp)
                            )
                            FilterChip(
                                selected = false,
                                onClick = {
                                    correctType = "machine_translate"
                                    viewModel.saveProfileSetting(profileId, "CORRECT_TYPE", "machine_translate")
                                },
                                label = { Text("Local MT", style = MaterialTheme.typography.labelSmall) },
                                colors = FilterChipDefaults.filterChipColors(
                                    selectedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                                    selectedLabelColor = MaterialTheme.colorScheme.onPrimaryContainer
                                ),
                                modifier = Modifier.padding(start = 4.dp)
                            )
                        }
                    }
                }
            } else null,
            onClear = { viewModel.clearCurrentSearch("correct") },
            suggestions = suggestions,
            onSuggestionClick = { word ->
                viewModel.loadWord(word)
                viewModel.correctInput = ""
                viewModel.clearSuggestions()
            },
            placeholder = if (isFollowUp && !autoNewSearch) "Ask follow-up question..." else if (correctType == "correction_only") "Paste text to correct & polish..." else "Paste text to correct & translate..."
        )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NormalTranslatorView(
    viewModel: com.aidict.app.ui.viewmodels.SearchViewModel,
    profileId: Int,
    sourceLang: String,
    targetLang: String,
    mtTier: com.aidict.app.data.LocalTranslationEngine.Tier,
    onSourceLangChange: (String) -> Unit,
    onTargetLangChange: (String) -> Unit,
    onMtTierChange: (com.aidict.app.data.LocalTranslationEngine.Tier) -> Unit,
    onSwitchMode: (String) -> Unit,
    onDeepenWithLlm: () -> Unit,
    onSpeak: (String, String) -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val clipboardManager = remember { context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager }
    var showManageModelsDialog by remember { mutableStateOf(false) }

    val supportedLanguages = remember { com.aidict.app.data.LocalTranslationEngine.getSupportedLanguages() }
    val sourceOptions = remember { listOf("Auto Detect") + supportedLanguages }

    LaunchedEffect(viewModel.mtSourceText, sourceLang, targetLang, mtTier) {
        kotlinx.coroutines.delay(300)
        viewModel.translateTransient(viewModel.mtSourceText, sourceLang, targetLang, mtTier)
    }

    if (showManageModelsDialog) {
        ManageOfflineModelsDialog(onDismiss = { showManageModelsDialog = false })
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
    ) {
        // Mode Selector Row
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            FilterChip(
                selected = false,
                onClick = { onSwitchMode("both") },
                label = { Text("Correction & Translation", style = MaterialTheme.typography.labelSmall) },
                modifier = Modifier.padding(end = 4.dp)
            )
            FilterChip(
                selected = false,
                onClick = { onSwitchMode("correction_only") },
                label = { Text("Correction Only", style = MaterialTheme.typography.labelSmall) },
                modifier = Modifier.padding(horizontal = 2.dp)
            )
            FilterChip(
                selected = true,
                onClick = { },
                label = { Text("Local MT", style = MaterialTheme.typography.labelSmall) },
                leadingIcon = { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(14.dp)) },
                colors = FilterChipDefaults.filterChipColors(
                    selectedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                    selectedLabelColor = MaterialTheme.colorScheme.onPrimaryContainer
                ),
                modifier = Modifier.padding(start = 4.dp)
            )
        }

        Spacer(Modifier.height(6.dp))

        // MT Sub-Row: Tier chips + Manage Offline Models button
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ) {
            FilterChip(
                selected = mtTier == com.aidict.app.data.LocalTranslationEngine.Tier.NORMAL,
                onClick = { onMtTierChange(com.aidict.app.data.LocalTranslationEngine.Tier.NORMAL) },
                label = { Text("Normal (Offline Opus-MT / ML Kit)", style = MaterialTheme.typography.labelSmall) },
                leadingIcon = if (mtTier == com.aidict.app.data.LocalTranslationEngine.Tier.NORMAL) {
                    { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(14.dp)) }
                } else null,
                colors = FilterChipDefaults.filterChipColors(
                    selectedContainerColor = MaterialTheme.colorScheme.secondaryContainer,
                    selectedLabelColor = MaterialTheme.colorScheme.onSecondaryContainer
                ),
                modifier = Modifier.padding(end = 4.dp)
            )
            FilterChip(
                selected = mtTier == com.aidict.app.data.LocalTranslationEngine.Tier.STRONG,
                onClick = { onMtTierChange(com.aidict.app.data.LocalTranslationEngine.Tier.STRONG) },
                label = { Text("Strong (NLLB-200)", style = MaterialTheme.typography.labelSmall) },
                leadingIcon = if (mtTier == com.aidict.app.data.LocalTranslationEngine.Tier.STRONG) {
                    { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(14.dp)) }
                } else null,
                colors = FilterChipDefaults.filterChipColors(
                    selectedContainerColor = MaterialTheme.colorScheme.secondaryContainer,
                    selectedLabelColor = MaterialTheme.colorScheme.onSecondaryContainer
                ),
                modifier = Modifier.padding(horizontal = 4.dp)
            )
            AssistChip(
                onClick = { showManageModelsDialog = true },
                label = { Text("Offline Packs 📥", style = MaterialTheme.typography.labelSmall) },
                modifier = Modifier.padding(start = 4.dp)
            )
        }

        Spacer(Modifier.height(10.dp))

        // Language Selector Bar
        Surface(
            shape = RoundedCornerShape(12.dp),
            color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp, vertical = 4.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                // Source Language Dropdown
                var srcExpanded by remember { mutableStateOf(false) }
                Box(modifier = Modifier.weight(1f)) {
                    TextButton(
                        onClick = { srcExpanded = true },
                        modifier = Modifier.fillMaxWidth(),
                        contentPadding = PaddingValues(horizontal = 4.dp, vertical = 2.dp)
                    ) {
                        Text(
                            text = if (sourceLang == "Auto Detect" && !viewModel.mtDetectedSourceLang.isNullOrBlank()) {
                                "Auto (${viewModel.mtDetectedSourceLang})"
                            } else {
                                sourceLang
                            },
                            style = MaterialTheme.typography.labelMedium,
                            maxLines = 1
                        )
                        Icon(Icons.Default.ArrowDropDown, contentDescription = null, modifier = Modifier.size(18.dp))
                    }
                    DropdownMenu(
                        expanded = srcExpanded,
                        onDismissRequest = { srcExpanded = false }
                    ) {
                        sourceOptions.forEach { lang ->
                            DropdownMenuItem(
                                text = { Text(lang) },
                                onClick = {
                                    onSourceLangChange(lang)
                                    srcExpanded = false
                                }
                            )
                        }
                    }
                }

                // Swap Button
                IconButton(
                    onClick = {
                        if (sourceLang != "Auto Detect") {
                            val temp = sourceLang
                            onSourceLangChange(targetLang)
                            onTargetLangChange(temp)
                        } else if (!viewModel.mtDetectedSourceLang.isNullOrBlank()) {
                            val detected = viewModel.mtDetectedSourceLang!!
                            onSourceLangChange(targetLang)
                            onTargetLangChange(detected)
                        }
                    },
                    modifier = Modifier.size(36.dp)
                ) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.CompareArrows,
                        contentDescription = "Swap Languages",
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.size(20.dp)
                    )
                }

                // Target Language Dropdown
                var tgtExpanded by remember { mutableStateOf(false) }
                Box(modifier = Modifier.weight(1f)) {
                    TextButton(
                        onClick = { tgtExpanded = true },
                        modifier = Modifier.fillMaxWidth(),
                        contentPadding = PaddingValues(horizontal = 4.dp, vertical = 2.dp)
                    ) {
                        Text(
                            text = targetLang,
                            style = MaterialTheme.typography.labelMedium,
                            maxLines = 1
                        )
                        Icon(Icons.Default.ArrowDropDown, contentDescription = null, modifier = Modifier.size(18.dp))
                    }
                    DropdownMenu(
                        expanded = tgtExpanded,
                        onDismissRequest = { tgtExpanded = false }
                    ) {
                        supportedLanguages.forEach { lang ->
                            DropdownMenuItem(
                                text = { Text(lang) },
                                onClick = {
                                    onTargetLangChange(lang)
                                    tgtExpanded = false
                                }
                            )
                        }
                    }
                }
            }
        }

        Spacer(Modifier.height(12.dp))

        // Source Input Card
        Card(
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.45f)),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(12.dp)) {
                OutlinedTextField(
                    value = viewModel.mtSourceText,
                    onValueChange = { viewModel.mtSourceText = it },
                    placeholder = { Text("Enter text to translate...", style = MaterialTheme.typography.bodyLarge) },
                    textStyle = MaterialTheme.typography.bodyLarge,
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(min = 120.dp, max = 220.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Color.Transparent,
                        unfocusedBorderColor = Color.Transparent
                    )
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "${viewModel.mtSourceText.length} characters",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                    )

                    Spacer(Modifier.weight(1f))

                    if (viewModel.mtSourceText.isNotBlank()) {
                        IconButton(onClick = { viewModel.mtSourceText = "" }, modifier = Modifier.size(32.dp)) {
                            Icon(Icons.Default.Clear, contentDescription = "Clear", modifier = Modifier.size(18.dp))
                        }
                    } else {
                        IconButton(
                            onClick = {
                                val clip = clipboardManager.primaryClip?.getItemAt(0)?.text?.toString() ?: ""
                                if (clip.isNotBlank()) {
                                    viewModel.mtSourceText = clip
                                }
                            },
                            modifier = Modifier.size(32.dp)
                        ) {
                            Icon(Icons.Default.ContentPaste, contentDescription = "Paste", modifier = Modifier.size(18.dp))
                        }
                    }

                    if (viewModel.mtSourceText.isNotBlank()) {
                        IconButton(
                            onClick = { onSpeak(viewModel.mtSourceText, viewModel.mtDetectedSourceLang ?: sourceLang) },
                            modifier = Modifier.size(32.dp)
                        ) {
                            Icon(Icons.AutoMirrored.Filled.VolumeUp, contentDescription = "Listen", modifier = Modifier.size(18.dp))
                        }
                    }
                }
            }
        }

        Spacer(Modifier.height(14.dp))

        // Target Translation Card
        Card(
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer),
            modifier = Modifier.fillMaxWidth().heightIn(min = 130.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(14.dp)
            ) {
                if (viewModel.mtIsLoading) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 24.dp),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(22.dp),
                            strokeWidth = 2.dp,
                            color = MaterialTheme.colorScheme.primary
                        )
                        Spacer(Modifier.width(10.dp))
                        Text(
                            text = if (viewModel.mtIsDownloadingModel) "Downloading offline language pack (~30MB)..." else "Translating with local model...",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSecondaryContainer
                        )
                    }
                } else if (!viewModel.mtErrorMessage.isNullOrBlank()) {
                    Column(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                        Text(
                            text = viewModel.mtErrorMessage!!,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.error
                        )
                        Spacer(Modifier.height(6.dp))
                        TextButton(
                            onClick = { viewModel.translateTransient(viewModel.mtSourceText, sourceLang, targetLang, mtTier) },
                            modifier = Modifier.align(Alignment.End)
                        ) {
                            Icon(Icons.Default.Refresh, contentDescription = null, modifier = Modifier.size(16.dp))
                            Spacer(Modifier.width(4.dp))
                            Text("Retry")
                        }
                    }
                } else if (viewModel.mtTranslatedText.isNotBlank()) {
                    SelectionContainer {
                        Text(
                            text = viewModel.mtTranslatedText,
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.onSecondaryContainer
                        )
                    }

                    Spacer(Modifier.height(12.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        // Speaker pronunciation button
                        IconButton(
                            onClick = { onSpeak(viewModel.mtTranslatedText, targetLang) },
                            modifier = Modifier.size(32.dp)
                        ) {
                            Icon(
                                Icons.AutoMirrored.Filled.VolumeUp,
                                contentDescription = "Listen translation",
                                tint = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.size(18.dp)
                            )
                        }

                        // Copy button
                        IconButton(
                            onClick = {
                                val clip = ClipData.newPlainText("Translation", viewModel.mtTranslatedText)
                                clipboardManager.setPrimaryClip(clip)
                                Toast.makeText(context, "Translation copied to clipboard", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.size(32.dp)
                        ) {
                            Icon(
                                Icons.Default.ContentCopy,
                                contentDescription = "Copy translation",
                                tint = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.size(18.dp)
                            )
                        }

                        // Save to History button (Explicit - unsaved by default!)
                        IconButton(
                            onClick = {
                                viewModel.saveCurrentMtToHistory(sourceLang, targetLang, profileId, mtTier) {
                                    Toast.makeText(context, "Saved to History!", Toast.LENGTH_SHORT).show()
                                }
                            },
                            modifier = Modifier.size(32.dp)
                        ) {
                            Icon(
                                imageVector = if (viewModel.mtIsSaved) Icons.Default.Bookmark else Icons.Outlined.BookmarkBorder,
                                contentDescription = "Save to History",
                                tint = if (viewModel.mtIsSaved) Color(0xFF10B981) else MaterialTheme.colorScheme.primary,
                                modifier = Modifier.size(18.dp)
                            )
                        }

                        Spacer(Modifier.weight(1f))

                        // Deepen with AI LLM Button
                        FilledTonalButton(
                            onClick = onDeepenWithLlm,
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
                            modifier = Modifier.height(34.dp)
                        ) {
                            Icon(Icons.Default.AutoAwesome, contentDescription = null, modifier = Modifier.size(14.dp))
                            Spacer(Modifier.width(6.dp))
                            Text("✨ Deepen with AI LLM", style = MaterialTheme.typography.labelSmall)
                        }
                    }
                } else {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 32.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "Translation will appear here instantaneously...",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSecondaryContainer.copy(alpha = 0.6f)
                        )
                    }
                }
            }
        }
    }
}
