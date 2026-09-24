package com.aidict.app

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.CompareArrows
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.lifecycleScope
import com.aidict.app.data.AppDatabase
import com.aidict.app.data.LocalTranslationEngine
import com.aidict.app.data.entities.AppSetting
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.util.Locale

class TranslateActivity : ComponentActivity(), TextToSpeech.OnInitListener {

    private var tts: TextToSpeech? = null
    private var isTtsReady = false

    private val inputQueryState = mutableStateOf("")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        tts = TextToSpeech(this, this)

        val extracted = extractText(intent)
        inputQueryState.value = extracted

        val database = AppDatabase.getDatabase(this)

        setContent {
            TranslateScreenUI(
                database = database,
                initialText = inputQueryState.value,
                onSpeak = { text, langName -> speak(text, langName) },
                onSendToAiDict = { query, targetMode ->
                    val popupIntent = Intent(this, PopupActivity::class.java).apply {
                        action = Intent.ACTION_SEND
                        putExtra(Intent.EXTRA_TEXT, query)
                        putExtra("EXTRA_MODE", targetMode)
                        flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
                    }
                    startActivity(popupIntent)
                    finish()
                },
                onClose = { finish() }
            )
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        val extracted = extractText(intent)
        if (extracted.isNotBlank()) {
            inputQueryState.value = extracted
        }
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            isTtsReady = true
        }
    }

    private fun speak(text: String, langName: String) {
        if (!isTtsReady || tts == null || text.isBlank()) return
        val tag = LocalTranslationEngine.getLanguageTag(langName) ?: "en"
        val locale = Locale.forLanguageTag(tag)
        tts?.language = locale
        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "translate_tts_${System.currentTimeMillis()}")
    }

    override fun onDestroy() {
        tts?.stop()
        tts?.shutdown()
        tts = null
        super.onDestroy()
    }

    private fun extractText(intent: Intent?): String {
        if (intent == null) return ""
        return intent.getCharSequenceExtra(Intent.EXTRA_PROCESS_TEXT)?.toString()
            ?: intent.getStringExtra(Intent.EXTRA_TEXT)
            ?: intent.getStringExtra("EXTRA_QUERY")
            ?: intent.getStringExtra(android.app.SearchManager.QUERY)
            ?: ""
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TranslateScreenUI(
    database: AppDatabase,
    initialText: String,
    onSpeak: (String, String) -> Unit,
    onSendToAiDict: (String, String) -> Unit,
    onClose: () -> Unit
) {
    val context = LocalContext.current
    val clipboardManager = remember { context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager }
    val coroutineScope = rememberCoroutineScope()

    var sourceText by remember { mutableStateOf(initialText) }
    var translatedText by remember { mutableStateOf("") }
    var detectedSourceLang by remember { mutableStateOf<String?>(null) }
    var isLoading by remember { mutableStateOf(false) }
    var isDownloadingModel by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    var sourceLanguage by remember { mutableStateOf("Auto Detect") }
    var targetLanguage by remember { mutableStateOf("English") }
    var mtTier by remember { mutableStateOf(LocalTranslationEngine.Tier.NORMAL) }
    var profileId by remember { mutableIntStateOf(1) }
    var appTheme by remember { mutableStateOf("tokyonight") }

    LaunchedEffect(Unit) {
        val savedProfileId = database.appDao().getSetting("ACTIVE_PROFILE_ID")?.value?.toIntOrNull()
        val defaultProfile = database.appDao().getDefaultProfile()
        val pId = savedProfileId ?: defaultProfile?.id ?: 1
        profileId = pId
        sourceLanguage = database.appDao().getSetting("CORRECT_SOURCE")?.value ?: "Auto Detect"
        targetLanguage = database.appDao().getSetting("CORRECT_TARGET")?.value ?: "English"
        val tierStr = database.appDao().getSetting("CORRECT_MT_TIER")?.value ?: "normal"
        mtTier = if (tierStr == "strong") LocalTranslationEngine.Tier.STRONG else LocalTranslationEngine.Tier.NORMAL
        appTheme = database.appDao().getSetting("APP_THEME")?.value ?: "tokyonight"
    }

    val colorScheme = when (appTheme) {
        "light" -> lightColorScheme()
        "dark" -> darkColorScheme()
        "nord" -> com.aidict.app.ui.theme.NordColors
        "dracula" -> com.aidict.app.ui.theme.DraculaColors
        "tokyonight" -> com.aidict.app.ui.theme.TokyoNightColors
        else -> com.aidict.app.ui.theme.TokyoNightColors
    }

    val supportedLanguages = remember { LocalTranslationEngine.getSupportedLanguages() }
    val sourceOptions = remember { listOf("Auto Detect") + supportedLanguages }

    var translationJob by remember { mutableStateOf<Job?>(null) }

    fun doTranslate(text: String, src: String, tgt: String, tier: LocalTranslationEngine.Tier) {
        val trimmed = text.trim()
        if (trimmed.isBlank()) {
            translatedText = ""
            errorMessage = null
            isLoading = false
            return
        }

        translationJob?.cancel()
        translationJob = coroutineScope.launch {
            isLoading = true
            errorMessage = null
            isDownloadingModel = false

            val result = LocalTranslationEngine.translate(
                text = trimmed,
                sourceLanguage = src,
                targetLanguage = tgt,
                tier = tier,
                onDownloadingModel = { downloading ->
                    isDownloadingModel = downloading
                }
            )

            isLoading = false
            isDownloadingModel = false

            if (result.isSuccess) {
                val res = result.getOrThrow()
                translatedText = res.translatedText
                detectedSourceLang = res.sourceLanguageName
                errorMessage = null
            } else {
                translatedText = ""
                errorMessage = result.exceptionOrNull()?.localizedMessage ?: "Translation failed"
            }
        }
    }

    // Trigger initial translation when sourceText or languages change
    LaunchedEffect(sourceText, sourceLanguage, targetLanguage, mtTier) {
        delay(200) // Small debounce
        doTranslate(sourceText, sourceLanguage, targetLanguage, mtTier)
    }

    MaterialTheme(colorScheme = colorScheme) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.55f))
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null
                ) {
                    onClose()
                },
            contentAlignment = Alignment.Center
        ) {
            Surface(
                modifier = Modifier
                    .fillMaxWidth(0.92f)
                    .widthIn(max = 520.dp)
                    .padding(vertical = 24.dp)
                    .clickable(
                        interactionSource = remember { MutableInteractionSource() },
                        indication = null
                    ) { /* prevent click-through */ },
                shape = RoundedCornerShape(20.dp),
                color = MaterialTheme.colorScheme.surface,
                tonalElevation = 8.dp,
                shadowElevation = 12.dp
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
                        .verticalScroll(rememberScrollState())
                ) {
                    // Header Bar
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Default.Translate,
                            contentDescription = "Translate",
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(24.dp)
                        )
                        Spacer(Modifier.width(8.dp))
                        Text(
                            text = "AI Dict Translate",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )

                        Spacer(Modifier.weight(1f))

                        // Tier selector chip
                        FilterChip(
                            selected = mtTier == LocalTranslationEngine.Tier.STRONG,
                            onClick = {
                                val newTier = if (mtTier == LocalTranslationEngine.Tier.NORMAL) {
                                    LocalTranslationEngine.Tier.STRONG
                                } else {
                                    LocalTranslationEngine.Tier.NORMAL
                                }
                                mtTier = newTier
                                coroutineScope.launch {
                                    database.appDao().insertSetting(AppSetting("CORRECT_MT_TIER", newTier.id))
                                }
                            },
                            label = {
                                Text(
                                    text = if (mtTier == LocalTranslationEngine.Tier.STRONG) "Strong (NLLB)" else "Normal (Offline)",
                                    style = MaterialTheme.typography.labelSmall
                                )
                            },
                            leadingIcon = {
                                Icon(
                                    imageVector = if (mtTier == LocalTranslationEngine.Tier.STRONG) Icons.Default.Check else Icons.Default.OfflinePin,
                                    contentDescription = null,
                                    modifier = Modifier.size(14.dp)
                                )
                            },
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                                selectedLabelColor = MaterialTheme.colorScheme.onPrimaryContainer
                            )
                        )

                        Spacer(Modifier.width(4.dp))

                        IconButton(onClick = onClose, modifier = Modifier.size(32.dp)) {
                            Icon(Icons.Default.Close, contentDescription = "Close", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }

                    Spacer(Modifier.height(12.dp))

                    // Language Selector Bar
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), RoundedCornerShape(12.dp))
                            .padding(horizontal = 8.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        // Source Language Menu
                        var srcExpanded by remember { mutableStateOf(false) }
                        Box(modifier = Modifier.weight(1f)) {
                            TextButton(
                                onClick = { srcExpanded = true },
                                modifier = Modifier.fillMaxWidth(),
                                contentPadding = PaddingValues(horizontal = 4.dp, vertical = 2.dp)
                            ) {
                                Text(
                                    text = if (sourceLanguage == "Auto Detect" && !detectedSourceLang.isNullOrBlank()) {
                                        "Auto (${detectedSourceLang})"
                                    } else {
                                        sourceLanguage
                                    },
                                    style = MaterialTheme.typography.labelMedium,
                                    maxLines = 1
                                )
                                Icon(Icons.Default.ArrowDropDown, contentDescription = null, modifier = Modifier.size(18.dp))
                            }
                            DropdownMenu(
                                expanded = srcExpanded,
                                onDismissRequest = { srcExpanded = false }
                            ) {
                                sourceOptions.forEach { lang ->
                                    DropdownMenuItem(
                                        text = { Text(lang) },
                                        onClick = {
                                            sourceLanguage = lang
                                            srcExpanded = false
                                            coroutineScope.launch {
                                                database.appDao().insertSetting(AppSetting("CORRECT_SOURCE", lang))
                                            }
                                        }
                                    )
                                }
                            }
                        }

                        // Swap Button
                        IconButton(
                            onClick = {
                                if (sourceLanguage != "Auto Detect") {
                                    val temp = sourceLanguage
                                    sourceLanguage = targetLanguage
                                    targetLanguage = temp
                                    coroutineScope.launch {
                                        database.appDao().insertSetting(AppSetting("CORRECT_SOURCE", sourceLanguage))
                                        database.appDao().insertSetting(AppSetting("CORRECT_TARGET", targetLanguage))
                                    }
                                } else if (!detectedSourceLang.isNullOrBlank()) {
                                    sourceLanguage = targetLanguage
                                    targetLanguage = detectedSourceLang!!
                                    coroutineScope.launch {
                                        database.appDao().insertSetting(AppSetting("CORRECT_SOURCE", sourceLanguage))
                                        database.appDao().insertSetting(AppSetting("CORRECT_TARGET", targetLanguage))
                                    }
                                }
                            },
                            modifier = Modifier.size(36.dp)
                        ) {
                            Icon(
                                imageVector = Icons.AutoMirrored.Filled.CompareArrows,
                                contentDescription = "Swap Languages",
                                tint = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.size(20.dp)
                            )
                        }

                        // Target Language Menu
                        var tgtExpanded by remember { mutableStateOf(false) }
                        Box(modifier = Modifier.weight(1f)) {
                            TextButton(
                                onClick = { tgtExpanded = true },
                                modifier = Modifier.fillMaxWidth(),
                                contentPadding = PaddingValues(horizontal = 4.dp, vertical = 2.dp)
                            ) {
                                Text(
                                    text = targetLanguage,
                                    style = MaterialTheme.typography.labelMedium,
                                    maxLines = 1
                                )
                                Icon(Icons.Default.ArrowDropDown, contentDescription = null, modifier = Modifier.size(18.dp))
                            }
                            DropdownMenu(
                                expanded = tgtExpanded,
                                onDismissRequest = { tgtExpanded = false }
                            ) {
                                supportedLanguages.forEach { lang ->
                                    DropdownMenuItem(
                                        text = { Text(lang) },
                                        onClick = {
                                            targetLanguage = lang
                                            tgtExpanded = false
                                            coroutineScope.launch {
                                                database.appDao().insertSetting(AppSetting("CORRECT_TARGET", lang))
                                            }
                                        }
                                    )
                                }
                            }
                        }
                    }

                    Spacer(Modifier.height(12.dp))

                    // Source Text Input Box
                    OutlinedTextField(
                        value = sourceText,
                        onValueChange = { sourceText = it },
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 100.dp, max = 160.dp),
                        placeholder = { Text("Enter text to translate...") },
                        textStyle = MaterialTheme.typography.bodyLarge,
                        shape = RoundedCornerShape(12.dp),
                        trailingIcon = {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                if (sourceText.isNotBlank()) {
                                    IconButton(onClick = { sourceText = "" }, modifier = Modifier.size(32.dp)) {
                                        Icon(Icons.Default.Clear, contentDescription = "Clear", modifier = Modifier.size(18.dp))
                                    }
                                } else {
                                    IconButton(
                                        onClick = {
                                            val clip = clipboardManager.primaryClip?.getItemAt(0)?.text?.toString() ?: ""
                                            if (clip.isNotBlank()) {
                                                sourceText = clip
                                            }
                                        },
                                        modifier = Modifier.size(32.dp)
                                    ) {
                                        Icon(Icons.Default.ContentPaste, contentDescription = "Paste", modifier = Modifier.size(18.dp))
                                    }
                                }
                                if (sourceText.isNotBlank()) {
                                    IconButton(
                                        onClick = { onSpeak(sourceText, detectedSourceLang ?: sourceLanguage) },
                                        modifier = Modifier.size(32.dp)
                                    ) {
                                        Icon(Icons.AutoMirrored.Filled.VolumeUp, contentDescription = "Listen", modifier = Modifier.size(18.dp))
                                    }
                                }
                            }
                        }
                    )

                    Spacer(Modifier.height(12.dp))

                    // Translated Result Area
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 100.dp),
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer)
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(12.dp)
                        ) {
                            if (isLoading) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 16.dp),
                                    horizontalArrangement = Arrangement.Center,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    CircularProgressIndicator(
                                        modifier = Modifier.size(20.dp),
                                        strokeWidth = 2.dp,
                                        color = MaterialTheme.colorScheme.primary
                                    )
                                    Spacer(Modifier.width(10.dp))
                                    Text(
                                        text = if (isDownloadingModel) "Downloading offline language pack (~30MB)..." else "Translating...",
                                        style = MaterialTheme.typography.bodyMedium,
                                        color = MaterialTheme.colorScheme.onSecondaryContainer
                                    )
                                }
                            } else if (!errorMessage.isNullOrBlank()) {
                                Column(modifier = Modifier.fillMaxWidth()) {
                                    Text(
                                        text = errorMessage!!,
                                        style = MaterialTheme.typography.bodyMedium,
                                        color = MaterialTheme.colorScheme.error
                                    )
                                    Spacer(Modifier.height(6.dp))
                                    TextButton(
                                        onClick = { doTranslate(sourceText, sourceLanguage, targetLanguage, mtTier) },
                                        modifier = Modifier.align(Alignment.End)
                                    ) {
                                        Icon(Icons.Default.Refresh, contentDescription = null, modifier = Modifier.size(16.dp))
                                        Spacer(Modifier.width(4.dp))
                                        Text("Retry")
                                    }
                                }
                            } else if (translatedText.isNotBlank()) {
                                SelectionContainer {
                                    Text(
                                        text = translatedText,
                                        style = MaterialTheme.typography.bodyLarge,
                                        color = MaterialTheme.colorScheme.onSecondaryContainer
                                    )
                                }

                                Spacer(Modifier.height(8.dp))

                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.End
                                ) {
                                    IconButton(
                                        onClick = { onSpeak(translatedText, targetLanguage) },
                                        modifier = Modifier.size(32.dp)
                                    ) {
                                        Icon(
                                            Icons.AutoMirrored.Filled.VolumeUp,
                                            contentDescription = "Listen translation",
                                            tint = MaterialTheme.colorScheme.primary,
                                            modifier = Modifier.size(18.dp)
                                        )
                                    }

                                    Spacer(Modifier.width(4.dp))

                                    IconButton(
                                        onClick = {
                                            val clip = ClipData.newPlainText("Translation", translatedText)
                                            clipboardManager.setPrimaryClip(clip)
                                            Toast.makeText(context, "Translation copied to clipboard", Toast.LENGTH_SHORT).show()
                                        },
                                        modifier = Modifier.size(32.dp)
                                    ) {
                                        Icon(
                                            Icons.Default.ContentCopy,
                                            contentDescription = "Copy translation",
                                            tint = MaterialTheme.colorScheme.primary,
                                            modifier = Modifier.size(18.dp)
                                        )
                                    }
                                }
                            } else {
                                Text(
                                    text = "Translation will appear here...",
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onSecondaryContainer.copy(alpha = 0.6f)
                                )
                            }
                        }
                    }

                    Spacer(Modifier.height(16.dp))

                    // Deepen with AI LLM Section
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp),
                        color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.45f)
                    ) {
                        Column(modifier = Modifier.padding(10.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    Icons.Default.AutoAwesome,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(Modifier.width(6.dp))
                                Text(
                                    text = "Need deeper analysis or grammar polish?",
                                    style = MaterialTheme.typography.labelMedium,
                                    fontWeight = FontWeight.SemiBold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                            }

                            Spacer(Modifier.height(8.dp))

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                FilledTonalButton(
                                    onClick = { onSendToAiDict(sourceText, "dict") },
                                    modifier = Modifier.weight(1f),
                                    contentPadding = PaddingValues(horizontal = 6.dp, vertical = 4.dp)
                                ) {
                                    Text("📚 Dict", style = MaterialTheme.typography.labelSmall)
                                }

                                FilledTonalButton(
                                    onClick = { onSendToAiDict(sourceText, "explain") },
                                    modifier = Modifier.weight(1f),
                                    contentPadding = PaddingValues(horizontal = 6.dp, vertical = 4.dp)
                                ) {
                                    Text("🧠 Explain", style = MaterialTheme.typography.labelSmall)
                                }

                                FilledTonalButton(
                                    onClick = { onSendToAiDict(sourceText, "correct") },
                                    modifier = Modifier.weight(1f),
                                    contentPadding = PaddingValues(horizontal = 6.dp, vertical = 4.dp)
                                ) {
                                    Text("✍️ Correct", style = MaterialTheme.typography.labelSmall)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
