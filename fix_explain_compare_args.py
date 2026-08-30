import re

def fix_args(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # We will just rewrite the ChatInputBar call manually for these screens.
    if 'ExplainScreen' in filename:
        match = re.search(r'com\.aidict\.app\.ui\.components\.ChatInputBar\([^)]*\)', content, re.DOTALL)
        new_call = """com.aidict.app.ui.components.ChatInputBar(
            inputTerm = text,
            onValueChange = { text = it },
            onSend = { if (state.word != null) viewModel.sendFollowUpMessage(text) else viewModel.streamExplain(text, profileId); text = "" },
            isLoading = state.isLoading,
            isFollowUp = state.word != null,
            onClear = if (state.word != null) { { viewModel.clearCurrentSearch() } } else null,
            placeholder = "Paste sentence/paragraph to explain..."
        )"""
        content = content.replace(match.group(0), new_call)

    if 'CompareScreen' in filename:
        match = re.search(r'com\.aidict\.app\.ui\.components\.ChatInputBar\([^)]*\)', content, re.DOTALL)
        new_call = """com.aidict.app.ui.components.ChatInputBar(
            inputTerm = text,
            onValueChange = { text = it },
            onSend = { if (state.word != null) viewModel.sendFollowUpMessage(text) else viewModel.streamCompare(text, profileId); text = "" },
            isLoading = state.isLoading,
            isFollowUp = state.word != null,
            onClear = if (state.word != null) { { viewModel.clearCurrentSearch() } } else null,
            placeholder = "Words to compare (comma separated)..."
        )"""
        content = content.replace(match.group(0), new_call)
        
    with open(filename, 'w') as f:
        f.write(content)

fix_args('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt')
fix_args('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt')
