sed -i 's/fun streamTranslation(text: String, source: String, target: String)/fun streamTranslation(text: String, source: String, target: String, profileId: Int)/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/TranslateViewModel.kt
sed -i 's/fun streamExplain(text: String)/fun streamExplain(text: String, profileId: Int)/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/ExplainViewModel.kt
sed -i 's/fun streamCompare(words: String)/fun streamCompare(words: String, profileId: Int)/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/CompareViewModel.kt
