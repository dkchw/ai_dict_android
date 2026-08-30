import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()

viewmodel_addition = """    val splitFraction = kotlinx.coroutines.flow.MutableStateFlow(0.5f)
    init {
        viewModelScope.launch {
            val saved = database.appDao().getSetting("HISTORY_SPLIT_FRACTION")?.value?.toFloatOrNull()
            if (saved != null) {
                splitFraction.value = saved
            }
        }
    }
    
    fun updateSplitFraction(fraction: Float) {
        splitFraction.value = fraction
        viewModelScope.launch {
            database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("HISTORY_SPLIT_FRACTION", fraction.toString()))
        }
    }
}"""
text = re.sub(r'\}\s*$', viewmodel_addition, text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)
