import re

def update_screen(filename, input_prop):
    with open(filename, 'r') as f:
        text = f.read()
    
    # insert externalLinks state collection
    insert_idx = text.find('val state by viewModel.')
    if insert_idx != -1:
        end_of_line = text.find('\n', insert_idx) + 1
        text = text[:end_of_line] + '    val externalLinks by viewModel.externalLinks.collectAsState()\n' + text[end_of_line:]
    
    # Replace the old onExternalLink
    old_ext_link = f"""
            onExternalLink = {{
                val term = if (state.word != null) state.word!!.term else viewModel.{input_prop}
                if (term.isNotBlank()) {{
                    val url = viewModel.getExternalLinkTemplate().replace("{{word}}", term.trim())
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                    context.startActivity(intent)
                }}
            }},"""
            
    new_ext_link = f"""
            externalLinks = externalLinks,
            onExternalLinkClick = {{ link ->
                val term = if (state.word != null) state.word!!.term else viewModel.{input_prop}
                if (term.isNotBlank()) {{
                    val url = link.url.replace("{{word}}", term.trim())
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                    context.startActivity(intent)
                }}
            }},"""
            
    text = text.replace(old_ext_link, new_ext_link)
    
    with open(filename, 'w') as f:
        f.write(text)

update_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'searchInput')
update_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'compareInput')
update_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'explainInput')
update_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'translateInput')

