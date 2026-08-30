# Fix SearchViewModel
sed -i 's/fun searchWord(term: String, sourceLang: String, targetLang: String)/fun searchWord(term: String, sourceLang: String, targetLang: String, profileId: Int)/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt
sed -i 's/profileId = 1/profileId = profileId/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt

# Fix TranslateViewModel
sed -i 's/fun translateText(text: String, source: String, target: String)/fun translateText(text: String, source: String, target: String, profileId: Int)/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/TranslateViewModel.kt
sed -i 's/profileId = 1/profileId = profileId/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/TranslateViewModel.kt

# Fix ExplainViewModel
sed -i 's/fun explainText(text: String)/fun explainText(text: String, profileId: Int)/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/ExplainViewModel.kt
sed -i 's/profileId = 1/profileId = profileId/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/ExplainViewModel.kt

# Fix CompareViewModel
sed -i 's/fun compareWords(words: String)/fun compareWords(words: String, profileId: Int)/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/CompareViewModel.kt
sed -i 's/profileId = 1/profileId = profileId/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/CompareViewModel.kt
