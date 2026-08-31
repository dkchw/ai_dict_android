import re

for screen in ['CompareScreen', 'TranslateScreen', 'ExplainScreen']:
    path = f"android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}.kt"
    with open(path, 'r') as f:
        text = f.read()

    # Find the fun ScreenName(...) block
    text = re.sub(
        rf"fun {screen}\([\s\S]*?modifier: Modifier = Modifier\n\)",
        f"fun {screen}(\n    viewModel: com.aidict.app.ui.viewmodels.SearchViewModel, profileId: Int,\n    autoNewSearch: Boolean = false,\n    onToggleAutoNewSearch: () -> Unit = {{}},\n    enterToSend: Boolean = false,\n    modifier: Modifier = Modifier\n)",
        text
    )
    
    with open(path, 'w') as f:
        f.write(text)

