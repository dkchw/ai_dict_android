import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Add getExternalLink method
method_code = """
    fun getExternalLinkTemplate(): String {
        return kotlinx.coroutines.runBlocking(kotlinx.coroutines.Dispatchers.IO) {
            database.appDao().getSetting("EXTERNAL_LINK")?.value ?: "https://dictionary.cambridge.org/dictionary/english/{word}"
        }
    }
"""
text = text.replace('fun getProfileSetting(profileId: Int, key: String): String? {', method_code + '\n    fun getProfileSetting(profileId: Int, key: String): String? {')

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

