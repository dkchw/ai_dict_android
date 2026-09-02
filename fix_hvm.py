import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()

target = """    }.flatMapLatest { q ->
        if (q == null) kotlinx.coroutines.flow.flowOf(null)
        else kotlinx.coroutines.flow.flow { emit(database.appDao().getWordIdsMatchingContent(q).toSet()) }
    }.stateIn(viewModelScope, SharingStarted.Lazily, null)"""

replacement = """    }.flatMapLatest { q ->
        if (q == null) kotlinx.coroutines.flow.flowOf<Set<Int>?>(null)
        else kotlinx.coroutines.flow.flow<Set<Int>?> { emit(database.appDao().getWordIdsMatchingContent(q).toSet()) }
    }.stateIn(viewModelScope, SharingStarted.Lazily, null)"""

text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)
print("Fixed HVM")
