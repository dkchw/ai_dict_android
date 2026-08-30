sed -i '/var defaultSourceLang/d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/TranslateViewModel.kt
sed -i '/var defaultTargetLang/d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/TranslateViewModel.kt
sed -i '/init {/,+5d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/TranslateViewModel.kt

# Remove closing brace
sed -i '$d' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/TranslateViewModel.kt

cat << 'INNER' >> android_app/app/src/main/java/com/aidict/app/ui/viewmodels/TranslateViewModel.kt

    suspend fun getProfileSetting(profileId: Int, key: String): String? {
        return kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
            database.appDao().getSetting("PROFILE_${profileId}_$key")?.value
        }
    }

    fun saveProfileSetting(profileId: Int, key: String, value: String) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("PROFILE_${profileId}_$key", value))
        }
    }
}
INNER
