sed -i 's/fun ChatInputBar(/fun ChatInputBar(\n    availableLanguages: List<String> = com.aidict.app.utils.LanguageManager.allLanguages,\n/' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt
sed -i 's/SmallLanguageSelector(currentValue = sourceLang/SmallLanguageSelector(availableLanguages = availableLanguages, currentValue = sourceLang/' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt
sed -i 's/SmallLanguageSelector(currentValue = targetLang/SmallLanguageSelector(availableLanguages = availableLanguages, currentValue = targetLang/' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt

sed -i 's/ChatInputBar(/ChatInputBar(availableLanguages = viewModel.orderedLanguages.collectAsState().value, /' android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt
sed -i 's/ChatInputBar(/ChatInputBar(availableLanguages = viewModel.orderedLanguages.collectAsState().value, /' android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt
