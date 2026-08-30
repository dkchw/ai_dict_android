# Remove the bad universalLauncher definition at line 143
sed -i '143,148d' android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt

# Inject it right after bgUniversal definition (line 91)
sed -i '/val bgUniversal by viewModel.bgUniversal.collectAsState()/a \
            val universalLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->\n\
                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_UNIVERSAL", it.toString()) }\n\
            }' android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt

# Remove the duplicated Row
sed -i '101d' android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt
