package com.aidict.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.material3.windowsizeclass.WindowSizeClass
import androidx.compose.material3.windowsizeclass.WindowWidthSizeClass
import androidx.compose.runtime.*
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.activity.compose.BackHandler
import com.aidict.app.ui.viewmodels.HistoryViewModel
import com.aidict.app.data.entities.Word
import com.aidict.app.data.entities.Session

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen(appViewModel: com.aidict.app.ui.viewmodels.AppViewModel,
    onNavigateToChat: (Word) -> Unit, 
    viewModel: HistoryViewModel,
    windowSizeClass: WindowSizeClass,
    modifier: Modifier = Modifier
) {
    val history by viewModel.historyState.collectAsState()
    val sessions by viewModel.sessions.collectAsState()
    val colorFilter by viewModel.colorFilter.collectAsState()
    val starsFilter by viewModel.starsFilter.collectAsState()
    var query by remember { mutableStateOf("") }
    
        var selectedWord by remember { mutableStateOf<Word?>(null) }
    
    LaunchedEffect(selectedWord) {
        viewModel.setSelectedWordId(selectedWord?.id)
    }
    
    if (selectedWord != null) {
        BackHandler {
            selectedWord = null
        }
    }
    
    var showCreateSession by remember { mutableStateOf(false) }
    var showRenameSession by remember { mutableStateOf<Session?>(null) }
    var showRenameWord by remember { mutableStateOf<com.aidict.app.data.entities.Word?>(null) }
    var wordNameInput by remember { mutableStateOf("") }
    var sessionNameInput by remember { mutableStateOf("") }

    val isTablet = windowSizeClass.widthSizeClass == WindowWidthSizeClass.Expanded

    val colors = listOf(
        "Red" to Color(0xFFEF4444),
        "Orange" to Color(0xFFF97316),
        "Yellow" to Color(0xFFEAB308),
        "Green" to Color(0xFF22C55E),
        "Blue" to Color(0xFF3B82F6)
    )

    val listContent = @Composable {
        Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
            val appState by appViewModel.uiState.collectAsState()
            Text("Mode: ${viewModel.currentMode.collectAsState().value.uppercase()} | Profile: ${appState.activeProfile?.name ?: "Unknown"}", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(bottom = 8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                OutlinedTextField(
                    value = query,
                    onValueChange = { 
                        query = it
                        viewModel.updateSearchQuery(it)
                    },
                    label = { Text("Search history...") },
                    modifier = Modifier.weight(1f)
                )
                Spacer(Modifier.width(8.dp))
                Button(onClick = { /* TODO: Special sort */ }) {
                    Text("Sort")
                }
            }
            
            Row(
                modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                colors.forEach { (name, colorValue) ->
                    FilterChip(
                        selected = colorFilter == name,
                        onClick = { viewModel.setFilterColor(name) },
                        label = { Text(name) },
                        leadingIcon = { Box(modifier = Modifier.size(12.dp).background(colorValue, CircleShape)) }
                    )
                }
                
                Spacer(modifier = Modifier.width(4.dp))
                HorizontalDivider(modifier = Modifier.width(1.dp).height(24.dp))
                Spacer(modifier = Modifier.width(4.dp))

                (1..5).forEach { star ->
                    FilterChip(
                        selected = starsFilter == star,
                        onClick = { viewModel.setFilterStars(star) },
                        label = { Text("$star") },
                        leadingIcon = { Icon(Icons.Default.Star, contentDescription = "Star $star", tint = Color(0xFFFFC107), modifier = Modifier.size(16.dp)) }
                    )
                }
            }
            
            Button(onClick = { 
                val timeName = java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss", java.util.Locale.getDefault()).format(java.util.Date())
                viewModel.createSession(timeName)
            }, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Default.Add, contentDescription = "Create Session")
                Spacer(Modifier.width(8.dp))
                Text("Create Session")
            }

            Spacer(modifier = Modifier.height(8.dp))

            val grouped = history.groupBy { it.sessionId }

            LazyColumn(modifier = Modifier.weight(1f)) {
                sessions.forEach { session ->
                    val wordsInSession = grouped[session.id] ?: emptyList()
                    if (wordsInSession.isNotEmpty() || sessions.size > 1) {
                        item {
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 8.dp)) {
                                Text(
                                    text = session.name,
                                    style = MaterialTheme.typography.titleMedium,
                                    modifier = Modifier.weight(1f)
                                )
                                IconButton(onClick = { 
                                    sessionNameInput = session.name
                                    showRenameSession = session
                                }) {
                                    Icon(Icons.Default.Edit, contentDescription = "Rename")
                                }
                                IconButton(onClick = { viewModel.deleteSession(session) }) {
                                    Icon(Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                                }
                            }
                        }
                        items(wordsInSession, key = { it.id }) { word ->
                            Card(
                                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).clickable { selectedWord = word },
                                elevation = CardDefaults.cardElevation(if (selectedWord?.id == word.id) 8.dp else 2.dp),
                                colors = CardDefaults.cardColors(
                                    containerColor = if (selectedWord?.id == word.id) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant
                                )
                            ) {
                                Row(modifier = Modifier.padding(start = 12.dp, top = 4.dp, bottom = 4.dp, end = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(text = word.term, style = MaterialTheme.typography.bodyLarge)
                                        if (!word.language.isNullOrBlank()) {
                                            Text(text = word.language, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.secondary)
                                        }
                                    }
                                    if (word.color != null) {
                                        val c = colors.find { it.first == word.color }?.second ?: Color.Gray
                                        Box(modifier = Modifier.size(12.dp).background(c, CircleShape).padding(end = 8.dp))
                                    }
                                    if (word.stars > 0) {
                                        Spacer(modifier = Modifier.width(8.dp))
                                        Row { (1..word.stars).forEach { _ -> Icon(Icons.Default.Star, contentDescription = "Star", tint = Color(0xFFFFC107), modifier = Modifier.size(16.dp)) } }
                                    }
                                    IconButton(onClick = {
                                        wordNameInput = word.term
                                        showRenameWord = word
                                    }) {
                                        Icon(Icons.Default.Edit, contentDescription = "Rename", modifier = Modifier.size(20.dp))
                                    }
                                    IconButton(onClick = { viewModel.deleteWord(word) }) {
                                        Icon(Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(20.dp))
                                    }
                                }
                            }
                        }
                    }
                }
                
                val unknownSessions = grouped.keys.filter { sid -> sessions.none { it.id == sid } }
                unknownSessions.forEach { sid ->
                    item { Text(text = "Session: $sid", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(vertical = 8.dp)) }
                    items(grouped[sid] ?: emptyList()) { word ->
                        Card(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).clickable { selectedWord = word },
                            elevation = CardDefaults.cardElevation(if (selectedWord?.id == word.id) 8.dp else 2.dp)
                        ) {
                            Row(modifier = Modifier.padding(start = 12.dp, top = 4.dp, bottom = 4.dp, end = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text(text = word.term, modifier = Modifier.weight(1f).padding(8.dp))
                                IconButton(onClick = {
                                    wordNameInput = word.term
                                    showRenameWord = word
                                }) {
                                    Icon(Icons.Default.Edit, contentDescription = "Rename", modifier = Modifier.size(20.dp))
                                }
                                IconButton(onClick = { viewModel.deleteWord(word) }) {
                                    Icon(Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(20.dp))
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    val detailContent = @Composable {
        val messages by viewModel.selectedChatMessages.collectAsState()
        if (selectedWord != null) {
            Column(modifier = Modifier.fillMaxSize().padding(16.dp).background(MaterialTheme.colorScheme.surface)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(text = "Details", style = MaterialTheme.typography.titleLarge, modifier = Modifier.weight(1f))
                    Button(onClick = { onNavigateToChat(selectedWord!!) }) { Text("Resume Chat") }
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(onClick = { selectedWord = null }) {
                        Icon(Icons.Default.Close, contentDescription = "Close Details")
                    }
                }
                Spacer(modifier = Modifier.height(8.dp))
                LazyColumn(modifier = Modifier.weight(1f).fillMaxWidth()) {
                    items(messages) { msg ->
                        val isUser = msg.role == "user"
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth(if (isUser) 0.85f else 1f)
                                    .background(
                                        color = if (isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.secondaryContainer,
                                        shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp)
                                    )
                                    .padding(12.dp)
                            ) {
                                com.aidict.app.ui.components.MarkdownText(
                                    text = msg.content,
                                    color = if (isUser) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSecondaryContainer
                                )
                            }
                        }
                    }
                }
            }
        }
    }

    val splitFraction by viewModel.splitFraction.collectAsState()
    val configuration = LocalConfiguration.current
    val density = LocalDensity.current

    if (isTablet) {
        val totalWidthDp = configuration.screenWidthDp.dp
        Row(modifier = modifier.fillMaxSize()) {
            Box(modifier = Modifier.weight(if (selectedWord != null) splitFraction else 1f)) { listContent() }
            if (selectedWord != null) {
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .width(8.dp)
                        .background(MaterialTheme.colorScheme.outlineVariant)
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                val dragAmountFraction = dragAmount.x / (totalWidthDp.toPx())
                                val newFraction = (splitFraction + dragAmountFraction).coerceIn(0.2f, 0.8f)
                                viewModel.updateSplitFraction(newFraction)
                            }
                        }
                ) {
                    VerticalDivider(modifier = Modifier.align(Alignment.Center))
                }
                Box(modifier = Modifier.weight(1f - splitFraction)) { detailContent() }
            }
        }
    } else {
        val totalHeightDp = configuration.screenHeightDp.dp
        Column(modifier = modifier.fillMaxSize()) {
            Box(modifier = Modifier.weight(if (selectedWord != null) splitFraction else 1f)) { listContent() }
            if (selectedWord != null) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(8.dp)
                        .background(MaterialTheme.colorScheme.outlineVariant)
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                val dragAmountFraction = dragAmount.y / (totalHeightDp.toPx())
                                val newFraction = (splitFraction + dragAmountFraction).coerceIn(0.2f, 0.8f)
                                viewModel.updateSplitFraction(newFraction)
                            }
                        }
                ) {
                    HorizontalDivider(modifier = Modifier.align(Alignment.Center))
                }
                Box(modifier = Modifier.weight(1f - splitFraction)) { detailContent() }
            }
        }
    }

    if (showCreateSession) {
        AlertDialog(
            onDismissRequest = { showCreateSession = false },
            title = { Text("New Session") },
            text = {
                OutlinedTextField(
                    value = sessionNameInput,
                    onValueChange = { sessionNameInput = it },
                    label = { Text("Session Name") }
                )
            },
            confirmButton = {
                TextButton(onClick = {
                    if (sessionNameInput.isNotBlank()) viewModel.createSession(sessionNameInput)
                    sessionNameInput = ""
                    showCreateSession = false
                }) { Text("Create") }
            },
            dismissButton = {
                TextButton(onClick = { showCreateSession = false }) { Text("Cancel") }
            }
        )
    }

    if (showRenameSession != null) {
        AlertDialog(
            onDismissRequest = { showRenameSession = null },
            title = { Text("Rename Session") },
            text = {
                OutlinedTextField(
                    value = sessionNameInput,
                    onValueChange = { sessionNameInput = it },
                    label = { Text("Session Name") }
                )
            },
            confirmButton = {
                TextButton(onClick = {
                    if (sessionNameInput.isNotBlank()) viewModel.renameSession(showRenameSession!!, sessionNameInput)
                    sessionNameInput = ""
                    showRenameSession = null
                }) { Text("Rename") }
            },
            dismissButton = {
                TextButton(onClick = { showRenameSession = null }) { Text("Cancel") }
            }
        )
    }

    if (showRenameWord != null) {
        AlertDialog(
            onDismissRequest = { showRenameWord = null },
            title = { Text("Rename History Item") },
            text = {
                OutlinedTextField(
                    value = wordNameInput,
                    onValueChange = { wordNameInput = it },
                    label = { Text("New Name") }
                )
            },
            confirmButton = {
                TextButton(onClick = {
                    if (wordNameInput.isNotBlank()) {
                        viewModel.renameWord(showRenameWord!!, wordNameInput)
                        if (selectedWord?.id == showRenameWord?.id) {
                            selectedWord = selectedWord?.copy(term = wordNameInput)
                        }
                    }
                    wordNameInput = ""
                    showRenameWord = null
                }) { Text("Rename") }
            },
            dismissButton = {
                TextButton(onClick = { showRenameWord = null }) { Text("Cancel") }
            }
        )
    }

}