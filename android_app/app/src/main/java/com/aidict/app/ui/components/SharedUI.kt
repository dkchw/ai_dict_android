package com.aidict.app.ui.components
import androidx.compose.animation.core.*

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.SwapHoriz
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.draw.clip
import androidx.compose.foundation.combinedClickable


import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.runtime.*
import coil.compose.AsyncImage
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchableDropdown(
    label: String,
    currentValue: String,
    options: List<String>,
    onSelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var expanded by remember { mutableStateOf(false) }
    var searchText by remember { mutableStateOf(currentValue) }

    LaunchedEffect(currentValue) {
        if (currentValue != searchText) searchText = currentValue
    }

    ExposedDropdownMenuBox(
        expanded = expanded,
        onExpandedChange = { expanded = !expanded },
        modifier = modifier
    ) {
        OutlinedTextField(
            value = searchText,
            onValueChange = { 
                searchText = it 
                expanded = true
                onSelected(it)
            },
            label = { Text(label) },
            modifier = Modifier.menuAnchor().fillMaxWidth(),
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
            colors = ExposedDropdownMenuDefaults.outlinedTextFieldColors(),
            singleLine = true
        )
        if (options.isNotEmpty()) {
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                val filtered = options.filter { it.contains(searchText, ignoreCase = true) }.take(50)
                filtered.forEach { option ->
                    DropdownMenuItem(
                        text = { Text(option) },
                        onClick = {
                            searchText = option
                            onSelected(option)
                            expanded = false
                        }
                    )
                }
            }
        }
    }
}


val LANGUAGE_CODES = mapOf(
    "Auto Detect" to "🤖 Auto",
    "English" to "🇬🇧 EN",
    "Vietnamese" to "🇻🇳 VI",
    "French" to "🇫🇷 FR",
    "Spanish" to "🇪🇸 ES",
    "German" to "🇩🇪 DE",
    "Japanese" to "🇯🇵 JA",
    "Chinese" to "🇨🇳 ZH",
    "Korean" to "🇰🇷 KO",
    "Russian" to "🇷🇺 RU",
    "Italian" to "🇮🇹 IT",
    "Portuguese" to "🇵🇹 PT",
    "Dutch" to "🇳🇱 NL",
    "Arabic" to "🇸🇦 AR"
)

@Composable
fun SmallLanguageSelector(
    availableLanguages: List<String>,

    currentValue: String,
    onSelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var expanded by remember { mutableStateOf(false) }
    Box(modifier = modifier) {
        TextButton(
            onClick = { expanded = true },
            contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)
        ) {
            val display = com.aidict.app.utils.LanguageManager.getDisplayFlag(currentValue)
            Text(display, style = MaterialTheme.typography.labelLarge)
            Icon(Icons.Default.ArrowDropDown, contentDescription = null, modifier = Modifier.size(16.dp))
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            availableLanguages.forEach { lang ->
                DropdownMenuItem(
                    text = { Text("${com.aidict.app.utils.LanguageManager.getDisplayFlag(lang)} $lang") },
                    onClick = {
                        onSelected(lang)
                        expanded = false
                    }
                )
            }
        }
    }
}

@Composable
fun ChatInputBar(
    availableLanguages: List<String> = com.aidict.app.utils.LanguageManager.defaultLanguages,

    inputTerm: String,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit,
    isLoading: Boolean,
    placeholder: String,
    isFollowUp: Boolean = false,
    sourceLang: String? = null,
    targetLang: String? = null,
    onSourceLangChange: ((String) -> Unit)? = null,
    onTargetLangChange: ((String) -> Unit)? = null,
    onClear: (() -> Unit)? = null,
    autoNewSearch: Boolean = false,
    onToggleAutoNewSearch: (() -> Unit)? = null,
    enterToSend: Boolean = false,
    modifier: Modifier = Modifier
) {
    Surface(
        shape = RoundedCornerShape(24.dp),
        color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
        tonalElevation = 2.dp,
        modifier = modifier.fillMaxWidth().padding(top = 8.dp, bottom = 8.dp)
    ) {
        Column(modifier = Modifier.padding(start = 8.dp, end = 8.dp, top = 4.dp, bottom = 8.dp)) {
            if (sourceLang != null && targetLang != null && onSourceLangChange != null && onTargetLangChange != null) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(start = 8.dp),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    SmallLanguageSelector(availableLanguages = availableLanguages, currentValue = sourceLang, onSelected = onSourceLangChange)
                    IconButton(
                        onClick = { 
                            onSourceLangChange(targetLang)
                            onTargetLangChange(sourceLang)
                        },
                        modifier = Modifier.padding(horizontal = 4.dp).size(24.dp)
                    ) {
                        Icon(Icons.Default.SwapHoriz, contentDescription = "Swap Languages", modifier = Modifier.size(16.dp))
                    }
                    SmallLanguageSelector(availableLanguages = availableLanguages, currentValue = targetLang, onSelected = onTargetLangChange)
                }
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.Bottom
            ) {
                if (onClear != null) {
                    androidx.compose.foundation.layout.Box(
                        contentAlignment = Alignment.Center,
                        modifier = Modifier
                            .padding(bottom = 8.dp, start = 8.dp, end = 8.dp)
                            .size(40.dp)
                            .background(if (autoNewSearch) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.secondaryContainer, CircleShape)
                            .clip(CircleShape)
                            .then(
                                @OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
                                Modifier.combinedClickable(
                                    onClick = onClear,
                                    onLongClick = onToggleAutoNewSearch
                                )
                            )
                    ) {
                        Icon(
                            if (autoNewSearch) Icons.Default.Bolt else Icons.Default.Add, 
                            contentDescription = "New Search", 
                            tint = if (autoNewSearch) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSecondaryContainer,
                            modifier = Modifier.size(24.dp)
                        )
                    }
                }

                OutlinedTextField(
                    value = inputTerm,
                    onValueChange = onValueChange,
                    placeholder = { Text(placeholder) },
                    modifier = Modifier.weight(1f),
                    minLines = 1,
                    maxLines = 4,
                    keyboardOptions = androidx.compose.foundation.text.KeyboardOptions.Default.copy(
                        imeAction = if (enterToSend) androidx.compose.ui.text.input.ImeAction.Send else androidx.compose.ui.text.input.ImeAction.Default
                    ),
                    keyboardActions = androidx.compose.foundation.text.KeyboardActions(
                        onSend = { if (inputTerm.isNotBlank() && !isLoading) onSend() }
                    ),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Color.Transparent,
                        unfocusedBorderColor = Color.Transparent,
                        focusedContainerColor = Color.Transparent,
                        unfocusedContainerColor = Color.Transparent
                    )
                )
                Spacer(modifier = Modifier.width(8.dp))
                IconButton(
                    onClick = onSend,
                    enabled = inputTerm.isNotBlank() && !isLoading,
                    modifier = Modifier
                        .padding(bottom = 8.dp)
                        .background(MaterialTheme.colorScheme.primary, CircleShape)
                ) {
                    Icon(
                        if (isFollowUp) Icons.AutoMirrored.Filled.Send else Icons.Default.Search, 
                        contentDescription = "Send",
                        tint = MaterialTheme.colorScheme.onPrimary
                    )
                }
            }
        }
    }
}

@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun MultiSelectSearchableDropdown(
    label: String,
    currentCsv: String,
    options: List<String>,
    onCsvChange: (String) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    var searchText by remember { mutableStateOf("") }
    
    val selectedItems = currentCsv.split(",").map { it.trim() }.filter { it.isNotBlank() }

    Column(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = { expanded = !expanded }
        ) {
            OutlinedTextField(
                value = searchText,
                onValueChange = { searchText = it; expanded = true },
                label = { Text(label) },
                modifier = Modifier.menuAnchor().fillMaxWidth(),
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                colors = ExposedDropdownMenuDefaults.outlinedTextFieldColors()
            )
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                val filtered = options.filter { it.contains(searchText, ignoreCase = true) }.take(10)
                filtered.forEach { option ->
                    DropdownMenuItem(
                        text = { Text(option) },
                        onClick = {
                            val newItems = if (selectedItems.contains(option)) {
                                selectedItems - option
                            } else {
                                selectedItems + option
                            }
                            onCsvChange(newItems.joinToString(", "))
                            searchText = ""
                            expanded = false
                        }
                    )
                }
            }
        }
        
        // Display selected items as chips
        @OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
        androidx.compose.foundation.layout.FlowRow(modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) {
            selectedItems.forEach { item ->
                InputChip(
                    selected = true,
                    onClick = {
                        onCsvChange((selectedItems - item).joinToString(", "))
                    },
                    label = { Text(com.aidict.app.utils.LanguageManager.getDisplayFlag(item)) },
                    trailingIcon = { Icon(Icons.Default.Delete, contentDescription = "Remove", modifier = Modifier.size(16.dp)) },
                    modifier = Modifier.padding(end = 4.dp, bottom = 4.dp)
                )
            }
        }
    }
}


@Composable
fun PulsingDots(modifier: Modifier = Modifier) {
    val transition = rememberInfiniteTransition()
    val scales = (0..2).map { index ->
        transition.animateFloat(
            initialValue = 0.5f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 600, delayMillis = index * 200, easing = LinearEasing),
                repeatMode = RepeatMode.Reverse
            )
        )
    }

    Row(modifier = modifier.padding(16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        scales.forEach { scale ->
            Box(
                modifier = Modifier
                    .size(8.dp)
                    .background(MaterialTheme.colorScheme.primary.copy(alpha = scale.value), CircleShape)
            )
        }
    }
}
