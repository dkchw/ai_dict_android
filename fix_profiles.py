import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/AppViewModel.kt', 'r') as f:
    content = f.read()

replacement = """
    init {
        viewModelScope.launch {
            database.appDao().getProfiles().collectLatest { profileList ->
                var list = profileList
                if (list.isEmpty()) {
                    val defaultProfile = Profile(name = "Default", isDefault = true, rank = 0)
                    val id = database.appDao().insertProfile(defaultProfile).toInt()
                    list = listOf(defaultProfile.copy(id = id))
                }
                
                val active = _uiState.value.activeProfile ?: list.firstOrNull { it.isDefault } ?: list.firstOrNull()
                _uiState.value = _uiState.value.copy(
                    profiles = list,
                    activeProfile = active
                )
            }
        }
    }
"""

pattern = r'    init \{\n        viewModelScope\.launch \{\n            database\.appDao\(\)\.getProfiles\(\)\.collectLatest \{ profileList ->\n                val active = _uiState\.value\.activeProfile \?: profileList\.firstOrNull \{ it\.isDefault \} \?: profileList\.firstOrNull\(\)\n                _uiState\.value = _uiState\.value\.copy\(\n                    profiles = profileList,\n                    activeProfile = active\n                \)\n            \}\n        \}\n    \}'
content = re.sub(pattern, replacement.strip('\n'), content)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/AppViewModel.kt', 'w') as f:
    f.write(content)
