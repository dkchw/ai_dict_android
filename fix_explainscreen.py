import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'r') as f:
    text = f.read()

# Add sourceLang and targetLang states inside Composable
insert_idx = text.find('val state by viewModel.explainState.collectAsState()')
if insert_idx != -1:
    end_of_line = text.find('\n', insert_idx) + 1
    new_states = """
    var sourceLang by remember { mutableStateOf("Auto Detect") }
    var targetLang by remember { mutableStateOf("English") }
    LaunchedEffect(profileId) {
        sourceLang = viewModel.getProfileSetting(profileId, "EXPLAIN_SOURCE") ?: "Auto Detect"
        targetLang = viewModel.getProfileSetting(profileId, "EXPLAIN_TARGET") ?: "English"
    }
"""
    text = text[:end_of_line] + new_states + text[end_of_line:]

# Update ChatInputBar in ExplainScreen
text = text.replace(
    'isFollowUp = state.word != null,',
    'isFollowUp = state.word != null,\n            sourceLang = if (state.word == null) sourceLang else null,\n            targetLang = if (state.word == null) targetLang else null,\n            onSourceLangChange = if (state.word == null) { { sourceLang = it; viewModel.saveProfileSetting(profileId, "EXPLAIN_SOURCE", it) } } else null,\n            onTargetLangChange = if (state.word == null) { { targetLang = it; viewModel.saveProfileSetting(profileId, "EXPLAIN_TARGET", it) } } else null,'
)

text = text.replace('viewModel.streamExplain(viewModel.explainInput, profileId)', 'viewModel.streamExplain(viewModel.explainInput, sourceLang, targetLang, profileId)')
text = text.replace('availableLanguages = viewModel.orderedLanguages.collectAsState().value,', '')
# Ensure availableLanguages is passed
text = text.replace('inputTerm = viewModel.explainInput,', 'availableLanguages = viewModel.orderedLanguages.collectAsState().value,\n            inputTerm = viewModel.explainInput,')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'w') as f:
    f.write(text)

