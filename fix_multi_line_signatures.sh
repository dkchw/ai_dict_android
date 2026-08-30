sed -i 's/viewModel: SearchViewModel,/viewModel: SearchViewModel, profileId: Int,/' android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt
sed -i 's/viewModel: TranslateViewModel,/viewModel: TranslateViewModel, profileId: Int,/' android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt
sed -i 's/viewModel: ExplainViewModel,/viewModel: ExplainViewModel, profileId: Int,/' android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt
sed -i 's/viewModel: CompareViewModel,/viewModel: CompareViewModel, profileId: Int,/' android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt
