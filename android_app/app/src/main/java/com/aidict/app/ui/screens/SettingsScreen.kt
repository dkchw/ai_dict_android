package com.aidict.app.ui.screens

import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Add
import androidx.compose.foundation.layout.wrapContentWidth
import androidx.compose.material3.Slider
import androidx.compose.foundation.clickable

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString
import androidx.compose.ui.Alignment
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.Modifier
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.unit.dp
import com.aidict.app.ui.viewmodels.SettingsViewModel
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.ArrowUpward
import androidx.compose.material.icons.filled.ArrowDownward
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
fun SettingsGroup(title: String, content: @Composable () -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    Card(
        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { expanded = !expanded }
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(title, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
                Icon(if (expanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown, contentDescription = "Toggle")
            }
            androidx.compose.animation.AnimatedVisibility(visible = expanded) {
                Column(modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, bottom = 16.dp)) {
                    content()
                }
            }
        }
    }
}

@Composable
@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
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
        item {
            val context = androidx.compose.ui.platform.LocalContext.current
            Row(modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = { com.aidict.app.utils.AutoUpdater(context).checkForUpdates() },
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.tertiary)
                ) { Text("Check Updates") }
                
                Button(
                    onClick = {
                        if (!android.provider.Settings.canDrawOverlays(context)) {
                            val intent = android.content.Intent(android.provider.Settings.ACTION_MANAGE_OVERLAY_PERMISSION, android.net.Uri.parse("package:${context.packageName}"))
                            context.startActivity(intent)
                        } else {
                            val intent = android.content.Intent(context, com.aidict.app.FloatingBubbleService::class.java)
                            context.startService(intent)
                            android.widget.Toast.makeText(context, "Floating Bubble Started", android.widget.Toast.LENGTH_SHORT).show()
                        }
                    },
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                ) { Text("Floating Bubble") }
            }
            val packageInfo = context.packageManager.getPackageInfo(context.packageName, 0)
            val versionName = packageInfo.versionName
            Text(
                "Version: $versionName", 
                style = MaterialTheme.typography.bodySmall, 
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f),
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp), 
                textAlign = androidx.compose.ui.text.style.TextAlign.Center
            )
        }
        item { ExternalDictManager(viewModel) }
        item {
            SettingsGroup("App Behavior") {
                val autoNewSearchStr by viewModel.autoNewSearch.collectAsState()
                val autoNewSearch = autoNewSearchStr.toBooleanStrictOrNull() ?: false
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("Auto New Search", style = MaterialTheme.typography.titleMedium)
                        Text("Automatically clear chat and start a new search when submitting", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Switch(checked = autoNewSearch, onCheckedChange = { viewModel.saveSetting("AUTO_NEW_SEARCH", it.toString()) })
                }
                val enterToSendStr by viewModel.enterToSend.collectAsState()
                val enterToSend = enterToSendStr.toBooleanStrictOrNull() ?: false
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("Enter to Send", style = MaterialTheme.typography.titleMedium)
                        Text("Pressing enter on the keyboard sends the message instead of new line", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Switch(checked = enterToSend, onCheckedChange = { viewModel.saveSetting("ENTER_TO_SEND", it.toString()) })
                }
            }
        }
        item {
            SettingsGroup("Display & Scaling") {
                val uiScaleStr by viewModel.getSettingFlow("UI_SCALE", "1.0").collectAsState()
                var uiScale by remember(uiScaleStr) { mutableStateOf(uiScaleStr.toFloatOrNull() ?: 1.0f) }
                Text(text = "UI Scale: ${java.lang.String.format("%.2f", uiScale)}", modifier = Modifier.padding(top = 8.dp))
                Slider(
                    value = uiScale,
                    onValueChange = { uiScale = it },
                    onValueChangeFinished = { viewModel.saveSetting("UI_SCALE", uiScale.toString()) },
                    valueRange = 0.5f..2.0f
                )
                val textScaleStr by viewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
                var textScale by remember(textScaleStr) { mutableStateOf(textScaleStr.toFloatOrNull() ?: 1.0f) }
                Text(text = "Text Size: ${java.lang.String.format("%.2f", textScale)}", modifier = Modifier.padding(top = 8.dp))
                Slider(
                    value = textScale,
                    onValueChange = { textScale = it },
                    onValueChangeFinished = { viewModel.saveSetting("TEXT_SIZE_SCALE", textScale.toString()) },
                    valueRange = 0.5f..2.0f
                )
            }
        }
        
        item {
            SettingsGroup("Backgrounds") {
                val bgUniversal by viewModel.bgUniversal.collectAsState()
                val universalLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_UNIVERSAL", it.toString()) } }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Universal BG (Fallback)"); Button(onClick = { universalLauncher.launch(arrayOf("image/*")) }) { Text(if (bgUniversal == null) "Select" else "Change") }; if (bgUniversal != null) IconButton(onClick = { viewModel.saveSetting("BG_UNIVERSAL", "") }) { Icon(Icons.Default.Delete, "Clear") } }
                
                val bgDict by viewModel.bgDict.collectAsState()
                val dictLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_DICT", it.toString()) } }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Dict Mode BG"); Button(onClick = { dictLauncher.launch(arrayOf("image/*")) }) { Text(if (bgDict == null) "Select" else "Change") }; if (bgDict != null) IconButton(onClick = { viewModel.saveSetting("BG_DICT", "") }) { Icon(Icons.Default.Delete, "Clear") } }

                val bgCompare by viewModel.bgCompare.collectAsState()
                val compareLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_COMPARE", it.toString()) } }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Compare Mode BG"); Button(onClick = { compareLauncher.launch(arrayOf("image/*")) }) { Text(if (bgCompare == null) "Select" else "Change") }; if (bgCompare != null) IconButton(onClick = { viewModel.saveSetting("BG_COMPARE", "") }) { Icon(Icons.Default.Delete, "Clear") } }

                val bgTranslate by viewModel.bgTranslate.collectAsState()
                val translateLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_TRANSLATE", it.toString()) } }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Translate Mode BG"); Button(onClick = { translateLauncher.launch(arrayOf("image/*")) }) { Text(if (bgTranslate == null) "Select" else "Change") }; if (bgTranslate != null) IconButton(onClick = { viewModel.saveSetting("BG_TRANSLATE", "") }) { Icon(Icons.Default.Delete, "Clear") } }

                val bgExplain by viewModel.bgExplain.collectAsState()
                val explainLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_EXPLAIN", it.toString()) } }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Explain Mode BG"); Button(onClick = { explainLauncher.launch(arrayOf("image/*")) }) { Text(if (bgExplain == null) "Select" else "Change") }; if (bgExplain != null) IconButton(onClick = { viewModel.saveSetting("BG_EXPLAIN", "") }) { Icon(Icons.Default.Delete, "Clear") } }
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

        item {
            SettingsGroup("Inspirational Quote") {
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

            if (quote == "Shuffle") {
                val enabledQuotes by viewModel.shuffleEnabledQuotes.collectAsState()
                val currentEnabled = enabledQuotes ?: allQuotesList
                
                Card(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Quotes included in Shuffle:", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(bottom = 8.dp))
                        allQuotesList.forEach { q ->
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable {
                                val newSet = currentEnabled.toMutableSet()
                                if (newSet.contains(q)) newSet.remove(q) else newSet.add(q)
                                if (newSet.isEmpty()) newSet.add(q) // Ensure at least one
                                viewModel.saveSetting("SHUFFLE_ENABLED_QUOTES", Json.encodeToString(newSet.toList()))
                            }.padding(vertical = 4.dp)) {
                                androidx.compose.material3.Checkbox(
                                    checked = currentEnabled.contains(q),
                                    onCheckedChange = null
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(q, style = MaterialTheme.typography.bodyMedium)
                            }
                        }
                    }
                }
            }
            } // end group
        }

        item { Spacer(Modifier.height(16.dp)) }

        item {
            SettingsGroup("General") {
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                Button(onClick = { exportLauncher.launch("aidict_backup.json") }) {
                    Text("Export Data")
                }
                Button(onClick = { importLauncher.launch(arrayOf("application/json")) }) {
                    Text("Import Data")
                }
            }
        }
        
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
        item {
            SettingsGroup("Languages") {
                com.aidict.app.ui.components.MultiSelectSearchableDropdown(
                    label = "Starred Languages", 
                    currentCsv = viewModel.starredLanguages.collectAsState().value, 
                    options = viewModel.allAvailableLanguages.collectAsState().value, 
                    onCsvChange = { viewModel.saveSetting("STARRED_LANGUAGES", it) }
                )
                
                Spacer(Modifier.height(16.dp))
                Text("Add Custom Language", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(bottom = 8.dp))
                
                var newLangName by remember { mutableStateOf("") }
                var newLangFlag by remember { mutableStateOf("") }
                
                Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    OutlinedTextField(
                        value = newLangName,
                        onValueChange = { newLangName = it },
                        label = { Text("Name (e.g. Dothraki)") },
                        modifier = Modifier.weight(1.5f).padding(end = 8.dp),
                        singleLine = true
                    )
                    OutlinedTextField(
                        value = newLangFlag,
                        onValueChange = { newLangFlag = it },
                        label = { Text("Flag / Icon") },
                        modifier = Modifier.weight(1f).padding(end = 8.dp),
                        singleLine = true
                    )
                    IconButton(
                        onClick = { 
                            if (newLangName.isNotBlank()) {
                                viewModel.addCustomLanguage(newLangName.trim(), newLangFlag.trim())
                                newLangName = ""
                                newLangFlag = ""
                            }
                        }
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "Add Language")
                    }
                }
            }
        }
        item {
            SettingsGroup("API Configuration") {
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
        }
        
        item { Spacer(Modifier.height(16.dp)) }
        item {
            SettingsGroup("Models") {
                Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.End) {
                    Button(onClick = { viewModel.refreshModels() }) { Icon(Icons.Default.Refresh, contentDescription = "Refresh Models", modifier = Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Refresh") }
                }
                SearchableModelDropdown("Dict Model", dictModel, availableModels) { viewModel.saveSetting("DICT_MODEL", it) }
                SearchableModelDropdown("Compare Model", compareModel, availableModels) { viewModel.saveSetting("COMPARE_MODEL", it) }
                SearchableModelDropdown("Explain Model", explainModel, availableModels) { viewModel.saveSetting("EXPLAIN_MODEL", it) }
                SearchableModelDropdown("Translate Model", translateModel, availableModels) { viewModel.saveSetting("TRANSLATE_MODEL", it) }
                SearchableModelDropdown("Fallback Model", fallbackModels, availableModels) { viewModel.saveSetting("FALLBACK_MODELS", it) }
                SearchableModelDropdown("Chat Model", chatModel, availableModels) { viewModel.saveSetting("CHAT_MODEL", it) }
            }
        }

        
        item { Spacer(Modifier.height(16.dp)) }
        

        item { Spacer(Modifier.height(16.dp)) }
        item {
            SettingsGroup("Prompts") {
                OutlinedTextField(value = dictPrompt, onValueChange = { viewModel.saveSetting("DICT_PROMPT", it) }, label = { Text("Dictionary Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), minLines = 3, maxLines = 10)
                OutlinedTextField(value = explainPrompt, onValueChange = { viewModel.saveSetting("EXPLAIN_PROMPT", it) }, label = { Text("Explain Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), minLines = 3, maxLines = 10)
                OutlinedTextField(value = translatePrompt, onValueChange = { viewModel.saveSetting("TRANSLATE_PROMPT", it) }, label = { Text("Translate Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), minLines = 3, maxLines = 10)
                OutlinedTextField(value = comparePrompt, onValueChange = { viewModel.saveSetting("COMPARE_PROMPT", it) }, label = { Text("Compare Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), minLines = 3, maxLines = 10)
            }
        }

        item { Spacer(Modifier.height(16.dp)) }
        item {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Profiles", style = MaterialTheme.typography.titleLarge, modifier = Modifier.weight(1f))
                Button(onClick = { showProfileDialog = true }) { Text("Add Profile") }
            }
        }

        items(profiles.sortedBy { it.rank }, key = { it.id }) { profile ->
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
        }    }

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

@Composable
fun ExternalDictManager(viewModel: com.aidict.app.ui.viewmodels.SettingsViewModel) {
    val externalDictsStr by viewModel.getSettingFlow("EXTERNAL_DICTS", "Cambridge|https://dictionary.cambridge.org/dictionary/english/%s").collectAsState()
    
    val dicts = remember(externalDictsStr) {
        if (externalDictsStr.isBlank()) emptyList()
        else externalDictsStr.split(",").mapNotNull { 
            val parts = it.split("|")
            if (parts.size >= 2) parts[0] to parts[1] else null
        }
    }

    var showDialog by remember { mutableStateOf(false) }

    if (showDialog) {
        var newName by remember { mutableStateOf("") }
        var newUrl by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { showDialog = false },
            title = { Text("Add External Dictionary") },
            text = {
                Column {
                    Text("Use %s for the search word placeholder.", style = MaterialTheme.typography.bodySmall)
                    Spacer(modifier = Modifier.height(8.dp))
                    OutlinedTextField(
                        value = newName,
                        onValueChange = { newName = it },
                        label = { Text("Dictionary Name") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    OutlinedTextField(
                        value = newUrl,
                        onValueChange = { newUrl = it },
                        label = { Text("URL (e.g. https://.../%s)") },
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        if (newName.isNotBlank() && newUrl.contains("%s")) {
                            val newList = dicts + (newName to newUrl)
                            viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}" })
                            showDialog = false
                        }
                    },
                    enabled = newName.isNotBlank() && newUrl.contains("%s")
                ) { Text("Add") }
            },
            dismissButton = {
                TextButton(onClick = { showDialog = false }) { Text("Cancel") }
            }
        )
    }

    SettingsGroup("Floating UI & Bubble Sizing") {
        Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp, vertical = 4.dp)) {
            val bubbleSizeStr by viewModel.getSettingFlow("BUBBLE_SIZE", "160").collectAsState()
            val popupWidthStr by viewModel.getSettingFlow("POPUP_WIDTH", "0.95").collectAsState()
            val popupHeightStr by viewModel.getSettingFlow("POPUP_HEIGHT", "0.90").collectAsState()
            
            var bubbleSize by remember { mutableStateOf<Float?>(null) }
            var popupWidth by remember { mutableStateOf<Float?>(null) }
            var popupHeight by remember { mutableStateOf<Float?>(null) }
            
            val currentBubbleSize = bubbleSize ?: (bubbleSizeStr.toFloatOrNull() ?: 160f)
            val currentPopupWidth = popupWidth ?: (popupWidthStr.toFloatOrNull() ?: 0.95f)
            val currentPopupHeight = popupHeight ?: (popupHeightStr.toFloatOrNull() ?: 0.90f)

            Text("Bubble Size: ${currentBubbleSize.toInt()}px", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = currentBubbleSize,
                onValueChange = { bubbleSize = it },
                onValueChangeFinished = { viewModel.saveSetting("BUBBLE_SIZE", currentBubbleSize.toInt().toString()) },
                valueRange = 80f..320f,
                steps = 23
            )

            Text("Popup Width: ${(currentPopupWidth * 100).toInt()}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = currentPopupWidth,
                onValueChange = { popupWidth = it },
                onValueChangeFinished = { viewModel.saveSetting("POPUP_WIDTH", currentPopupWidth.toString()) },
                valueRange = 0.3f..1.0f,
                steps = 13
            )

            Text("Popup Height: ${(currentPopupHeight * 100).toInt()}%", style = MaterialTheme.typography.bodyMedium)
            androidx.compose.material3.Slider(
                value = currentPopupHeight,
                onValueChange = { popupHeight = it },
                onValueChangeFinished = { viewModel.saveSetting("POPUP_HEIGHT", currentPopupHeight.toString()) },
                valueRange = 0.3f..1.0f,
                steps = 13
            )
        }
    }
    Spacer(Modifier.height(16.dp))
    SettingsGroup("External Dictionaries") {
        Column(modifier = Modifier.fillMaxWidth().padding(8.dp)) {
            dicts.forEachIndexed { index, (name, url) ->
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(name, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        Text(url, style = MaterialTheme.typography.bodySmall, maxLines = 1)
                    }
                    IconButton(onClick = {
                        val newList = dicts.toMutableList().apply { removeAt(index) }
                        viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}" })
                    }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                    }
                }
                androidx.compose.material3.HorizontalDivider()
            }
            
            Button(
                onClick = { showDialog = true },
                modifier = Modifier.align(Alignment.End).padding(top = 8.dp)
            ) {
                Text("Add Link")
            }
        }
    }
}
