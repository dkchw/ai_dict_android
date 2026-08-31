import re

for screen, mode in [
    ('SearchScreen', 'dict'),
    ('CompareScreen', 'compare'),
    ('TranslateScreen', 'translate'),
    ('ExplainScreen', 'explain')
]:
    path = f"android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}.kt"
    with open(path, 'r') as f:
        text = f.read()

    # Find the onSend block
    # It might be `onSend = { ... },`
    # Let's use regex to replace the onSend block.
    # It usually starts with `onSend = {` and ends before `isLoading = state.isLoading,`
    
    # We can use a simpler string replacement for each specific screen.
    if screen == 'SearchScreen':
        old = """            onSend = {
                if (isFollowUp) {
                    viewModel.sendFollowUpMessage(viewModel.searchInput, "dict")
                } else {
                    viewModel.searchWord(viewModel.searchInput, sourceLang, targetLang, profileId)
                }
                viewModel.searchInput = ""
            },"""
        new = """            onSend = {
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
        text = text.replace(old, new)
    elif screen == 'CompareScreen':
        old = """            onSend = {
                if (state.word != null) {
                    viewModel.sendFollowUpMessage(viewModel.searchInput, "compare")
                } else {
                    viewModel.streamSearch(viewModel.searchInput, profileId = profileId, mode = "compare")
                }
                viewModel.searchInput = ""
            },"""
        new = """            onSend = {
                if (autoNewSearch && state.word != null) {
                    viewModel.clearCurrentSearch()
                    viewModel.streamSearch(viewModel.searchInput, profileId = profileId, mode = "compare")
                } else if (state.word != null) {
                    viewModel.sendFollowUpMessage(viewModel.searchInput, "compare")
                } else {
                    viewModel.streamSearch(viewModel.searchInput, profileId = profileId, mode = "compare")
                }
                viewModel.searchInput = ""
            },"""
        text = text.replace(old, new)
    elif screen == 'TranslateScreen':
        old = """            onSend = {
                if (state.word != null) {
                    viewModel.sendFollowUpMessage(viewModel.searchInput, "translate")
                } else {
                    viewModel.streamSearch(viewModel.searchInput, sourceLang, targetLang, profileId, "translate")
                }
                viewModel.searchInput = ""
            },"""
        new = """            onSend = {
                if (autoNewSearch && state.word != null) {
                    viewModel.clearCurrentSearch()
                    viewModel.streamSearch(viewModel.searchInput, sourceLang, targetLang, profileId, "translate")
                } else if (state.word != null) {
                    viewModel.sendFollowUpMessage(viewModel.searchInput, "translate")
                } else {
                    viewModel.streamSearch(viewModel.searchInput, sourceLang, targetLang, profileId, "translate")
                }
                viewModel.searchInput = ""
            },"""
        text = text.replace(old, new)
    elif screen == 'ExplainScreen':
        old = """            onSend = {
                if (state.word != null) {
                    viewModel.sendFollowUpMessage(viewModel.searchInput, "explain")
                } else {
                    viewModel.streamSearch(viewModel.searchInput, profileId = profileId, mode = "explain")
                }
                viewModel.searchInput = ""
            },"""
        new = """            onSend = {
                if (autoNewSearch && state.word != null) {
                    viewModel.clearCurrentSearch()
                    viewModel.streamSearch(viewModel.searchInput, profileId = profileId, mode = "explain")
                } else if (state.word != null) {
                    viewModel.sendFollowUpMessage(viewModel.searchInput, "explain")
                } else {
                    viewModel.streamSearch(viewModel.searchInput, profileId = profileId, mode = "explain")
                }
                viewModel.searchInput = ""
            },"""
        text = text.replace(old, new)
        
    with open(path, 'w') as f:
        f.write(text)

