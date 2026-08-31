import os

screens = {
    "SearchScreen.kt": "dict",
    "CompareScreen.kt": "compare",
    "TranslateScreen.kt": "translate",
    "ExplainScreen.kt": "explain"
}

for filename, mode in screens.items():
    filepath = f"android_app/app/src/main/java/com/aidict/app/ui/screens/{filename}"
    with open(filepath, "r") as f:
        text = f.read()

    # 1. Fix state collection
    text = text.replace("viewModel.uiState.collectAsState()", f"viewModel.{mode}State.collectAsState()")

    # 2. Fix toggleStar
    text = text.replace("viewModel.toggleStar()", f'viewModel.toggleStar("{mode}")')

    # 3. Fix sendFollowUpMessage
    text = text.replace("viewModel.sendFollowUpMessage(viewModel.searchInput)", f'viewModel.sendFollowUpMessage(viewModel.searchInput, "{mode}")')
    text = text.replace("viewModel.sendFollowUpMessage(viewModel.compareInput)", f'viewModel.sendFollowUpMessage(viewModel.compareInput, "{mode}")')
    text = text.replace("viewModel.sendFollowUpMessage(viewModel.translateInput)", f'viewModel.sendFollowUpMessage(viewModel.translateInput, "{mode}")')
    text = text.replace("viewModel.sendFollowUpMessage(viewModel.explainInput)", f'viewModel.sendFollowUpMessage(viewModel.explainInput, "{mode}")')
    
    # 4. Fix stopStream
    text = text.replace("viewModel.stopStream()", f'viewModel.stopStream("{mode}")')

    # 5. Fix resumeChat
    text = text.replace("viewModel.resumeChat(editingContent)", f'viewModel.resumeChat(editingContent, "{mode}")')
    
    # 6. Fix retryMessage
    text = text.replace("viewModel.retryMessage(msg, false)", f'viewModel.retryMessage(msg, false, "{mode}")')
    text = text.replace("viewModel.retryMessage(msg, true)", f'viewModel.retryMessage(msg, true, "{mode}")')
    
    # 7. Fix deleteMessage
    text = text.replace("viewModel.deleteMessage(msg)", f'viewModel.deleteMessage(msg, "{mode}")')

    with open(filepath, "w") as f:
        f.write(text)

print("Updated screens")
