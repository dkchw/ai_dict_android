import re

def update_screen(filename, input_prop):
    with open(filename, 'r') as f:
        text = f.read()
    
    # ensure intent and uri are imported
    if 'import android.content.Intent' not in text:
        text = text.replace('import androidx.compose.ui.Modifier', 'import androidx.compose.ui.Modifier\nimport android.content.Intent\nimport android.net.Uri\nimport androidx.compose.ui.platform.LocalContext')
        
    # generate onExternalLink implementation
    ext_link_impl = f"""
            onExternalLink = {{
                val term = if (state.word != null) state.word!!.term else viewModel.{input_prop}
                if (term.isNotBlank()) {{
                    val url = viewModel.getExternalLinkTemplate().replace("{{word}}", term.trim())
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                    context.startActivity(intent)
                }}
            }},"""
            
    # Inject into ChatInputBar
    text = text.replace('isFollowUp = state.word != null,', f'isFollowUp = state.word != null,{ext_link_impl}')
    
    with open(filename, 'w') as f:
        f.write(text)

update_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'searchInput')
update_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'compareInput')
update_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'explainInput')
update_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'translateInput')

