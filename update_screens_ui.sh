# SearchScreen
sed -i '/if (!isFollowUp) {/,/        }/d' android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt

sed -i 's/isFollowUp = isFollowUp/isFollowUp = isFollowUp,\n            sourceLang = if (!isFollowUp) sourceLang else null,\n            targetLang = if (!isFollowUp) targetLang else null,\n            onSourceLangChange = if (!isFollowUp) { { sourceLang = it } } else null,\n            onTargetLangChange = if (!isFollowUp) { { targetLang = it } } else null/' android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt

# TranslateScreen
sed -i '/Row(/,/        }/d' android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt

sed -i 's/placeholder = "Text to translate..."/placeholder = "Text to translate...",\n            sourceLang = sourceLang,\n            targetLang = targetLang,\n            onSourceLangChange = { sourceLang = it },\n            onTargetLangChange = { targetLang = it }/' android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt
