import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'r') as f:
    text = f.read()

imports = """import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString
import kotlinx.serialization.decodeFromString
import com.aidict.app.models.ExternalLink
"""
text = text.replace('import com.aidict.app.data.AppDatabase', imports + 'import com.aidict.app.data.AppDatabase')

flow_code = """    private val defaultLinks = listOf(
        ExternalLink("Cambridge", "https://dictionary.cambridge.org/dictionary/english/{word}", "https://dictionary.cambridge.org/favicon.ico"),
        ExternalLink("Google", "https://www.google.com/search?q={word}", "https://www.google.com/favicon.ico"),
        ExternalLink("Wikipedia", "https://en.wikipedia.org/wiki/{word}", "https://en.wikipedia.org/favicon.ico")
    )
    val externalLinks: StateFlow<List<ExternalLink>> = database.appDao().getSettingsFlow()
        .map { settings ->
            val jsonStr = settings.find { it.key == "EXTERNAL_LINKS" }?.value
            if (jsonStr != null) {
                try { Json.decodeFromString<List<ExternalLink>>(jsonStr) } catch (e: Exception) { defaultLinks }
            } else defaultLinks
        }.stateIn(viewModelScope, SharingStarted.Lazily, defaultLinks)

    fun saveExternalLinks(links: List<ExternalLink>) {
        val jsonStr = Json.encodeToString(links)
        saveSetting("EXTERNAL_LINKS", jsonStr)
    }
"""

text = re.sub(r'    val externalLinkTemplate.*?\}\n', '', text, flags=re.DOTALL) # remove old string template if there
text = text.replace('val comparePrompt = getSettingFlow("COMPARE_PROMPT", DefaultPrompts.COMPARE_PROMPT)', 'val comparePrompt = getSettingFlow("COMPARE_PROMPT", DefaultPrompts.COMPARE_PROMPT)\n' + flow_code)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'w') as f:
    f.write(text)

