import re
with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()

text = text.replace('fun setActiveProfileId(id: Int) { activeProfileId.value = id     \n    val splitFraction', 'fun setActiveProfileId(id: Int) { activeProfileId.value = id }\n/*')
text = text.replace('    fun updateSplitFraction(fraction: Float) {\n        splitFraction.value = fraction\n        viewModelScope.launch {\n            database.appDao().insertSetting(com.aidict.app.data.entities.AppSetting("HISTORY_SPLIT_FRACTION", fraction.toString()))\n        }\n    }\n}\n', '*/\n')

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)
