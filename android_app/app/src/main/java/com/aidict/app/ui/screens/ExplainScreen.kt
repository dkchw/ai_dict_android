package com.aidict.app.ui.screens



import androidx.compose.foundation.layout.*

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
import com.aidict.app.ui.components.MarkdownText
import androidx.compose.ui.unit.dp
import com.aidict.app.ui.viewmodels.ExplainViewModel

@Composable
fun ExplainScreen(
    viewModel: com.aidict.app.ui.viewmodels.SearchViewModel, profileId: Int,
    modifier: Modifier = Modifier
) {
    val state by viewModel.uiState.collectAsState()
    var text by remember { mutableStateOf("") }
    val context = LocalContext.current
    val clipboardManager = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager

    Column(modifier = modifier.fillMaxSize().padding(16.dp)) {
        Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
            if (state.isLoading && state.currentStream.isEmpty()) {
                CircularProgressIndicator(modifier = Modifier.align(androidx.compose.ui.Alignment.Center))
            } else {
                androidx.compose.foundation.lazy.LazyColumn(modifier = Modifier.fillMaxSize()) {
                    item { Text(text = state.currentStream) }
                    state.error?.let {
                        item { Text(text = "Error: $it", color = MaterialTheme.colorScheme.error) }
                    }
                }
            }
        }

        com.aidict.app.ui.components.ChatInputBar(
            inputTerm = text,
            onValueChange = { text = it },
            onSend = { if (state.word != null) viewModel.sendFollowUpMessage(text) else viewModel.streamExplain(text, profileId); text = "" },
            isLoading = state.isLoading,
            isFollowUp = state.word != null,
            onClear = { viewModel.clearCurrentSearch() },
            placeholder = "Paste sentence/paragraph to explain..."
        )
    }
}
