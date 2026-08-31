import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()

viewmodel_addition = """
    private val selectedWordId = MutableStateFlow<Int?>(null)
    @OptIn(ExperimentalCoroutinesApi::class)
    val selectedChatMessages = selectedWordId.flatMapLatest { wordId ->
        if (wordId == null) kotlinx.coroutines.flow.flowOf(emptyList())
        else database.appDao().getChatMessages(wordId)
    }.stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    fun setSelectedWordId(wordId: Int?) {
        selectedWordId.value = wordId
    }
}"""

text = re.sub(r'\}\s*$', viewmodel_addition, text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)
