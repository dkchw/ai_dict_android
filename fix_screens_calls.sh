sed -i 's/viewModel.streamTranslation(sourceText, sourceLang, targetLang)/viewModel.streamTranslation(sourceText, sourceLang, targetLang, profileId)/' android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt
sed -i 's/viewModel.streamExplain(sourceText)/viewModel.streamExplain(sourceText, profileId)/' android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt
sed -i 's/viewModel.streamCompare(sourceText)/viewModel.streamCompare(sourceText, profileId)/' android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt
