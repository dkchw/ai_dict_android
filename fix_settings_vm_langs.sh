sed -i 's/val orderedLanguages = starredLanguages.map.*/val orderedLanguages = database.appDao().getSettingsFlow().map { s -> com.aidict.app.utils.LanguageManager.getOrderedLanguages(s.find { it.key == "STARRED_LANGUAGES" }?.value, s.find { it.key == "CUSTOM_LANGUAGES" }?.value) }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, com.aidict.app.utils.LanguageManager.getOrderedLanguages(null, null))/g' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt

cat << 'INNER' >> android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt

    fun addCustomLanguage(name: String, flagIso: String) {
        viewModelScope.launch {
            val current = database.appDao().getSetting("CUSTOM_LANGUAGES")?.value ?: ""
            val newEntry = "${name.trim()}|${flagIso.trim()}"
            val newCustom = if (current.isBlank()) newEntry else "$current,$newEntry"
            database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("CUSTOM_LANGUAGES", newCustom))
        }
    }
}
INNER

# Fix missing brace
sed -i '$d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
