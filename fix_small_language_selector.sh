sed -i 's/fun SmallLanguageSelector(/fun SmallLanguageSelector(\n    availableLanguages: List<String>,\n/' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt
sed -i 's/SUPPORTED_LANGUAGES.forEach { lang ->/availableLanguages.forEach { lang ->/' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt
sed -i '/val SUPPORTED_LANGUAGES = listOf/d' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt
