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

    text = text.replace("viewModel.editMessage(msg, editingContent)", f'viewModel.editMessage(msg, editingContent, "{mode}")')

    with open(filepath, "w") as f:
        f.write(text)

