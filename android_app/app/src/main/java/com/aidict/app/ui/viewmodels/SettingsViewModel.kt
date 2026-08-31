package com.aidict.app.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aidict.app.data.AppDatabase
import com.aidict.app.data.LlmRepository
import com.aidict.app.data.entities.AppSetting
import com.aidict.app.data.entities.Profile
import com.aidict.app.utils.DefaultPrompts
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class SettingsViewModel(
    private val database: AppDatabase,
    private val llmRepository: LlmRepository
) : ViewModel() {

    val apiKey = getSettingFlow("OPENROUTER_API_KEY", "")
    val isDarkMode = database.appDao().getSettingsFlow()
        .map { settings -> settings.find { it.key == "DARK_MODE" }?.value?.toBooleanStrictOrNull() ?: true }
        .stateIn(viewModelScope, SharingStarted.Lazily, true)

    val appTheme = getSettingFlow("APP_THEME", "tokyonight")


    val dictModel = getSettingFlow("DICT_MODEL", "inclusionai/ling-3.0-flash")
    val compareModel = getSettingFlow("COMPARE_MODEL", "inclusionai/ling-3.0-flash")
    val explainModel = getSettingFlow("EXPLAIN_MODEL", "inclusionai/ling-3.0-flash")
    val translateModel = getSettingFlow("TRANSLATE_MODEL", "inclusionai/ling-3.0-flash")
    
    val fallbackModels = getSettingFlow("FALLBACK_MODELS", "~deepseek/deepseek-v4-flash-latest")
    val chatModel = getSettingFlow("CHAT_MODEL", "~deepseek/deepseek-v4-flash-latest")

    val dictPrompt = getSettingFlow("DICT_PROMPT", DefaultPrompts.DICT_PROMPT)
    val explainPrompt = getSettingFlow("EXPLAIN_PROMPT", DefaultPrompts.EXPLAIN_PROMPT)
    val starredLanguages = getSettingFlow("STARRED_LANGUAGES", "English, Vietnamese, German, French, Spanish, Japanese, Chinese, Korean, Russian, Italian, Portuguese")
    val allAvailableLanguages = database.appDao().getSettingsFlow().map { s -> com.aidict.app.utils.LanguageManager.getAllAvailable(s.find { it.key == "CUSTOM_LANGUAGES" }?.value) }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, com.aidict.app.utils.LanguageManager.getAllAvailable(null))
    val orderedLanguages = database.appDao().getSettingsFlow().map { s -> com.aidict.app.utils.LanguageManager.getOrderedLanguages(s.find { it.key == "STARRED_LANGUAGES" }?.value, s.find { it.key == "CUSTOM_LANGUAGES" }?.value) }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, com.aidict.app.utils.LanguageManager.getOrderedLanguages(null, null))

    val translatePrompt = getSettingFlow("TRANSLATE_PROMPT", DefaultPrompts.TRANSLATE_PROMPT)
    val comparePrompt = getSettingFlow("COMPARE_PROMPT", DefaultPrompts.COMPARE_PROMPT)
    val externalLinkTemplate = getSettingFlow("EXTERNAL_LINK", "https://dictionary.cambridge.org/dictionary/english/{word}")

    val profiles = database.appDao().getProfiles()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    private val _availableModels = MutableStateFlow<List<String>>(emptyList())
    val availableModels: StateFlow<List<String>> = _availableModels

    init {
        viewModelScope.launch {
            _availableModels.value = llmRepository.fetchModels()
        }
    }

    private fun getSettingFlow(key: String, default: String): StateFlow<String> {
        return database.appDao().getSettingsFlow()
            .map { settings -> settings.find { it.key == key }?.value ?: default }
            .stateIn(viewModelScope, SharingStarted.Lazily, default)
    }

    fun refreshModels() {
        viewModelScope.launch {
            _availableModels.value = llmRepository.fetchModels()
        }
    }

    fun saveSetting(key: String, value: String) {
        viewModelScope.launch {
            database.appDao().insertSetting(AppSetting(key, value))
        }
    }

    fun toggleDarkMode(isDark: Boolean) {
        saveSetting("DARK_MODE", isDark.toString())
    }

    fun createProfile(name: String) {
        viewModelScope.launch {
            database.appDao().insertProfile(Profile(name = name, rank = 0, isDefault = false))
        }
    }

    fun renameProfile(profile: Profile, newName: String) {
        viewModelScope.launch {
            database.appDao().insertProfile(profile.copy(name = newName))
        }
    }

    fun deleteProfile(profile: Profile) {
        viewModelScope.launch {
            database.appDao().deleteProfile(profile)
        }
    }

    fun getDatabase(): AppDatabase = database

    fun setDefaultProfile(profile: Profile) {
        viewModelScope.launch {
            val allProfiles = profiles.value
            allProfiles.forEach { p ->
                if (p.id == profile.id) {
                    database.appDao().insertProfile(p.copy(isDefault = true))
                } else if (p.isDefault) {
                    database.appDao().insertProfile(p.copy(isDefault = false))
                }
            }
        }
    }

    fun moveProfileUp(profile: Profile) {
        viewModelScope.launch {
            val allProfiles = profiles.value.sortedBy { it.rank }.toMutableList()
            val index = allProfiles.indexOfFirst { it.id == profile.id }
            if (index > 0) {
                val above = allProfiles[index - 1]
                val currentRank = profile.rank
                database.appDao().insertProfile(profile.copy(rank = above.rank))
                database.appDao().insertProfile(above.copy(rank = currentRank))
            }
        }
    }

    fun moveProfileDown(profile: Profile) {
        viewModelScope.launch {
            val allProfiles = profiles.value.sortedBy { it.rank }.toMutableList()
            val index = allProfiles.indexOfFirst { it.id == profile.id }
            if (index < allProfiles.size - 1) {
                val below = allProfiles[index + 1]
                val currentRank = profile.rank
                database.appDao().insertProfile(profile.copy(rank = below.rank))
                database.appDao().insertProfile(below.copy(rank = currentRank))
            }
        }
    }


    val bgDict = getSettingFlow("BG_DICT", "").map { it.ifBlank { null } }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val bgCompare = getSettingFlow("BG_COMPARE", "").map { it.ifBlank { null } }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val bgTranslate = getSettingFlow("BG_TRANSLATE", "").map { it.ifBlank { null } }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val bgExplain = getSettingFlow("BG_EXPLAIN", "").map { it.ifBlank { null } }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    
    val bgBlurRadius = getSettingFlow("BG_BLUR_RADIUS", "10.0").map { it.toFloatOrNull() ?: 10f }.stateIn(viewModelScope, SharingStarted.Lazily, 10f)
    val bgOpacity = getSettingFlow("BG_OPACITY", "1.0").map { it.toFloatOrNull() ?: 1f }.stateIn(viewModelScope, SharingStarted.Lazily, 1f)
    
    val bgUniversal = getSettingFlow("BG_UNIVERSAL", "").map { it.ifBlank { null } }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, null)
    val quoteStyle = getSettingFlow("QUOTE_STYLE", "Serif")
    val customQuotes = getSettingFlow("CUSTOM_QUOTES", "")
    val allQuotes = customQuotes.map { custom ->
        val defaults = listOf("Per studium ad sapientiam", "Labor omnia vincit", "Assiduitas mater scientiae", "Nulla dies sine linea", "Carpe diem", "Vincit qui se vincit")
        val customs = custom.split("|").filter { it.isNotBlank() }
        defaults + customs
    }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, listOf("Per studium ad sapientiam", "Labor omnia vincit", "Assiduitas mater scientiae", "Nulla dies sine linea", "Carpe diem", "Vincit qui se vincit"))

    fun addCustomQuote(quote: String) {
        viewModelScope.launch {
            val current = database.appDao().getSetting("CUSTOM_QUOTES")?.value ?: ""
            val newCustom = if (current.isBlank()) quote else "$current|$quote"
            database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("CUSTOM_QUOTES", newCustom))
        }
    }
    val quoteMode = getSettingFlow("QUOTE_MODE", "None")

    fun addCustomLanguage(name: String, flagIso: String) {
        viewModelScope.launch {
            val current = database.appDao().getSetting("CUSTOM_LANGUAGES")?.value ?: ""
            val newEntry = "${name.trim()}|${flagIso.trim()}"
            val newCustom = if (current.isBlank()) newEntry else "$current,$newEntry"
            database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("CUSTOM_LANGUAGES", newCustom))
        }
    }
}
