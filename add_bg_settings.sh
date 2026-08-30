cat << 'INNER_EOF' >> android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt

    private val _bgDict = MutableStateFlow<String?>(null)
    val bgDict: StateFlow<String?> = _bgDict.asStateFlow()
    
    private val _bgCompare = MutableStateFlow<String?>(null)
    val bgCompare: StateFlow<String?> = _bgCompare.asStateFlow()
    
    private val _bgTranslate = MutableStateFlow<String?>(null)
    val bgTranslate: StateFlow<String?> = _bgTranslate.asStateFlow()
    
    private val _bgExplain = MutableStateFlow<String?>(null)
    val bgExplain: StateFlow<String?> = _bgExplain.asStateFlow()
    
    private val _bgBlurRadius = MutableStateFlow(10f)
    val bgBlurRadius: StateFlow<Float> = _bgBlurRadius.asStateFlow()
INNER_EOF

# Add loading block for bg properties
sed -i '/_appTheme.value = database.appDao().getSetting("APP_THEME")?.value ?: "tokyonight"/a \            _bgDict.value = database.appDao().getSetting("BG_DICT")?.value\n            _bgCompare.value = database.appDao().getSetting("BG_COMPARE")?.value\n            _bgTranslate.value = database.appDao().getSetting("BG_TRANSLATE")?.value\n            _bgExplain.value = database.appDao().getSetting("BG_EXPLAIN")?.value\n            _bgBlurRadius.value = database.appDao().getSetting("BG_BLUR_RADIUS")?.value?.toFloatOrNull() ?: 10f' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt

