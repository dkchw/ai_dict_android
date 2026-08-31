import re

# 1. Update DAO
with open('android_app/app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'r') as f:
    dao_text = f.read()
dao_text = dao_text.replace('    suspend fun deleteNotesByIds(ids: List<Int>)\n}', '    suspend fun deleteNotesByIds(ids: List<Int>)\n\n    @Query("DELETE FROM session WHERE id IN (:ids)")\n    suspend fun deleteSessionsByIds(ids: List<String>)\n\n    @Query("DELETE FROM word WHERE id IN (:ids)")\n    suspend fun deleteWordsByIds(ids: List<Int>)\n}')
with open('android_app/app/src/main/java/com/aidict/app/data/dao/AppDao.kt', 'w') as f:
    f.write(dao_text)

# 2. Update ViewModel
with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    vm_text = f.read()
vm_methods = """
    fun deleteSelectedSessions(sessionIds: Set<String>) {
        viewModelScope.launch {
            database.appDao().deleteSessionsByIds(sessionIds.toList())
            val active = database.appDao().getSetting("ACTIVE_SESSION_ID")?.value
            if (active in sessionIds) {
                setActiveSession(null)
            }
        }
    }

    fun deleteSelectedWords(wordIds: Set<Int>) {
        viewModelScope.launch {
            database.appDao().deleteWordsByIds(wordIds.toList())
            if (selectedWordId.value in wordIds) {
                setSelectedWordId(null)
            }
        }
    }
"""
vm_text = vm_text.replace('    fun deleteSession(session: Session) {\n        viewModelScope.launch {\n            database.appDao().deleteSession(session)\n        }\n    }', '    fun deleteSession(session: Session) {\n        viewModelScope.launch {\n            database.appDao().deleteSession(session)\n        }\n    }\n' + vm_methods)
with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(vm_text)

# 3. Update HistoryScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    hs_text = f.read()

# Imports
hs_text = hs_text.replace('import androidx.compose.material.icons.filled.Star', 'import androidx.compose.material.icons.filled.Star\nimport androidx.compose.material.icons.filled.KeyboardArrowDown\nimport androidx.compose.material.icons.filled.KeyboardArrowUp')

# State variables
state_old = """    var showCreateSession by remember { mutableStateOf(false) }
    var showRenameSession by remember { mutableStateOf<Session?>(null) }
    var showRenameWord by remember { mutableStateOf<com.aidict.app.data.entities.Word?>(null) }
    var wordNameInput by remember { mutableStateOf("") }
    var sessionNameInput by remember { mutableStateOf("") }"""
    
state_new = state_old + """

    var isSelectionMode by remember { mutableStateOf(false) }
    var selectedSessionIds by remember { mutableStateOf(setOf<String>()) }
    var selectedWordIds by remember { mutableStateOf(setOf<Int>()) }
    var collapsedSessionIds by remember { mutableStateOf(setOf<String>()) }"""
hs_text = hs_text.replace(state_old, state_new)

# Back Handler
back_old = """    if (selectedWord != null) {
        BackHandler {
            selectedWord = null
                        viewModel.setSelectedWordId(null)
        }
    }"""
back_new = """    if (isSelectionMode) {
        BackHandler {
            isSelectionMode = false
            selectedSessionIds = emptySet()
            selectedWordIds = emptySet()
        }
    } else if (selectedWord != null) {
        BackHandler {
            selectedWord = null
            viewModel.setSelectedWordId(null)
        }
    }"""
hs_text = hs_text.replace(back_old, back_new)

# Action Bar
action_old = """            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = { viewModel.setActiveSession(null) },
                    modifier = Modifier.weight(1f),
                    colors = androidx.compose.material3.ButtonDefaults.buttonColors(
                        containerColor = if (activeSessionId.isNullOrBlank()) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                        contentColor = if (activeSessionId.isNullOrBlank()) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                ) {
                    Text("Default Session")
                }
                Button(
                    onClick = { showCreateSession = true }, 
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Default.Add, contentDescription = "Create Session")
                    Spacer(Modifier.width(8.dp))
                    Text("New Session")
                }
            }"""
action_new = """            if (isSelectionMode) {
                Row(modifier = Modifier.fillMaxWidth().background(MaterialTheme.colorScheme.primaryContainer, androidx.compose.foundation.shape.RoundedCornerShape(8.dp)).padding(8.dp), verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = { isSelectionMode = false; selectedSessionIds = emptySet(); selectedWordIds = emptySet() }) {
                        Icon(Icons.Default.Close, contentDescription = "Cancel Selection")
                    }
                    Text("${selectedSessionIds.size} Sessions, ${selectedWordIds.size} Words", modifier = Modifier.weight(1f), style = MaterialTheme.typography.titleMedium)
                    IconButton(onClick = {
                        viewModel.deleteSelectedSessions(selectedSessionIds)
                        viewModel.deleteSelectedWords(selectedWordIds)
                        isSelectionMode = false
                        selectedSessionIds = emptySet()
                        selectedWordIds = emptySet()
                    }) {
                        Icon(Icons.Default.Delete, contentDescription = "Delete Selected", tint = MaterialTheme.colorScheme.error)
                    }
                }
            } else {
""" + action_old + """
            }"""
hs_text = hs_text.replace(action_old, action_new)

# LazyColumn - we will use regex to capture the entire LazyColumn block securely
lazy_col_pattern = r'            LazyColumn\(modifier = Modifier\.weight\(1f\)\) \{.*?\n            \}'
# Actually, since python regex might have trouble with nested brackets, let's just do a manual string replace from `            LazyColumn(modifier = Modifier.weight(1f)) {` up to `            val detailContent = @Composable {`
lazy_col_start = '            LazyColumn(modifier = Modifier.weight(1f)) {'
detail_content_start = '            val detailContent = @Composable {'

parts = hs_text.split(lazy_col_start)
part0 = parts[0]
subparts = parts[1].split(detail_content_start)
part2 = detail_content_start + subparts[1]

lazy_col_new = """            @OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
            LazyColumn(modifier = Modifier.weight(1f)) {
                sessions.forEach { session ->
                    val wordsInSession = grouped[session.id] ?: emptyList()
                    val isSessionActive = activeSessionId == session.id
                    val isCollapsed = collapsedSessionIds.contains(session.id)
                    item {
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)
                            .background(if (isSelectionMode && selectedSessionIds.contains(session.id)) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.5f) else if (isSessionActive) MaterialTheme.colorScheme.primaryContainer else androidx.compose.ui.graphics.Color.Transparent, shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp))
                            .androidx.compose.foundation.combinedClickable(
                                onClick = {
                                    if (isSelectionMode) {
                                        selectedSessionIds = if (selectedSessionIds.contains(session.id)) selectedSessionIds - session.id else selectedSessionIds + session.id
                                    } else {
                                        viewModel.setActiveSession(session.id)
                                    }
                                },
                                onLongClick = {
                                    if (!isSelectionMode) {
                                        isSelectionMode = true
                                        selectedSessionIds = selectedSessionIds + session.id
                                    }
                                }
                            ).padding(8.dp)) {
                            
                            if (isSelectionMode) {
                                Checkbox(checked = selectedSessionIds.contains(session.id), onCheckedChange = { selectedSessionIds = if (it) selectedSessionIds + session.id else selectedSessionIds - session.id })
                            }
                            
                            Text(
                                text = "${session.name} (${wordsInSession.size})" + if (isSessionActive) " (Active)" else "",
                                style = MaterialTheme.typography.titleMedium,
                                color = if (isSessionActive) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface,
                                modifier = Modifier.weight(1f)
                            )
                            
                            if (!isSelectionMode) {
                                IconButton(onClick = { 
                                    collapsedSessionIds = if (isCollapsed) collapsedSessionIds - session.id else collapsedSessionIds + session.id 
                                }) {
                                    Icon(if (isCollapsed) Icons.Default.KeyboardArrowDown else Icons.Default.KeyboardArrowUp, contentDescription = "Toggle Collapse")
                                }
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
                    }
                    if (!isCollapsed) {
                        items(wordsInSession, key = { it.id }) { word ->
                            Card(
                                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).androidx.compose.foundation.combinedClickable(
                                    onClick = {
                                        if (isSelectionMode) {
                                            selectedWordIds = if (selectedWordIds.contains(word.id)) selectedWordIds - word.id else selectedWordIds + word.id
                                        } else {
                                            selectedWord = word; viewModel.setSelectedWordId(word.id)
                                        }
                                    },
                                    onLongClick = {
                                        if (!isSelectionMode) {
                                            isSelectionMode = true
                                            selectedWordIds = selectedWordIds + word.id
                                        }
                                    }
                                ),
                                elevation = CardDefaults.cardElevation(if (selectedWord?.id == word.id) 8.dp else 2.dp),
                                colors = CardDefaults.cardColors(
                                    containerColor = if (isSelectionMode && selectedWordIds.contains(word.id)) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.5f) else if (selectedWord?.id == word.id) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant
                                )
                            ) {
                                Row(modifier = Modifier.padding(start = 12.dp, top = 4.dp, bottom = 4.dp, end = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                    if (isSelectionMode) {
                                        Checkbox(checked = selectedWordIds.contains(word.id), onCheckedChange = { selectedWordIds = if (it) selectedWordIds + word.id else selectedWordIds - word.id })
                                    }
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
                                    if (!isSelectionMode) {
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
                
                val unknownSessions = grouped.keys.filter { sid -> sessions.none { it.id == sid } }
                unknownSessions.forEach { sid ->
                    val isCollapsed = collapsedSessionIds.contains(sid)
                    item { 
                        val count = (grouped[sid] ?: emptyList()).size
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp).clickable { collapsedSessionIds = if (isCollapsed) collapsedSessionIds - sid else collapsedSessionIds + sid }) {
                            Text(text = "Session: $sid ($count)", style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
                            Icon(if (isCollapsed) Icons.Default.KeyboardArrowDown else Icons.Default.KeyboardArrowUp, contentDescription = "Toggle Collapse")
                        }
                    }
                    if (!isCollapsed) {
                        items(grouped[sid] ?: emptyList(), key = { it.id }) { word ->
                            Card(
                                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).androidx.compose.foundation.combinedClickable(
                                    onClick = {
                                        if (isSelectionMode) {
                                            selectedWordIds = if (selectedWordIds.contains(word.id)) selectedWordIds - word.id else selectedWordIds + word.id
                                        } else {
                                            selectedWord = word; viewModel.setSelectedWordId(word.id)
                                        }
                                    },
                                    onLongClick = {
                                        if (!isSelectionMode) {
                                            isSelectionMode = true
                                            selectedWordIds = selectedWordIds + word.id
                                        }
                                    }
                                ),
                                elevation = CardDefaults.cardElevation(if (selectedWord?.id == word.id) 8.dp else 2.dp),
                                colors = CardDefaults.cardColors(
                                    containerColor = if (isSelectionMode && selectedWordIds.contains(word.id)) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.5f) else if (selectedWord?.id == word.id) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant
                                )
                            ) {
                                Row(modifier = Modifier.padding(start = 12.dp, top = 4.dp, bottom = 4.dp, end = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                    if (isSelectionMode) {
                                        Checkbox(checked = selectedWordIds.contains(word.id), onCheckedChange = { selectedWordIds = if (it) selectedWordIds + word.id else selectedWordIds - word.id })
                                    }
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
                                    if (!isSelectionMode) {
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
"""

hs_text = part0 + lazy_col_new + part2
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(hs_text)

