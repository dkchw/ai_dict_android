import os

screens = [
    ('SearchScreen', 'SearchScreen(\n    viewModel: SearchViewModel, profileId: Int,\n    modifier: Modifier = Modifier\n)'),
    ('CompareScreen', 'CompareScreen(\n    viewModel: SearchViewModel, profileId: Int,\n    modifier: Modifier = Modifier\n)'),
    ('TranslateScreen', 'TranslateScreen(\n    viewModel: SearchViewModel, profileId: Int,\n    modifier: Modifier = Modifier\n)'),
    ('ExplainScreen', 'ExplainScreen(\n    viewModel: SearchViewModel, profileId: Int,\n    modifier: Modifier = Modifier\n)')
]

for screen, sig_old in screens:
    path = f"android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}.kt"
    with open(path, 'r') as f:
        text = f.read()

    # Update Signature
    sig_new = f"{screen}(\n    viewModel: SearchViewModel, profileId: Int,\n    autoNewSearch: Boolean = false,\n    onToggleAutoNewSearch: () -> Unit = {{}},\n    enterToSend: Boolean = false,\n    modifier: Modifier = Modifier\n)"
    text = text.replace(sig_old, sig_new)
    
    # Inject autoNewSearch params into ChatInputBar
    text = text.replace("isLoading = state.isLoading,", "isLoading = state.isLoading,\n            autoNewSearch = autoNewSearch,\n            onToggleAutoNewSearch = onToggleAutoNewSearch,\n            enterToSend = enterToSend,")

    # Update onSend logic
    if screen == 'SearchScreen':
        old_send = """            onSend = {
                if (isFollowUp) {
                    viewModel.sendFollowUpMessage(viewModel.searchInput, "dict")
                } else {
                    viewModel.searchWord(viewModel.searchInput, sourceLang, targetLang, profileId)
                }
                viewModel.searchInput = ""
            },"""
        new_send = """            onSend = {
                if (autoNewSearch && isFollowUp) {
                    viewModel.clearCurrentSearch()
                    viewModel.searchWord(viewModel.searchInput, sourceLang, targetLang, profileId)
                } else if (isFollowUp) {
                    viewModel.sendFollowUpMessage(viewModel.searchInput, "dict")
                } else {
                    viewModel.searchWord(viewModel.searchInput, sourceLang, targetLang, profileId)
                }
                viewModel.searchInput = ""
            },"""
        text = text.replace(old_send, new_send)
    elif screen == 'CompareScreen':
        old_send = 'onSend = { if (state.word != null) viewModel.sendFollowUpMessage(viewModel.compareInput, "compare") else viewModel.streamCompare(viewModel.compareInput, sourceLang, targetLang, profileId); viewModel.compareInput = "" },'
        new_send = 'onSend = { if (autoNewSearch && state.word != null) { viewModel.clearCurrentSearch(); viewModel.streamCompare(viewModel.compareInput, sourceLang, targetLang, profileId) } else if (state.word != null) viewModel.sendFollowUpMessage(viewModel.compareInput, "compare") else viewModel.streamCompare(viewModel.compareInput, sourceLang, targetLang, profileId); viewModel.compareInput = "" },'
        text = text.replace(old_send, new_send)
    elif screen == 'TranslateScreen':
        old_send = 'onSend = { if (state.word != null) viewModel.sendFollowUpMessage(viewModel.translateInput, "translate") else viewModel.streamTranslate(viewModel.translateInput, sourceLang, targetLang, profileId); viewModel.translateInput = "" },'
        new_send = 'onSend = { if (autoNewSearch && state.word != null) { viewModel.clearCurrentSearch(); viewModel.streamTranslate(viewModel.translateInput, sourceLang, targetLang, profileId) } else if (state.word != null) viewModel.sendFollowUpMessage(viewModel.translateInput, "translate") else viewModel.streamTranslate(viewModel.translateInput, sourceLang, targetLang, profileId); viewModel.translateInput = "" },'
        text = text.replace(old_send, new_send)
    elif screen == 'ExplainScreen':
        old_send = 'onSend = { if (state.word != null) viewModel.sendFollowUpMessage(viewModel.explainInput, "explain") else viewModel.streamExplain(viewModel.explainInput, profileId); viewModel.explainInput = "" },'
        new_send = 'onSend = { if (autoNewSearch && state.word != null) { viewModel.clearCurrentSearch(); viewModel.streamExplain(viewModel.explainInput, profileId) } else if (state.word != null) viewModel.sendFollowUpMessage(viewModel.explainInput, "explain") else viewModel.streamExplain(viewModel.explainInput, profileId); viewModel.explainInput = "" },'
        text = text.replace(old_send, new_send)

    with open(path, 'w') as f:
        f.write(text)

