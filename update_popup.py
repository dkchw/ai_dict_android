import re

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
    text = f.read()

old_launched = """            LaunchedEffect(Unit) {
                if (textExtra.isNotBlank() && searchViewModel.searchInput.isBlank()) {
                    searchViewModel.searchInput = textExtra
                }
            }"""

new_launched = """            LaunchedEffect(Unit) {
                if (textExtra.isNotBlank() && searchViewModel.searchInput.isBlank()) {
                    searchViewModel.clearCurrentSearch()
                    searchViewModel.searchInput = textExtra
                    
                    kotlinx.coroutines.delay(100) // Brief delay to ensure UI and AppViewModel are ready
                    val profileId = appViewModel.uiState.value.activeProfile?.id ?: 1
                    val sourceLang = searchViewModel.getProfileSetting(profileId, "DICT_SOURCE") ?: "Auto Detect"
                    val targetLang = searchViewModel.getProfileSetting(profileId, "DICT_TARGET") ?: "English"
                    
                    searchViewModel.searchWord(textExtra, sourceLang, targetLang, profileId)
                }
            }"""

text = text.replace(old_launched, new_launched)

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
    f.write(text)

