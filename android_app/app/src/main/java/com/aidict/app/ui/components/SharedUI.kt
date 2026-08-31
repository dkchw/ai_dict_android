package com.aidict.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.SwapHoriz
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.runtime.*
import coil.compose.AsyncImage
import com.aidict.app.models.ExternalLink
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
    externalLinks: List<ExternalLink> = emptyList(),
    onExternalLinkClick: ((ExternalLink) -> Unit)? = null,
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
                    IconButton(
                        onClick = onClear, 
                        modifier = Modifier
                            .padding(bottom = 8.dp, start = 8.dp, end = 8.dp)
                            .background(MaterialTheme.colorScheme.secondaryContainer, CircleShape)
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "New Search", tint = MaterialTheme.colorScheme.onSecondaryContainer)
                    }
                }
                                if (onExternalLinkClick != null && externalLinks.isNotEmpty()) {
                    val firstLink = externalLinks.first()
                    IconButton(
                        onClick = { onExternalLinkClick(firstLink) },
                        modifier = Modifier
                            .padding(bottom = 8.dp, end = if (externalLinks.size > 1) 0.dp else 8.dp)
                            .background(MaterialTheme.colorScheme.tertiaryContainer, CircleShape)
                    ) {
                        if (firstLink.iconUrl.isNotBlank()) {
                            AsyncImage(model = firstLink.iconUrl, contentDescription = firstLink.name, modifier = Modifier.size(24.dp))
                        } else {
                            Icon(Icons.Default.Language, contentDescription = firstLink.name, tint = MaterialTheme.colorScheme.onTertiaryContainer)
                        }
                    }
                    if (externalLinks.size > 1) {
                        var expanded by remember { mutableStateOf(false) }
                        Box(modifier = Modifier.padding(bottom = 8.dp, end = 8.dp)) {
                            IconButton(onClick = { expanded = true }) {
                                Icon(Icons.Default.MoreVert, contentDescription = "More Links")
                            }
                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                externalLinks.drop(1).forEach { link ->
                                    DropdownMenuItem(
                                        text = { Text(link.name) },
                                        onClick = { onExternalLinkClick(link); expanded = false },
                                        leadingIcon = {
                                            if (link.iconUrl.isNotBlank()) {
                                                AsyncImage(model = link.iconUrl, contentDescription = link.name, modifier = Modifier.size(20.dp))
                                            } else {
                                                Icon(Icons.Default.Language, contentDescription = link.name)
                                            }
                                        }
                                    )
                                }
                            }
                        }
                    }
                }
                OutlinedTextField(
                    value = inputTerm,
                    onValueChange = onValueChange,
                    placeholder = { Text(placeholder) },
                    modifier = Modifier.weight(1f),
                    minLines = 1,
                    maxLines = 4,
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
