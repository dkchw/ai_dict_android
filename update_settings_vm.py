import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'r') as f:
    text = f.read()

# Add shuffleEnabledQuotes
all_quotes_block = """    val allQuotes = customQuotes.map { custom ->
        val defaults = listOf("Per studium ad sapientiam", "Labor omnia vincit", "Assiduitas mater scientiae", "Nulla dies sine linea", "Carpe diem", "Vincit qui se vincit")
        val customs = custom.split("|").filter { it.isNotBlank() }
        defaults + customs
    }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, listOf("Per studium ad sapientiam", "Labor omnia vincit", "Assiduitas mater scientiae", "Nulla dies sine linea", "Carpe diem", "Vincit qui se vincit"))"""

shuffle_enabled_quotes = """
    val shuffleEnabledQuotes = database.appDao().getSettingsFlow().map { settings ->
        val jsonStr = settings.find { it.key == "SHUFFLE_ENABLED_QUOTES" }?.value
        if (!jsonStr.isNullOrBlank()) {
            try { kotlinx.serialization.json.Json.decodeFromString<List<String>>(jsonStr) } catch(e: Exception) { null }
        } else null
    }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, null)
"""

text = text.replace(all_quotes_block, all_quotes_block + shuffle_enabled_quotes)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'w') as f:
    f.write(text)

