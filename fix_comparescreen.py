import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'r') as f:
    text = f.read()

# Add sourceLang and targetLang states inside Composable
insert_idx = text.find('val state by viewModel.compareState.collectAsState()')
if insert_idx != -1:
    end_of_line = text.find('\n', insert_idx) + 1
    new_states = """
    var sourceLang by remember { mutableStateOf("Auto Detect") }
    var targetLang by remember { mutableStateOf("English") }
    LaunchedEffect(profileId) {
        sourceLang = viewModel.getProfileSetting(profileId, "COMPARE_SOURCE") ?: "Auto Detect"
        targetLang = viewModel.getProfileSetting(profileId, "COMPARE_TARGET") ?: "English"
    }
"""
    text = text[:end_of_line] + new_states + text[end_of_line:]

# Update ChatInputBar in CompareScreen
text = text.replace(
    'isFollowUp = state.word != null,',
    'isFollowUp = state.word != null,\n            sourceLang = if (state.word == null) sourceLang else null,\n            targetLang = if (state.word == null) targetLang else null,\n            onSourceLangChange = if (state.word == null) { { sourceLang = it; viewModel.saveProfileSetting(profileId, "COMPARE_SOURCE", it) } } else null,\n            onTargetLangChange = if (state.word == null) { { targetLang = it; viewModel.saveProfileSetting(profileId, "COMPARE_TARGET", it) } } else null,'
)

text = text.replace('viewModel.streamCompare(viewModel.compareInput, profileId)', 'viewModel.streamCompare(viewModel.compareInput, sourceLang, targetLang, profileId)')
text = text.replace('availableLanguages = viewModel.orderedLanguages.collectAsState().value,', '')
# Ensure availableLanguages is passed
text = text.replace('inputTerm = viewModel.compareInput,', 'availableLanguages = viewModel.orderedLanguages.collectAsState().value,\n            inputTerm = viewModel.compareInput,')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'w') as f:
    f.write(text)

