import re

def update_screen(filename, search_logic_func):
    with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'r') as f:
        search_content = f.read()

    lazy_column = re.search(r'(// Chat History & Streaming.*?)\s*// Unified Input Bar', search_content, re.DOTALL).group(1)

    with open(filename, 'r') as f:
        content = f.read()
        
    # Inject lazy column
    content = re.sub(r'// Response Area.*?// Bottom Input Bar', lazy_column + '\n\n        // Bottom Input Bar', content, flags=re.DOTALL)
    
    # Update ChatInputBar
    # We need to add isFollowUp and onClear
    content = content.replace('placeholder = ', 'isFollowUp = state.word != null,\n            onClear = if (state.word != null) { { viewModel.clearCurrentSearch() } } else null,\n            placeholder = ')
    
    # Change the onSend logic
    if search_logic_func:
        content = re.sub(r'onSend = \{.*?\},', f'onSend = {{\n                if (state.word != null) {{\n                    viewModel.sendFollowUpMessage(sourceText)\n                }} else {{\n                    {search_logic_func}\n                }}\n                sourceText = ""\n            }},', content, flags=re.DOTALL)
    
    with open(filename, 'w') as f:
        f.write(content)

update_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'viewModel.streamTranslation(sourceText, sourceLang, targetLang, profileId)')

# For explain, the variable is `text`, not `sourceText`
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'r') as f:
    content = f.read()
content = content.replace('inputTerm = text', 'inputTerm = text\n            isFollowUp = state.word != null')
content = content.replace('onSend = { viewModel.streamExplain(text, profileId) }', 'onSend = { if(state.word != null) viewModel.sendFollowUpMessage(text) else viewModel.streamExplain(text, profileId); text = "" }')
content = content.replace('placeholder = ', 'onClear = if (state.word != null) { { viewModel.clearCurrentSearch() } } else null,\n            placeholder = ')
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'w') as f:
    f.write(content)

update_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', None) # Already manually did onSend

# For Compare, variable is `word1`, `word2`
# Compare doesn't use ChatInputBar directly for its two inputs... wait it does!
# But for follow up, it just needs ONE input.
# CompareScreen has ChatInputBar?
