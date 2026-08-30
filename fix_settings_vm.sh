# Remove the bad lines at end
sed -i '127,$d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt

# Re-insert them before the last closing brace
sed -i '/^}$/i \    private val _bgDict = MutableStateFlow<String?>(null)\n    val bgDict: StateFlow<String?> = _bgDict.asStateFlow()\n    \n    private val _bgCompare = MutableStateFlow<String?>(null)\n    val bgCompare: StateFlow<String?> = _bgCompare.asStateFlow()\n    \n    private val _bgTranslate = MutableStateFlow<String?>(null)\n    val bgTranslate: StateFlow<String?> = _bgTranslate.asStateFlow()\n    \n    private val _bgExplain = MutableStateFlow<String?>(null)\n    val bgExplain: StateFlow<String?> = _bgExplain.asStateFlow()\n    \n    private val _bgBlurRadius = MutableStateFlow(10f)\n    val bgBlurRadius: StateFlow<Float> = _bgBlurRadius.asStateFlow()' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt
