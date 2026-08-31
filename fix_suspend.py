import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

text = text.replace('suspend \n    fun getExternalLinkTemplate', 'fun getExternalLinkTemplate')
text = text.replace('fun getProfileSetting(profileId: Int, key: String): String? {', 'suspend fun getProfileSetting(profileId: Int, key: String): String? {')

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)
