import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

imports = """import kotlinx.serialization.json.Json
import kotlinx.serialization.decodeFromString
import com.aidict.app.models.ExternalLink
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.SharingStarted
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
"""

# replace getExternalLinkTemplate
text = re.sub(r'    fun getExternalLinkTemplate\(\): String \{.*?\}\n', flow_code, text, flags=re.DOTALL)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

