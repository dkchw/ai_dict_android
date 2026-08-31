import os

screens = [
    'SearchScreen', 'CompareScreen', 'TranslateScreen', 'ExplainScreen'
]

for screen in screens:
    path = f"android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}.kt"
    with open(path, 'r') as f:
        text = f.read()

    # Modify ChatInputBar call to include autoNewSearch arguments
    # Look for: onClear = ... )
    
    # Actually, let's just append the three arguments before the closing parenthesis of ChatInputBar.
    
    # Regex to find the ChatInputBar call and inject arguments
    # `onClear = { ... }` or `onClear = null`
    # Replace `onClear = (.*)` with `onClear = \1,\n            autoNewSearch = autoNewSearch,\n            onToggleAutoNewSearch = onToggleAutoNewSearch,\n            enterToSend = enterToSend`
    
    import re
    text = re.sub(
        r'(onClear = [^\n]+)', 
        r'\1,\n            autoNewSearch = autoNewSearch,\n            onToggleAutoNewSearch = onToggleAutoNewSearch,\n            enterToSend = enterToSend', 
        text
    )
    
    # Modify onSend lambda:
    # Look for `if (isFollowUp) {` or `if (state.word != null) {` inside `onSend = {`
    # Actually, let's just replace `onSend = {` with `onSend = { if (autoNewSearch && state.word != null) { viewModel.clearCurrentSearch(); viewModel.searchInput = "" }; `
    # But wait, if we clear it, `isFollowUp` might still evaluate to true if it was evaluated before the lambda?
    # No, `isFollowUp` is `val isFollowUp = state.word != null`. It evaluates to true.
    # Inside the lambda, `isFollowUp` is true, so it will call `viewModel.sendFollowUpMessage`.
    # Wait, if we clear it, we shouldn't use `sendFollowUpMessage`! We should use `viewModel.searchWord` or `streamSearch`.
    # It's better to rewrite the `onSend` completely.
    
    with open(path, 'w') as f:
        f.write(text)

