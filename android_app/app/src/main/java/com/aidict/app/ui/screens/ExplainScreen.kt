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

    Column(modifier = modifier.fillMaxSize().scrollable(rememberScrollState(), Orientation.Vertical).padding(16.dp)) {
        Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
            if (state.isLoading && state.currentStream.isEmpty()) {
                com.aidict.app.ui.components.PulsingDots(modifier = Modifier.align(androidx.compose.ui.Alignment.Center))
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
            availableLanguages = viewModel.orderedLanguages.collectAsState().value,
            inputTerm = viewModel.explainInput,
            onValueChange = { viewModel.explainInput = it },
            onSend = { if (state.word != null) viewModel.sendFollowUpMessage(viewModel.explainInput, "explain") else viewModel.streamExplain(viewModel.explainInput, sourceLang, targetLang, profileId); viewModel.explainInput = "" },
            isLoading = state.isLoading,
            isFollowUp = state.word != null,
            sourceLang = if (state.word == null) sourceLang else null,
            targetLang = if (state.word == null) targetLang else null,
            onSourceLangChange = if (state.word == null) { { sourceLang = it; viewModel.saveProfileSetting(profileId, "EXPLAIN_SOURCE", it) } } else null,
            onTargetLangChange = if (state.word == null) { { targetLang = it; viewModel.saveProfileSetting(profileId, "EXPLAIN_TARGET", it) } } else null,
            onClear = { viewModel.clearCurrentSearch() },
            placeholder = if (state.word != null) "Enter your question..." else "Paste sentence/paragraph to explain..."
        )
    }
}
