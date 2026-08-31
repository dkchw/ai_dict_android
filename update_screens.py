import os

screens = [
    'SearchScreen', 'CompareScreen', 'TranslateScreen', 'ExplainScreen'
]

mode_names = {
    'SearchScreen': '"dict"',
    'CompareScreen': '"compare"',
    'TranslateScreen': '"translate"',
    'ExplainScreen': '"explain"'
}

for screen in screens:
    path = f"android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}.kt"
    with open(path, 'r') as f:
        text = f.read()
    
    # Update signature
    sig_old = f"fun {screen}(\n    viewModel: SearchViewModel, profileId: Int,\n    modifier: Modifier = Modifier\n)"
    sig_new = f"fun {screen}(\n    viewModel: SearchViewModel, profileId: Int,\n    autoNewSearch: Boolean = false,\n    onToggleAutoNewSearch: () -> Unit = {{}},\n    enterToSend: Boolean = false,\n    modifier: Modifier = Modifier\n)"
    
    text = text.replace(sig_old, sig_new)
    
    # Update ChatInputBar call parameters
    # Find ChatInputBar
    # It might be: ChatInputBar(
    
    # For onSend lambda, they typically look like:
    # onSend = {
    #    if (state.word != null) {
    #        viewModel.sendFollowUpMessage(...)
    #    } else {
    #        ...
    #    }
    #    viewModel.searchInput = ""
    # }
    # Or in CompareScreen:
    # onSend = {
    #     if (state.word != null) {
    #         viewModel.sendFollowUpMessage(viewModel.searchInput, "compare")
    #     } else {
    #         viewModel.streamSearch(viewModel.searchInput, profileId = profileId, mode = "compare")
    #     }
    #     viewModel.searchInput = ""
    # }
    
    # Let's replace the whole ChatInputBar block carefully using regex.
    # It's easier to just replace `isFollowUp = state.word != null,` with:
    # `isFollowUp = state.word != null,\n            autoNewSearch = autoNewSearch,\n            onToggleAutoNewSearch = onToggleAutoNewSearch,\n            enterToSend = enterToSend,`
    
    text = text.replace("isFollowUp = state.word != null,", 
        "isFollowUp = state.word != null,\n            autoNewSearch = autoNewSearch,\n            onToggleAutoNewSearch = onToggleAutoNewSearch,\n            enterToSend = enterToSend,")
    
    # And replace `onSend = {` block
    # We will do this by looking for `onSend = {` and replacing it with the new logic.
    # Wait, it's safer to just inject `if (autoNewSearch && state.word != null) viewModel.clearCurrentSearch()` right before `if (state.word != null)` inside onSend
    
    text = text.replace(
        "onSend = {\n                            if (state.word != null) {",
        "onSend = {\n                            if (autoNewSearch && state.word != null) viewModel.clearCurrentSearch()\n                            if (state.word != null) {"
    )
    
    with open(path, 'w') as f:
        f.write(text)

