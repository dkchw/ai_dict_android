sed -i '/val bgBlur by settingsViewModel.bgBlurRadius.collectAsState()/a \        val bgUniversal by settingsViewModel.bgUniversal.collectAsState()' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt

sed -i 's/currentMode == 0 -> bgDict/currentMode == 0 -> bgDict ?: bgUniversal/' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt
sed -i 's/currentMode == 1 -> bgCompare/currentMode == 1 -> bgCompare ?: bgUniversal/' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt
sed -i 's/currentMode == 2 -> bgTranslate/currentMode == 2 -> bgTranslate ?: bgUniversal/' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt
sed -i 's/currentMode == 3 -> bgExplain/currentMode == 3 -> bgExplain ?: bgUniversal/' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt
