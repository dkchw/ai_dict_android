import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/AppViewModel.kt', 'r') as f:
    text = f.read()

init_old = """    init {
        viewModelScope.launch {
            database.appDao().getProfiles().collectLatest { profileList ->
                var list = profileList
                if (list.isEmpty()) {
                    val defaultProfile = Profile(name = "Default", isDefault = true, rank = 0)
                    val id = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) { database.appDao().insertProfile(defaultProfile).toInt() }
                    list = listOf(defaultProfile.copy(id = id))
                }
                
                val active = _uiState.value.activeProfile ?: list.firstOrNull { it.isDefault } ?: list.firstOrNull()
                _uiState.value = _uiState.value.copy(
                    profiles = list,
                    activeProfile = active
                )
            }
        }
    }"""

init_new = """    init {
        viewModelScope.launch {
            val savedProfileId = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
                database.appDao().getSetting("ACTIVE_PROFILE_ID")?.value?.toIntOrNull()
            }
            
            database.appDao().getProfiles().collectLatest { profileList ->
                var list = profileList
                if (list.isEmpty()) {
                    val defaultProfile = Profile(name = "Default", isDefault = true, rank = 0)
                    val id = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) { database.appDao().insertProfile(defaultProfile).toInt() }
                    list = listOf(defaultProfile.copy(id = id))
                }
                
                val active = _uiState.value.activeProfile ?: list.find { it.id == savedProfileId } ?: list.firstOrNull { it.isDefault } ?: list.firstOrNull()
                _uiState.value = _uiState.value.copy(
                    profiles = list,
                    activeProfile = active
                )
            }
        }
    }"""
text = text.replace(init_old, init_new)

set_active_old = """    fun setActiveProfile(profile: Profile) {
        _uiState.value = _uiState.value.copy(activeProfile = profile)
    }"""

set_active_new = """    fun setActiveProfile(profile: Profile) {
        _uiState.value = _uiState.value.copy(activeProfile = profile)
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("ACTIVE_PROFILE_ID", profile.id.toString()))
        }
    }"""
text = text.replace(set_active_old, set_active_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/AppViewModel.kt', 'w') as f:
    f.write(text)

