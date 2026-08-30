sed -i '/val quoteMode/i \    val quoteStyle = getSettingFlow("QUOTE_STYLE", "Serif")' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt

sed -i '/val bgUniversal =/d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
sed -i '/val quoteStyle =/i \    val bgUniversal = getSettingFlow("BG_UNIVERSAL", "").map { it.ifBlank { null } }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, null)' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
