import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'r') as f:
    text = f.read()

old_create = """    fun createProfile(name: String) {
        viewModelScope.launch {
            database.appDao().insertProfile(Profile(name = name, rank = 0, isDefault = false))
        }
    }"""

new_create = """    fun createProfile(name: String) {
        viewModelScope.launch {
            val maxRank = profiles.value.maxOfOrNull { it.rank } ?: -1
            database.appDao().insertProfile(Profile(name = name, rank = maxRank + 1, isDefault = false))
        }
    }"""

old_move = """    fun moveProfileUp(profile: Profile) {
        viewModelScope.launch {
            val allProfiles = profiles.value.sortedBy { it.rank }.toMutableList()
            val index = allProfiles.indexOfFirst { it.id == profile.id }
            if (index > 0) {
                val above = allProfiles[index - 1]
                val currentRank = profile.rank
                database.appDao().insertProfile(profile.copy(rank = above.rank))
                database.appDao().insertProfile(above.copy(rank = currentRank))
            }
        }
    }

    fun moveProfileDown(profile: Profile) {
        viewModelScope.launch {
            val allProfiles = profiles.value.sortedBy { it.rank }.toMutableList()
            val index = allProfiles.indexOfFirst { it.id == profile.id }
            if (index < allProfiles.size - 1) {
                val below = allProfiles[index + 1]
                val currentRank = profile.rank
                database.appDao().insertProfile(profile.copy(rank = below.rank))
                database.appDao().insertProfile(below.copy(rank = currentRank))
            }
        }
    }"""

new_move = """    private suspend fun normalizeRanks(allProfiles: List<com.aidict.app.data.entities.Profile>): List<com.aidict.app.data.entities.Profile> {
        var needsUpdate = false
        val updated = allProfiles.mapIndexed { index, p -> 
            if (p.rank != index) needsUpdate = true
            p.copy(rank = index) 
        }
        if (needsUpdate) {
            updated.forEach { database.appDao().insertProfile(it) }
        }
        return updated
    }

    fun moveProfileUp(profile: com.aidict.app.data.entities.Profile) {
        viewModelScope.launch {
            val allProfiles = normalizeRanks(profiles.value.sortedBy { it.rank })
            val index = allProfiles.indexOfFirst { it.id == profile.id }
            if (index > 0) {
                val above = allProfiles[index - 1]
                val pToUpdate = allProfiles[index]
                
                val currentRank = pToUpdate.rank
                database.appDao().insertProfile(pToUpdate.copy(rank = above.rank))
                database.appDao().insertProfile(above.copy(rank = currentRank))
            }
        }
    }

    fun moveProfileDown(profile: com.aidict.app.data.entities.Profile) {
        viewModelScope.launch {
            val allProfiles = normalizeRanks(profiles.value.sortedBy { it.rank })
            val index = allProfiles.indexOfFirst { it.id == profile.id }
            if (index < allProfiles.size - 1) {
                val below = allProfiles[index + 1]
                val pToUpdate = allProfiles[index]
                
                val currentRank = pToUpdate.rank
                database.appDao().insertProfile(pToUpdate.copy(rank = below.rank))
                database.appDao().insertProfile(below.copy(rank = currentRank))
            }
        }
    }"""

text = text.replace(old_create, new_create)
text = text.replace(old_move, new_move)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'w') as f:
    f.write(text)

