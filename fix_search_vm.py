import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Add active stream jobs map
active_jobs_decl = """    private var compareJob: kotlinx.coroutines.Job? = null

    private val activeStreamJobs = mutableMapOf<String, kotlinx.coroutines.Job>()"""

text = text.replace('    private var compareJob: kotlinx.coroutines.Job? = null', active_jobs_decl)

# Update clearCurrentSearch
clear_old = """    fun clearCurrentSearch() {
        // we keep drafts but reset state outputs if explicitly requested, but maybe not?
        // Actually, we should probably reset all states? No, only reset when switching if desired.
        // Wait, the prompt says output bleeds. Let's just leave clearCurrentSearch as is but resetting all states.
        _dictState.value = SearchState()
        _compareState.value = SearchState()
        _translateState.value = SearchState()
        _explainState.value = SearchState()
    }"""

clear_new = """    fun clearCurrentSearch() {
        activeStreamJobs.values.forEach { it.cancel() }
        activeStreamJobs.clear()
        
        _dictState.value = SearchState()
        _compareState.value = SearchState()
        _translateState.value = SearchState()
        _explainState.value = SearchState()
    }"""
text = text.replace(clear_old, clear_new)

# Add activeStreamJobs tracking to searchWord
search_word_old = """    fun searchWord(term: String, source: String, target: String, profileId: Int) {
        val _uiState = _dictState
        viewModelScope.launch {"""
search_word_new = """    fun searchWord(term: String, source: String, target: String, profileId: Int) {
        val _uiState = _dictState
        activeStreamJobs["dict"]?.cancel()
        activeStreamJobs["dict"] = viewModelScope.launch {"""
text = text.replace(search_word_old, search_word_new)

# sendFollowUpMessage
send_follow_up_old = """    fun sendFollowUpMessage(content: String, mode: String) {
        val _uiState = getUiState(mode)
        viewModelScope.launch {"""
send_follow_up_new = """    fun sendFollowUpMessage(content: String, mode: String) {
        val _uiState = getUiState(mode)
        activeStreamJobs[mode]?.cancel()
        activeStreamJobs[mode] = viewModelScope.launch {"""
text = text.replace(send_follow_up_old, send_follow_up_new)

# retryMessage
retry_old = """    fun retryMessage(msg: com.aidict.app.data.entities.ChatMessage, forceFallback: Boolean = false, mode: String) {
        val _uiState = getUiState(mode)
        viewModelScope.launch {"""
retry_new = """    fun retryMessage(msg: com.aidict.app.data.entities.ChatMessage, forceFallback: Boolean = false, mode: String) {
        val _uiState = getUiState(mode)
        activeStreamJobs[mode]?.cancel()
        activeStreamJobs[mode] = viewModelScope.launch {"""
text = text.replace(retry_old, retry_new)

# streamTranslation
stream_trans_old = """    fun streamTranslation(text: String, source: String, target: String, profileId: Int) {
        val _uiState = _translateState
        viewModelScope.launch {"""
stream_trans_new = """    fun streamTranslation(text: String, source: String, target: String, profileId: Int) {
        val _uiState = _translateState
        activeStreamJobs["translate"]?.cancel()
        activeStreamJobs["translate"] = viewModelScope.launch {"""
text = text.replace(stream_trans_old, stream_trans_new)

# streamCompare
stream_comp_old = """    fun streamCompare(text: String, source: String, target: String, profileId: Int) {
        val _uiState = _compareState
        viewModelScope.launch {"""
stream_comp_new = """    fun streamCompare(text: String, source: String, target: String, profileId: Int) {
        val _uiState = _compareState
        activeStreamJobs["compare"]?.cancel()
        activeStreamJobs["compare"] = viewModelScope.launch {"""
text = text.replace(stream_comp_old, stream_comp_new)

# streamExplain
stream_exp_old = """    fun streamExplain(text: String, source: String, target: String, profileId: Int) {
        val _uiState = _explainState
        viewModelScope.launch {"""
stream_exp_new = """    fun streamExplain(text: String, source: String, target: String, profileId: Int) {
        val _uiState = _explainState
        activeStreamJobs["explain"]?.cancel()
        activeStreamJobs["explain"] = viewModelScope.launch {"""
text = text.replace(stream_exp_old, stream_exp_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

