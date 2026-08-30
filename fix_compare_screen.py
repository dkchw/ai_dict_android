import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'r') as f:
    search_content = f.read()

lazy_column = re.search(r'(// Chat History & Streaming.*?)\s*// Unified Input Bar', search_content, re.DOTALL).group(1)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'r') as f:
    content = f.read()
    
# Inject lazy column
content = re.sub(r'Box\(modifier = Modifier.weight\(1f\).*?// Bottom Input Bar', lazy_column + '\n\n        // Bottom Input Bar', content, flags=re.DOTALL)
# But wait, CompareScreen doesn't have // Bottom Input Bar in the previous sed, let's just replace Box.
match = re.search(r'Box\(modifier = Modifier.weight\(1f\).*?com.aidict.app.ui.components.ChatInputBar', content, re.DOTALL)
if match:
    # Just replace the Box inside
    old_box = re.search(r'Box\(modifier = Modifier.weight\(1f\).*?}\n        }', content, re.DOTALL).group(0)
    content = content.replace(old_box, lazy_column)

# Update ChatInputBar
content = content.replace('inputTerm = text', 'inputTerm = text\n            isFollowUp = state.word != null')
content = content.replace('onSend = { viewModel.streamCompare(text, profileId) }', 'onSend = { if(state.word != null) viewModel.sendFollowUpMessage(text) else viewModel.streamCompare(text, profileId); text = "" }')
content = content.replace('placeholder = ', 'onClear = if (state.word != null) { { viewModel.clearCurrentSearch() } } else null,\n            placeholder = ')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'w') as f:
    f.write(content)
