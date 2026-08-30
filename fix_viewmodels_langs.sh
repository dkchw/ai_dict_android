for file in android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt android_app/app/src/main/java/com/aidict/app/ui/viewmodels/TranslateViewModel.kt android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt; do
    sed -i 's/getOrderedLanguages(s.find { it.key == "STARRED_LANGUAGES" }?.value)/getOrderedLanguages(s.find { it.key == "STARRED_LANGUAGES" }?.value, s.find { it.key == "CUSTOM_LANGUAGES" }?.value)/g' "$file"
done
