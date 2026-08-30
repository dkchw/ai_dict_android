cat << 'INNER_EOF' > android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt
package com.aidict.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
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

val SUPPORTED_LANGUAGES = listOf("Auto Detect", "English", "Vietnamese", "French", "Spanish", "German", "Japanese", "Chinese", "Korean", "Russian", "Italian", "Portuguese", "Dutch", "Arabic")

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
            val display = LANGUAGE_CODES[currentValue] ?: currentValue.take(4)
            Text(display, style = MaterialTheme.typography.labelLarge)
            Icon(Icons.Default.ArrowDropDown, contentDescription = null, modifier = Modifier.size(16.dp))
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            SUPPORTED_LANGUAGES.forEach { lang ->
                DropdownMenuItem(
                    text = { Text("${LANGUAGE_CODES[lang] ?: ""} $lang") },
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
                    horizontalArrangement = Arrangement.Start,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    SmallLanguageSelector(currentValue = sourceLang, onSelected = onSourceLangChange)
                    Icon(Icons.Default.ArrowForward, contentDescription = "To", modifier = Modifier.padding(horizontal = 4.dp).size(14.dp))
                    SmallLanguageSelector(currentValue = targetLang, onSelected = onTargetLangChange)
                }
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.Bottom
            ) {
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
INNER_EOF
