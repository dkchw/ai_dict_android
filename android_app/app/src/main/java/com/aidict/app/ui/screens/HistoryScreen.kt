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
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.material3.windowsizeclass.WindowSizeClass
import androidx.compose.material3.windowsizeclass.WindowWidthSizeClass
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.aidict.app.ui.viewmodels.HistoryViewModel
import com.aidict.app.data.entities.Word
import com.aidict.app.data.entities.Session

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen(appViewModel: com.aidict.app.ui.viewmodels.AppViewModel, 
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
    
    var showCreateSession by remember { mutableStateOf(false) }
    var showRenameSession by remember { mutableStateOf<Session?>(null) }
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
                sessionNameInput = ""
                showCreateSession = true 
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
                            val dismissState = rememberSwipeToDismissBoxState()
                            SwipeToDismissBox(
                                state = dismissState,
                                backgroundContent = {
                                    Box(
                                        Modifier.fillMaxSize().background(MaterialTheme.colorScheme.error).padding(16.dp),
                                        contentAlignment = Alignment.CenterEnd
                                    ) {
                                        Icon(Icons.Default.Delete, contentDescription = "Delete", tint = Color.White)
                                    }
                                }
                            ) {
                                Card(
                                    modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).clickable { selectedWord = word },
                                    elevation = CardDefaults.cardElevation(if (selectedWord?.id == word.id) 8.dp else 2.dp),
                                    colors = CardDefaults.cardColors(
                                        containerColor = if (selectedWord?.id == word.id) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant
                                    )
                                ) {
                                    Row(modifier = Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
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
                            Text(text = word.term, modifier = Modifier.padding(12.dp))
                        }
                    }
                }
            }
        }
    }

    val detailContent = @Composable {
        if (selectedWord != null) {
            Column(modifier = Modifier.fillMaxSize().padding(16.dp).background(MaterialTheme.colorScheme.surface)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(text = "Details for: ${selectedWord!!.term}", style = MaterialTheme.typography.headlineSmall, modifier = Modifier.weight(1f))
                    IconButton(onClick = { selectedWord = null }) {
                        Icon(Icons.Default.Delete, contentDescription = "Close")
                    }
                }
                HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                Text("Chat history for this word will appear here.")
            }
        }
    }

    if (isTablet) {
        Row(modifier = modifier.fillMaxSize()) {
            Box(modifier = Modifier.weight(1f)) { listContent() }
            if (selectedWord != null) {
                VerticalDivider()
                Box(modifier = Modifier.weight(1f)) { detailContent() }
            }
        }
    } else {
        Column(modifier = modifier.fillMaxSize()) {
            Box(modifier = Modifier.weight(if (selectedWord != null) 1f else 2f)) { listContent() }
            if (selectedWord != null) {
                HorizontalDivider()
                Box(modifier = Modifier.weight(1f)) { detailContent() }
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
}
