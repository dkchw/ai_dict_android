package com.aidict.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.aidict.app.ui.viewmodels.SettingsViewModel
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.outlined.StarBorder
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material.icons.filled.KeyboardArrowDown
import com.aidict.app.data.entities.Profile
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.compose.ui.platform.LocalContext
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.compose.rememberLauncherForActivityResult
import android.content.Intent
import android.net.Uri
import com.aidict.app.ui.viewmodels.BackupHelper
import kotlinx.coroutines.launch
import android.widget.Toast

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(viewModel: SettingsViewModel, modifier: Modifier = Modifier) {
    val apiKey by viewModel.apiKey.collectAsState()
    val isDarkMode by viewModel.isDarkMode.collectAsState()
    val appTheme by viewModel.appTheme.collectAsState()
    val dictModel by viewModel.dictModel.collectAsState()
    val compareModel by viewModel.compareModel.collectAsState()
    val explainModel by viewModel.explainModel.collectAsState()
    val translateModel by viewModel.translateModel.collectAsState()
    val fallbackModels by viewModel.fallbackModels.collectAsState()
    val chatModel by viewModel.chatModel.collectAsState()
    
    val externalLinkTemplate by viewModel.externalLinkTemplate.collectAsState()
            val dictPrompt by viewModel.dictPrompt.collectAsState()
    val explainPrompt by viewModel.explainPrompt.collectAsState()
    val translatePrompt by viewModel.translatePrompt.collectAsState()
    val comparePrompt by viewModel.comparePrompt.collectAsState()
    
    val profiles by viewModel.profiles.collectAsState()
    val availableModels by viewModel.availableModels.collectAsState()

    var showProfileDialog by remember { mutableStateOf(false) }
    var newProfileName by remember { mutableStateOf("") }
    
    var showRenameDialog by remember { mutableStateOf<Profile?>(null) }
    var renameProfileName by remember { mutableStateOf("") }

    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    
    val exportLauncher = rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("application/json")) { uri ->
        uri?.let {
            scope.launch {
                val result = BackupHelper.exportData(context, viewModel.getDatabase(), it)
                if (result.isSuccess) Toast.makeText(context, "Export successful", Toast.LENGTH_SHORT).show()
                else Toast.makeText(context, "Export failed: ${result.exceptionOrNull()?.message}", Toast.LENGTH_LONG).show()
            }
        }
    }
    
    val importLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        uri?.let {
            scope.launch {
                val result = BackupHelper.importData(context, viewModel.getDatabase(), it)
                if (result.isSuccess) Toast.makeText(context, "Import successful. Please restart the app.", Toast.LENGTH_LONG).show()
                else Toast.makeText(context, "Import failed: ${result.exceptionOrNull()?.message}", Toast.LENGTH_LONG).show()
            }
        }
    }

    LazyColumn(modifier = modifier.fillMaxSize().padding(16.dp)) {
        item { Text("Backgrounds", style = MaterialTheme.typography.titleLarge) }

        item {

            val bgDict by viewModel.bgDict.collectAsState()
        val bgUniversal by viewModel.bgUniversal.collectAsState()
            val universalLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->

                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_UNIVERSAL", it.toString()) }

            }

            val dictLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->

                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_DICT", it.toString()) }
            }

            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {

                Text("Universal BG (Fallback)")
                Button(onClick = { universalLauncher.launch(arrayOf("image/*")) }) { Text(if (bgUniversal == null) "Select" else "Change") }
                if (bgUniversal != null) IconButton(onClick = { viewModel.saveSetting("BG_UNIVERSAL", "") }) { Icon(Icons.Default.Delete, "Clear") }
            }
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Dict Mode BG")

                Button(onClick = { dictLauncher.launch(arrayOf("image/*")) }) { Text(if (bgDict == null) "Select" else "Change") }

                if (bgDict != null) IconButton(onClick = { viewModel.saveSetting("BG_DICT", "") }) { Icon(Icons.Default.Delete, "Clear") }

            }

        }

        item {

            val bgCompare by viewModel.bgCompare.collectAsState()

            val compareLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->

                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_COMPARE", it.toString()) }

            }

            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {

                Text("Compare Mode BG")

                Button(onClick = { compareLauncher.launch(arrayOf("image/*")) }) { Text(if (bgCompare == null) "Select" else "Change") }

                if (bgCompare != null) IconButton(onClick = { viewModel.saveSetting("BG_COMPARE", "") }) { Icon(Icons.Default.Delete, "Clear") }

            }

        }

        item {

            val bgTranslate by viewModel.bgTranslate.collectAsState()

            val translateLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->

                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_TRANSLATE", it.toString()) }

            }

            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {

                Text("Translate Mode BG")

                Button(onClick = { translateLauncher.launch(arrayOf("image/*")) }) { Text(if (bgTranslate == null) "Select" else "Change") }

                if (bgTranslate != null) IconButton(onClick = { viewModel.saveSetting("BG_TRANSLATE", "") }) { Icon(Icons.Default.Delete, "Clear") }

            }

        }

        item {

            val bgExplain by viewModel.bgExplain.collectAsState()

            val explainLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->

                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_EXPLAIN", it.toString()) }

            }

            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {

                Text("Explain Mode BG")

                Button(onClick = { explainLauncher.launch(arrayOf("image/*")) }) { Text(if (bgExplain == null) "Select" else "Change") }

                if (bgExplain != null) IconButton(onClick = { viewModel.saveSetting("BG_EXPLAIN", "") }) { Icon(Icons.Default.Delete, "Clear") }

            }

        }

        item {

            val blur by viewModel.bgBlurRadius.collectAsState()

            Column(modifier = Modifier.padding(vertical = 8.dp)) {

                Text("Background Blur Radius: ${blur.toInt()} dp")

                Slider(value = blur, onValueChange = { viewModel.saveSetting("BG_BLUR_RADIUS", it.toString()) }, valueRange = 0f..50f)

            }

        }

        item {

            val opacity by viewModel.bgOpacity.collectAsState()

            Column(modifier = Modifier.padding(vertical = 8.dp)) {

                Text("Background Opacity: ${(opacity * 100).toInt()}%")

                Slider(value = opacity, onValueChange = { viewModel.saveSetting("BG_OPACITY", it.toString()) }, valueRange = 0f..1f)

            }

        }

        item { Text("Inspirational Quote", style = MaterialTheme.typography.titleLarge) }

        item {

            val quote by viewModel.quoteMode.collectAsState()

            val allQuotesList by viewModel.allQuotes.collectAsState()
            val quotes = listOf("None", "Shuffle") + allQuotesList
            var showAddQuoteDialog by remember { mutableStateOf(false) }

            var newQuoteText by remember { mutableStateOf("") }

            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.End) {

                Button(onClick = { showAddQuoteDialog = true }) {

                    Text("Add Custom Quote")

                }

            }

            if (showAddQuoteDialog) {

                AlertDialog(

                    onDismissRequest = { showAddQuoteDialog = false },

                    title = { Text("Add Custom Quote") },

                    text = {

                        OutlinedTextField(value = newQuoteText, onValueChange = { newQuoteText = it }, label = { Text("Quote Text") }, modifier = Modifier.fillMaxWidth())

                    },

                    confirmButton = {

                        Button(onClick = {

                            if (newQuoteText.isNotBlank()) {

                                viewModel.addCustomQuote(newQuoteText.trim())

                                viewModel.saveSetting("QUOTE_MODE", newQuoteText.trim())

                                newQuoteText = ""

                                showAddQuoteDialog = false

                            }

                        }) { Text("Add") }

                    },

                    dismissButton = { TextButton(onClick = { showAddQuoteDialog = false }) { Text("Cancel") } }

                )

            }
            val quoteStyle by viewModel.quoteStyle.collectAsState()
            val styles = listOf("Serif", "Sans Serif", "Monospace", "Cursive")
            com.aidict.app.ui.components.SearchableDropdown(
                label = "Quote Style",
                currentValue = quoteStyle,
                options = styles,
                onSelected = { viewModel.saveSetting("QUOTE_STYLE", it) }
            )

            com.aidict.app.ui.components.SearchableDropdown(

                label = "Display Quote on Empty Screens",

                currentValue = quote,

                options = quotes,

                onSelected = { viewModel.saveSetting("QUOTE_MODE", it) }

            )

        }

        item { Spacer(Modifier.height(16.dp)) }

        item { Text("General", style = MaterialTheme.typography.titleLarge) }
        
        item {
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                Button(onClick = { exportLauncher.launch("aidict_backup.json") }) {
                    Text("Export Data")
                }
                Button(onClick = { importLauncher.launch(arrayOf("application/json")) }) {
                    Text("Import Data")
                }
            }
        }
        
        item {
            var expanded by remember { mutableStateOf(false) }
            ExposedDropdownMenuBox(
                expanded = expanded,
                onExpandedChange = { expanded = !expanded },
                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)
            ) {
                OutlinedTextField(
                    value = when(appTheme) {
                        "light" -> "Light"
                        "dark" -> "Dark"
                        "tokyonight" -> "Tokyo Night (Default)"
                        "nord" -> "Nord"
                        "dracula" -> "Dracula"
                        else -> "Tokyo Night (Default)"
                    },
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("App Theme") },
                    modifier = Modifier.menuAnchor().fillMaxWidth(),
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                    colors = ExposedDropdownMenuDefaults.outlinedTextFieldColors()
                )
                ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                    listOf("light", "dark", "tokyonight", "nord", "dracula").forEach { theme ->
                        DropdownMenuItem(
                            text = { 
                                Text(when(theme) {
                                    "light" -> "Light"
                                    "dark" -> "Dark"
                                    "tokyonight" -> "Tokyo Night (Default)"
                                    "nord" -> "Nord"
                                    "dracula" -> "Dracula"
                                    else -> theme
                                }) 
                            },
                            onClick = {
                                viewModel.saveSetting("APP_THEME", theme)
                                if (theme == "light") viewModel.toggleDarkMode(false)
                                else if (theme == "dark") viewModel.toggleDarkMode(true)
                                expanded = false
                            }
                        )
                    }
                }
            }
        }

        item { Spacer(Modifier.height(16.dp)) }
        item { com.aidict.app.ui.components.MultiSelectSearchableDropdown(label = "Search to add Starred Languages", currentCsv = viewModel.starredLanguages.collectAsState().value, options = viewModel.allAvailableLanguages.collectAsState().value, onCsvChange = { viewModel.saveSetting("STARRED_LANGUAGES", it) }) }
        item {
        }
        item { Text("API Configuration", style = MaterialTheme.typography.titleLarge) }
        item {
            var passwordVisible by remember { mutableStateOf(false) }
            OutlinedTextField(
                value = apiKey,
                onValueChange = { viewModel.saveSetting("OPENROUTER_API_KEY", it) },
                label = { Text("OpenRouter API Key") },
                visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = {
                    val image = if (passwordVisible) Icons.Filled.Visibility else Icons.Filled.VisibilityOff
                    val description = if (passwordVisible) "Hide API key" else "Show API key"
                    IconButton(onClick = { passwordVisible = !passwordVisible }) {
                        Icon(imageVector = image, contentDescription = description)
                    }
                },
                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)
            )
        }
        
        item { Spacer(Modifier.height(16.dp)) }
        item { Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Models", style = MaterialTheme.typography.titleLarge); Button(onClick = { viewModel.refreshModels() }) { Icon(Icons.Default.Refresh, contentDescription = "Refresh Models", modifier = Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Refresh") } } }

        item { SearchableModelDropdown("Dict Model", dictModel, availableModels) { viewModel.saveSetting("DICT_MODEL", it) } }
        item { SearchableModelDropdown("Compare Model", compareModel, availableModels) { viewModel.saveSetting("COMPARE_MODEL", it) } }
        item { SearchableModelDropdown("Explain Model", explainModel, availableModels) { viewModel.saveSetting("EXPLAIN_MODEL", it) } }
        item { SearchableModelDropdown("Translate Model", translateModel, availableModels) { viewModel.saveSetting("TRANSLATE_MODEL", it) } }
        
        item { SearchableModelDropdown("Fallback Model", fallbackModels, availableModels) { viewModel.saveSetting("FALLBACK_MODELS", it) } }
        item { SearchableModelDropdown("Chat Model", chatModel, availableModels) { viewModel.saveSetting("CHAT_MODEL", it) } }

        
        item { Spacer(Modifier.height(16.dp)) }
        item { Text("External Link", style = MaterialTheme.typography.titleLarge) }
        item {
            OutlinedTextField(
                value = externalLinkTemplate, 
                onValueChange = { viewModel.saveSetting("EXTERNAL_LINK", it) }, 
                label = { Text("External Link Template (use {word})") }, 
                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), 
                singleLine = true
            )
        }

        item { Spacer(Modifier.height(16.dp)) }
        item { Text("Prompts", style = MaterialTheme.typography.titleLarge) }
        
        item {
            OutlinedTextField(value = dictPrompt, onValueChange = { viewModel.saveSetting("DICT_PROMPT", it) }, label = { Text("Dictionary Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), minLines = 3, maxLines = 10)
            OutlinedTextField(value = explainPrompt, onValueChange = { viewModel.saveSetting("EXPLAIN_PROMPT", it) }, label = { Text("Explain Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), minLines = 3, maxLines = 10)
            OutlinedTextField(value = translatePrompt, onValueChange = { viewModel.saveSetting("TRANSLATE_PROMPT", it) }, label = { Text("Translate Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), minLines = 3, maxLines = 10)
            OutlinedTextField(value = comparePrompt, onValueChange = { viewModel.saveSetting("COMPARE_PROMPT", it) }, label = { Text("Compare Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), minLines = 3, maxLines = 10)
        }

        item { Spacer(Modifier.height(16.dp)) }
        item {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Profiles", style = MaterialTheme.typography.titleLarge, modifier = Modifier.weight(1f))
                Button(onClick = { showProfileDialog = true }) { Text("Add Profile") }
            }
        }

        items(profiles.sortedBy { it.rank }) { profile ->
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = { viewModel.setDefaultProfile(profile) }) {
                    Icon(if (profile.isDefault) Icons.Default.Star else Icons.Outlined.StarBorder, contentDescription = "Default Profile")
                }
                Text(profile.name, modifier = Modifier.weight(1f))
                IconButton(onClick = { viewModel.moveProfileUp(profile) }) {
                    Icon(Icons.Default.KeyboardArrowUp, contentDescription = "Move Up")
                }
                IconButton(onClick = { viewModel.moveProfileDown(profile) }) {
                    Icon(Icons.Default.KeyboardArrowDown, contentDescription = "Move Down")
                }
                IconButton(onClick = { 
                    renameProfileName = profile.name
                    showRenameDialog = profile 
                }) {
                    Icon(Icons.Default.Edit, contentDescription = "Edit")
                }
                IconButton(onClick = { viewModel.deleteProfile(profile) }) {
                    Icon(Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                }
            }
        }

        item { Spacer(Modifier.height(32.dp)) }
        item {
            val context = androidx.compose.ui.platform.LocalContext.current
            Button(
                onClick = { com.aidict.app.utils.AutoUpdater(context).checkForUpdates() },
                modifier = Modifier.fillMaxWidth()
            ) { Text("Check for Updates") }
        }
    }

    if (showProfileDialog) {
        AlertDialog(
            onDismissRequest = { showProfileDialog = false },
            title = { Text("New Profile") },
            text = {
                OutlinedTextField(
                    value = newProfileName,
                    onValueChange = { newProfileName = it },
                    label = { Text("Profile Name") }
                )
            },
            confirmButton = {
                TextButton(onClick = {
                    if (newProfileName.isNotBlank()) viewModel.createProfile(newProfileName)
                    newProfileName = ""
                    showProfileDialog = false
                }) { Text("Create") }
            },
            dismissButton = {
                TextButton(onClick = { showProfileDialog = false }) { Text("Cancel") }
            }
        )
    }
    
    if (showRenameDialog != null) {
        AlertDialog(
            onDismissRequest = { showRenameDialog = null },
            title = { Text("Rename Profile") },
            text = {
                OutlinedTextField(
                    value = renameProfileName,
                    onValueChange = { renameProfileName = it },
                    label = { Text("Profile Name") }
                )
            },
            confirmButton = {
                TextButton(onClick = {
                    if (renameProfileName.isNotBlank()) viewModel.renameProfile(showRenameDialog!!, renameProfileName)
                    renameProfileName = ""
                    showRenameDialog = null
                }) { Text("Rename") }
            },
            dismissButton = {
                TextButton(onClick = { showRenameDialog = null }) { Text("Cancel") }
            }
        )

    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchableModelDropdown(label: String, currentValue: String, availableModels: List<String>, onSelected: (String) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    var searchText by remember { mutableStateOf(currentValue) }

    ExposedDropdownMenuBox(
        expanded = expanded,
        onExpandedChange = { expanded = !expanded },
        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)
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
            colors = ExposedDropdownMenuDefaults.outlinedTextFieldColors()
        )
        if (availableModels.isNotEmpty()) {
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                val filtered = availableModels.filter { it.contains(searchText, ignoreCase = true) }.take(50)
                filtered.forEach { model ->
                    DropdownMenuItem(
                        text = { Text(model) },
                        onClick = {
                            searchText = model
                            onSelected(model)
                            expanded = false
                        }
                    )
                }
            }
        }
    }
}
