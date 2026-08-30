# SearchScreen
sed -i 's/fun SearchScreen(viewModel: SearchViewModel/fun SearchScreen(viewModel: SearchViewModel, profileId: Int/' android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt
sed -i 's/viewModel.searchWord(inputTerm, sourceLang, targetLang)/viewModel.searchWord(inputTerm, sourceLang, targetLang, profileId)/' android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt

# TranslateScreen
sed -i 's/fun TranslateScreen(viewModel: TranslateViewModel/fun TranslateScreen(viewModel: TranslateViewModel, profileId: Int/' android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt
sed -i 's/viewModel.translateText(sourceText, sourceLang, targetLang)/viewModel.translateText(sourceText, sourceLang, targetLang, profileId)/' android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt

# ExplainScreen
sed -i 's/fun ExplainScreen(viewModel: ExplainViewModel/fun ExplainScreen(viewModel: ExplainViewModel, profileId: Int/' android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt
sed -i 's/viewModel.explainText(sourceText)/viewModel.explainText(sourceText, profileId)/' android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt

# CompareScreen
sed -i 's/fun CompareScreen(viewModel: CompareViewModel/fun CompareScreen(viewModel: CompareViewModel, profileId: Int/' android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt
sed -i 's/viewModel.compareWords(sourceText)/viewModel.compareWords(sourceText, profileId)/' android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt

