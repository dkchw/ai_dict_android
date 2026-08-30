# Delete MutableStateFlow properties at end of file
sed -i '141,$d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt

# Append new flow mappings to the end of the file, inside the class
cat << 'INNER' >> android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt

    val bgDict = getSettingFlow("BG_DICT", "").map { it.ifBlank { null } }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val bgCompare = getSettingFlow("BG_COMPARE", "").map { it.ifBlank { null } }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val bgTranslate = getSettingFlow("BG_TRANSLATE", "").map { it.ifBlank { null } }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    val bgExplain = getSettingFlow("BG_EXPLAIN", "").map { it.ifBlank { null } }.stateIn(viewModelScope, SharingStarted.Lazily, null)
    
    val bgBlurRadius = getSettingFlow("BG_BLUR_RADIUS", "10.0").map { it.toFloatOrNull() ?: 10f }.stateIn(viewModelScope, SharingStarted.Lazily, 10f)
    val bgOpacity = getSettingFlow("BG_OPACITY", "1.0").map { it.toFloatOrNull() ?: 1f }.stateIn(viewModelScope, SharingStarted.Lazily, 1f)
    
    val quoteMode = getSettingFlow("QUOTE_MODE", "None")
}
INNER

# Delete the initialization logic from init block
sed -i '/_bgDict.value =/d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
sed -i '/_bgCompare.value =/d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
sed -i '/_bgTranslate.value =/d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
sed -i '/_bgExplain.value =/d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
sed -i '/_bgBlurRadius.value =/d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
sed -i '/_bgOpacity.value =/d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
sed -i '/_quoteMode.value =/d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
