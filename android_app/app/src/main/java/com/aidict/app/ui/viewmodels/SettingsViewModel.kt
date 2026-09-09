package com.aidict.app.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString
import kotlinx.serialization.decodeFromString
import com.aidict.app.data.AppDatabase
import com.aidict.app.data.LlmRepository
import com.aidict.app.data.entities.AppSetting
import com.aidict.app.data.entities.Profile
import com.aidict.app.utils.DefaultPrompts
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

data class ProfileSettingItem(
    val key: String,
    val effectiveValue: String,
    val isCustom: Boolean,
    val globalValue: String,
    val defaultValue: String
)

data class ProfileAiConfig(
    val selectedProfileId: Int?,
    val selectedProfileName: String,
    val dictModel: ProfileSettingItem,
    val compareModel: ProfileSettingItem,
    val explainModel: ProfileSettingItem,
    val translateModel: ProfileSettingItem,
    val fallbackModels: ProfileSettingItem,
    val chatModel: ProfileSettingItem,
    val dictReasoning: ProfileSettingItem,
    val compareReasoning: ProfileSettingItem,
    val explainReasoning: ProfileSettingItem,
    val translateReasoning: ProfileSettingItem,
    val fallbackReasoning: ProfileSettingItem,
    val chatReasoning: ProfileSettingItem,
    val dictPrompt: ProfileSettingItem,
    val comparePrompt: ProfileSettingItem,
    val explainPrompt: ProfileSettingItem,
    val translatePrompt: ProfileSettingItem,
    val hasCustomOverrides: Boolean
)

class SettingsViewModel(
    private val database: AppDatabase,
    private val llmRepository: LlmRepository
) : ViewModel() {

    val apiKey = getSettingFlow("OPENROUTER_API_KEY", "")
    val isDarkMode = database.appDao().getSettingsFlow()
        .map { settings -> settings.find { it.key == "DARK_MODE" }?.value?.toBooleanStrictOrNull() ?: true }
        .stateIn(viewModelScope, SharingStarted.Lazily, true)

    val appTheme = getSettingFlow("APP_THEME", "tokyonight")


    val dictModel = getSettingFlow("DICT_MODEL", "~deepseek/deepseek-v4-flash-latest")
    val compareModel = getSettingFlow("COMPARE_MODEL", "~deepseek/deepseek-v4-flash-latest")
    val explainModel = getSettingFlow("EXPLAIN_MODEL", "~deepseek/deepseek-v4-flash-latest")
    val translateModel = getSettingFlow("TRANSLATE_MODEL", "~deepseek/deepseek-v4-flash-latest")
    
    val dictReasoning = getSettingFlow("DICT_REASONING", "default")
    val compareReasoning = getSettingFlow("COMPARE_REASONING", "default")
    val explainReasoning = getSettingFlow("EXPLAIN_REASONING", "default")
    val translateReasoning = getSettingFlow("TRANSLATE_REASONING", "default")
    val fallbackReasoning = getSettingFlow("FALLBACK_REASONING", "default")
    val chatReasoning = getSettingFlow("CHAT_REASONING", "default")
    
    val autoNewSearch = getSettingFlow("AUTO_NEW_SEARCH", "false")
    val enterToSend = getSettingFlow("ENTER_TO_SEND", "false")
    val persistentBackground = getSettingFlow("PERSISTENT_BACKGROUND_SERVICE", "false")
    
    val fallbackModels = getSettingFlow("FALLBACK_MODELS", "google/gemini-3.8-flash")
    val chatModel = getSettingFlow("CHAT_MODEL", "~deepseek/deepseek-v4-flash-latest")

    val dictPrompt = getSettingFlow("DICT_PROMPT", DefaultPrompts.DICT_PROMPT)
    val explainPrompt = getSettingFlow("EXPLAIN_PROMPT", DefaultPrompts.EXPLAIN_PROMPT)
    val starredLanguages = getSettingFlow("STARRED_LANGUAGES", "English, Vietnamese, German, French, Spanish, Japanese, Chinese, Korean, Russian, Italian, Portuguese")
    val allAvailableLanguages = database.appDao().getSettingsFlow().map { s -> com.aidict.app.utils.LanguageManager.getAllAvailable(s.find { it.key == "CUSTOM_LANGUAGES" }?.value) }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, com.aidict.app.utils.LanguageManager.getAllAvailable(null))
    val orderedLanguages = database.appDao().getSettingsFlow().map { s -> com.aidict.app.utils.LanguageManager.getOrderedLanguages(s.find { it.key == "STARRED_LANGUAGES" }?.value, s.find { it.key == "CUSTOM_LANGUAGES" }?.value) }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, com.aidict.app.utils.LanguageManager.getOrderedLanguages(null, null))

    val translatePrompt = getSettingFlow("TRANSLATE_PROMPT", DefaultPrompts.TRANSLATE_PROMPT)
    val comparePrompt = getSettingFlow("COMPARE_PROMPT", DefaultPrompts.COMPARE_PROMPT)
    
    
    val profiles = database.appDao().getProfiles()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    private val _selectedProfileId = MutableStateFlow<Int?>(null)
    val selectedProfileId: StateFlow<Int?> = _selectedProfileId.asStateFlow()

    fun selectProfileScope(profileId: Int?) {
        _selectedProfileId.value = profileId
    }

    val aiConfig: StateFlow<ProfileAiConfig> = combine(
        _selectedProfileId,
        database.appDao().getSettingsFlow(),
        profiles
    ) { selId, settings, profileList ->
        val profileName = if (selId == null) {
            "Global Defaults"
        } else {
            profileList.find { it.id == selId }?.name ?: "Profile #$selId"
        }

        fun resolveItem(key: String, defaultVal: String): ProfileSettingItem {
            val globalVal = settings.find { it.key == key }?.value?.trim()?.ifEmpty { null } ?: defaultVal
            if (selId == null) {
                return ProfileSettingItem(
                    key = key,
                    effectiveValue = globalVal,
                    isCustom = false,
                    globalValue = globalVal,
                    defaultValue = defaultVal
                )
            } else {
                val profileVal = settings.find { it.key == "PROFILE_${selId}_$key" }?.value?.trim()?.ifEmpty { null }
                val isCustom = profileVal != null
                return ProfileSettingItem(
                    key = key,
                    effectiveValue = profileVal ?: globalVal,
                    isCustom = isCustom,
                    globalValue = globalVal,
                    defaultValue = defaultVal
                )
            }
        }

        val dModel = resolveItem("DICT_MODEL", "~deepseek/deepseek-v4-flash-latest")
        val cModel = resolveItem("COMPARE_MODEL", "~deepseek/deepseek-v4-flash-latest")
        val eModel = resolveItem("EXPLAIN_MODEL", "~deepseek/deepseek-v4-flash-latest")
        val tModel = resolveItem("TRANSLATE_MODEL", "~deepseek/deepseek-v4-flash-latest")
        val fModel = resolveItem("FALLBACK_MODELS", "google/gemini-3.8-flash")
        val chModel = resolveItem("CHAT_MODEL", "~deepseek/deepseek-v4-flash-latest")

        val dReasoning = resolveItem("DICT_REASONING", "default")
        val cReasoning = resolveItem("COMPARE_REASONING", "default")
        val eReasoning = resolveItem("EXPLAIN_REASONING", "default")
        val tReasoning = resolveItem("TRANSLATE_REASONING", "default")
        val fReasoning = resolveItem("FALLBACK_REASONING", "default")
        val chReasoning = resolveItem("CHAT_REASONING", "default")

        val dPrompt = resolveItem("DICT_PROMPT", DefaultPrompts.DICT_PROMPT)
        val cPrompt = resolveItem("COMPARE_PROMPT", DefaultPrompts.COMPARE_PROMPT)
        val ePrompt = resolveItem("EXPLAIN_PROMPT", DefaultPrompts.EXPLAIN_PROMPT)
        val tPrompt = resolveItem("TRANSLATE_PROMPT", DefaultPrompts.TRANSLATE_PROMPT)

        val hasAnyCustom = selId != null && (
            dModel.isCustom || cModel.isCustom || eModel.isCustom || tModel.isCustom ||
            fModel.isCustom || chModel.isCustom ||
            dReasoning.isCustom || cReasoning.isCustom || eReasoning.isCustom ||
            tReasoning.isCustom || fReasoning.isCustom || chReasoning.isCustom ||
            dPrompt.isCustom || cPrompt.isCustom || ePrompt.isCustom || tPrompt.isCustom
        )

        ProfileAiConfig(
            selectedProfileId = selId,
            selectedProfileName = profileName,
            dictModel = dModel,
            compareModel = cModel,
            explainModel = eModel,
            translateModel = tModel,
            fallbackModels = fModel,
            chatModel = chModel,
            dictReasoning = dReasoning,
            compareReasoning = cReasoning,
            explainReasoning = eReasoning,
            translateReasoning = tReasoning,
            fallbackReasoning = fReasoning,
            chatReasoning = chReasoning,
            dictPrompt = dPrompt,
            comparePrompt = cPrompt,
            explainPrompt = ePrompt,
            translatePrompt = tPrompt,
            hasCustomOverrides = hasAnyCustom
        )
    }.stateIn(
        viewModelScope,
        SharingStarted.Lazily,
        ProfileAiConfig(
            selectedProfileId = null,
            selectedProfileName = "Global Defaults",
            dictModel = ProfileSettingItem("DICT_MODEL", "~deepseek/deepseek-v4-flash-latest", false, "~deepseek/deepseek-v4-flash-latest", "~deepseek/deepseek-v4-flash-latest"),
            compareModel = ProfileSettingItem("COMPARE_MODEL", "~deepseek/deepseek-v4-flash-latest", false, "~deepseek/deepseek-v4-flash-latest", "~deepseek/deepseek-v4-flash-latest"),
            explainModel = ProfileSettingItem("EXPLAIN_MODEL", "~deepseek/deepseek-v4-flash-latest", false, "~deepseek/deepseek-v4-flash-latest", "~deepseek/deepseek-v4-flash-latest"),
            translateModel = ProfileSettingItem("TRANSLATE_MODEL", "~deepseek/deepseek-v4-flash-latest", false, "~deepseek/deepseek-v4-flash-latest", "~deepseek/deepseek-v4-flash-latest"),
            fallbackModels = ProfileSettingItem("FALLBACK_MODELS", "google/gemini-3.8-flash", false, "google/gemini-3.8-flash", "google/gemini-3.8-flash"),
            chatModel = ProfileSettingItem("CHAT_MODEL", "~deepseek/deepseek-v4-flash-latest", false, "~deepseek/deepseek-v4-flash-latest", "~deepseek/deepseek-v4-flash-latest"),
            dictReasoning = ProfileSettingItem("DICT_REASONING", "default", false, "default", "default"),
            compareReasoning = ProfileSettingItem("COMPARE_REASONING", "default", false, "default", "default"),
            explainReasoning = ProfileSettingItem("EXPLAIN_REASONING", "default", false, "default", "default"),
            translateReasoning = ProfileSettingItem("TRANSLATE_REASONING", "default", false, "default", "default"),
            fallbackReasoning = ProfileSettingItem("FALLBACK_REASONING", "default", false, "default", "default"),
            chatReasoning = ProfileSettingItem("CHAT_REASONING", "default", false, "default", "default"),
            dictPrompt = ProfileSettingItem("DICT_PROMPT", DefaultPrompts.DICT_PROMPT, false, DefaultPrompts.DICT_PROMPT, DefaultPrompts.DICT_PROMPT),
            comparePrompt = ProfileSettingItem("COMPARE_PROMPT", DefaultPrompts.COMPARE_PROMPT, false, DefaultPrompts.COMPARE_PROMPT, DefaultPrompts.COMPARE_PROMPT),
            explainPrompt = ProfileSettingItem("EXPLAIN_PROMPT", DefaultPrompts.EXPLAIN_PROMPT, false, DefaultPrompts.EXPLAIN_PROMPT, DefaultPrompts.EXPLAIN_PROMPT),
            translatePrompt = ProfileSettingItem("TRANSLATE_PROMPT", DefaultPrompts.TRANSLATE_PROMPT, false, DefaultPrompts.TRANSLATE_PROMPT, DefaultPrompts.TRANSLATE_PROMPT),
            hasCustomOverrides = false
        )
    )

    fun saveAiSetting(key: String, value: String) {
        val selId = _selectedProfileId.value
        viewModelScope.launch {
            if (selId == null) {
                database.appDao().insertSetting(AppSetting(key, value))
            } else {
                database.appDao().insertSetting(AppSetting("PROFILE_${selId}_$key", value))
            }
        }
    }

    fun resetAiSetting(key: String) {
        val selId = _selectedProfileId.value
        viewModelScope.launch {
            if (selId != null) {
                database.appDao().deleteSetting("PROFILE_${selId}_$key")
            } else {
                database.appDao().deleteSetting(key)
            }
        }
    }

    fun resetCurrentProfileToDefaults() {
        val selId = _selectedProfileId.value ?: return
        viewModelScope.launch {
            database.appDao().deleteProfileSettings(selId)
        }
    }

    fun copyAiSettings(fromProfileId: Int?, toProfileId: Int) {
        viewModelScope.launch {
            val keys = listOf(
                "DICT_MODEL", "COMPARE_MODEL", "EXPLAIN_MODEL", "TRANSLATE_MODEL",
                "FALLBACK_MODELS", "CHAT_MODEL",
                "DICT_REASONING", "COMPARE_REASONING", "EXPLAIN_REASONING", "TRANSLATE_REASONING",
                "FALLBACK_REASONING", "CHAT_REASONING",
                "DICT_PROMPT", "COMPARE_PROMPT", "EXPLAIN_PROMPT", "TRANSLATE_PROMPT"
            )
            for (k in keys) {
                val value = if (fromProfileId == null) {
                    database.appDao().getSetting(k)?.value
                } else {
                    database.appDao().getSetting("PROFILE_${fromProfileId}_$k")?.value
                        ?: database.appDao().getSetting(k)?.value
                }
                if (value != null) {
                    database.appDao().insertSetting(AppSetting("PROFILE_${toProfileId}_$k", value))
                }
            }
        }
    }

    private val _availableModels = MutableStateFlow<List<String>>(emptyList())
    val availableModels: StateFlow<List<String>> = _availableModels

    init {
        viewModelScope.launch {
            try {
                val oldModel = "inclusionai/ling-3.0-flash"
                val newDefaultModel = "~deepseek/deepseek-v4-flash-latest"
                val newFallbackModel = "google/gemini-3.8-flash"
                val allSettings = database.appDao().getAllSettings()
                for (setting in allSettings) {
                    if (setting.value == oldModel) {
                        database.appDao().insertSetting(setting.copy(value = newDefaultModel))
                    } else if (setting.key.endsWith("FALLBACK_MODELS") && (setting.value == oldModel || setting.value == newDefaultModel)) {
                        database.appDao().insertSetting(setting.copy(value = newFallbackModel))
                    }
                }
            } catch (ignored: Exception) {}

            _availableModels.value = llmRepository.fetchModels()
        }
    }

    fun getSettingFlow(key: String, default: String): StateFlow<String> {
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
            val maxRank = profiles.value.maxOfOrNull { it.rank } ?: -1
            database.appDao().insertProfile(Profile(name = name, rank = maxRank + 1, isDefault = false))
        }
    }

    fun renameProfile(profile: Profile, newName: String) {
        viewModelScope.launch {
            database.appDao().insertProfile(profile.copy(name = newName))
        }
    }

    fun deleteProfile(profile: Profile) {
        viewModelScope.launch {
            database.appDao().deleteProfileSettings(profile.id)
            database.appDao().deleteProfile(profile)
            if (_selectedProfileId.value == profile.id) {
                _selectedProfileId.value = null
            }
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

    private suspend fun normalizeRanks(allProfiles: List<com.aidict.app.data.entities.Profile>): List<com.aidict.app.data.entities.Profile> {
        var needsUpdate = false
        val updated = allProfiles.mapIndexed { index, p -> 
            if (p.rank != index) needsUpdate = true
            p.copy(rank = index) 
        }
        if (needsUpdate) {
            updated.forEach { database.appDao().insertProfile(it) }
        }
        return updated
    }

    fun moveProfileUp(profile: com.aidict.app.data.entities.Profile) {
        viewModelScope.launch {
            val allProfiles = normalizeRanks(profiles.value.sortedBy { it.rank })
            val index = allProfiles.indexOfFirst { it.id == profile.id }
            if (index > 0) {
                val above = allProfiles[index - 1]
                val pToUpdate = allProfiles[index]
                
                val currentRank = pToUpdate.rank
                database.appDao().insertProfile(pToUpdate.copy(rank = above.rank))
                database.appDao().insertProfile(above.copy(rank = currentRank))
            }
        }
    }

    fun moveProfileDown(profile: com.aidict.app.data.entities.Profile) {
        viewModelScope.launch {
            val allProfiles = normalizeRanks(profiles.value.sortedBy { it.rank })
            val index = allProfiles.indexOfFirst { it.id == profile.id }
            if (index < allProfiles.size - 1) {
                val below = allProfiles[index + 1]
                val pToUpdate = allProfiles[index]
                
                val currentRank = pToUpdate.rank
                database.appDao().insertProfile(pToUpdate.copy(rank = below.rank))
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
    val shuffleEnabledQuotes = database.appDao().getSettingsFlow().map { settings ->
        val jsonStr = settings.find { it.key == "SHUFFLE_ENABLED_QUOTES" }?.value
        if (!jsonStr.isNullOrBlank()) {
            try { kotlinx.serialization.json.Json.decodeFromString<List<String>>(jsonStr) } catch(e: Exception) { null }
        } else null
    }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, null)


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
