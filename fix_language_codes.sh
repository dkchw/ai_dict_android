cat << 'INNER' >> android_app/app/src/main/java/com/aidict/app/utils/LanguageManager.kt

    private val FLAG_MAP = mapOf(
        "Auto Detect" to "🤖 Auto",
        "English" to "🇬🇧 EN",
        "Vietnamese" to "🇻🇳 VI",
        "French" to "🇫🇷 FR",
        "Spanish" to "🇪🇸 ES",
        "German" to "🇩🇪 DE",
        "Japanese" to "🇯🇵 JA",
        "Chinese" to "🇨🇳 ZH",
        "Korean" to "🇰🇷 KO",
        "Russian" to "🇷🇺 RU",
        "Italian" to "🇮🇹 IT",
        "Portuguese" to "🇵🇹 PT",
        "Dutch" to "🇳🇱 NL",
        "Arabic" to "🇸🇦 AR"
    )

    fun getDisplayFlag(language: String): String {
        FLAG_MAP[language]?.let { return it }
        val iso = Locale.getISOLanguages().find { Locale(it).getDisplayLanguage(Locale.ENGLISH) == language }
        return iso?.uppercase() ?: language.take(4).uppercase()
    }
INNER
sed -i 's/LANGUAGE_CODES\[currentValue\] ?: currentValue.take(4)/com.aidict.app.utils.LanguageManager.getDisplayFlag(currentValue)/' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt
sed -i 's/LANGUAGE_CODES\[lang\] ?: ""/com.aidict.app.utils.LanguageManager.getDisplayFlag(lang)/' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt
