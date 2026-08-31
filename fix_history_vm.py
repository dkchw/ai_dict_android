import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()

# Add activeSessionId
import_line = "import kotlinx.coroutines.flow.flatMapLatest"
new_import = "import kotlinx.coroutines.flow.flatMapLatest\nimport com.aidict.app.data.entities.AppSetting"
text = text.replace(import_line, new_import)

session_val = """    val sessions = activeProfileId.flatMapLatest { pid -> database.appDao().getSessions(pid.toLong()) }"""
new_session_val = """    val sessions = activeProfileId.flatMapLatest { pid -> database.appDao().getSessions(pid.toLong()) }
    
    val activeSessionId = database.appDao().getSettingsFlow().map { settings ->
        settings.find { it.key == "ACTIVE_SESSION_ID" }?.value
    }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.Lazily, null)

    fun setActiveSession(id: String?) {
        viewModelScope.launch {
            if (id == null) {
                val s = database.appDao().getSetting("ACTIVE_SESSION_ID")
                if (s != null) database.appDao().deleteSetting(s)
            } else {
                database.appDao().insertSetting(AppSetting("ACTIVE_SESSION_ID", id))
            }
        }
    }"""
text = text.replace(session_val, new_session_val)

# Also make createSession return the id or just set it as active
create_session = """    fun createSession(name: String) {
        viewModelScope.launch {
            database.appDao().insertSession(Session(name = name, profileId = activeProfileId.value.toLong()))
        }
    }"""
new_create_session = """    fun createSession(name: String) {
        viewModelScope.launch {
            val s = Session(name = name, profileId = activeProfileId.value.toLong())
            database.appDao().insertSession(s)
            setActiveSession(s.id)
        }
    }"""
text = text.replace(create_session, new_create_session)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)

