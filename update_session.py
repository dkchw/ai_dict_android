import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()

old_create = """    fun createSession(name: String) {
        viewModelScope.launch {
            val session = Session(name = name, profileId = activeProfileId.value.toLong())
            database.appDao().insertSession(session)
        }
    }"""
new_create = """    fun createSession(name: String) {
        viewModelScope.launch {
            val finalName = if (name.isBlank()) {
                java.text.SimpleDateFormat("MMM dd, yyyy HH:mm", java.util.Locale.getDefault()).format(java.util.Date())
            } else name
            val session = com.aidict.app.data.entities.Session(name = finalName, profileId = activeProfileId.value.toLong())
            database.appDao().insertSession(session)
        }
    }"""
text = text.replace(old_create, new_create)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)

