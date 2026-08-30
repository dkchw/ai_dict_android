sed -i 's/private val allHistory = currentMode.flatMapLatest { mode ->/private val activeProfileId = kotlinx.coroutines.flow.MutableStateFlow(1)\n    fun setActiveProfileId(id: Int) { activeProfileId.value = id }\n\n    @OptIn(ExperimentalCoroutinesApi::class)\n    private val allHistory = kotlinx.coroutines.flow.combine(currentMode, activeProfileId) { m, p -> Pair(m, p) }.flatMapLatest { (mode, pid) ->/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt

sed -i 's/database.appDao().getWordsByMode(1, mode)/database.appDao().getWordsByMode(pid, mode)/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt

sed -i 's/val sessions = database.appDao().getSessions(1)/val sessions = activeProfileId.flatMapLatest { pid -> database.appDao().getSessions(pid.toLong()) }/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt

sed -i 's/profileId = 1/profileId = activeProfileId.value.toLong()/' android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt

