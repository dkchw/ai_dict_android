import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'r') as f:
    text = f.read()

ext_link_impl = """
            externalLinks = if (isFollowUp) externalLinks else emptyList(),
            onExternalLinkClick = { link ->
                val term = if (state.word != null) state.word!!.term else viewModel.searchInput
                if (term.isNotBlank()) {
                    val url = link.url.replace("{word}", term.trim())
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                    context.startActivity(intent)
                }
            },"""

text = text.replace('isFollowUp = isFollowUp,', f'isFollowUp = isFollowUp,{ext_link_impl}')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'w') as f:
    f.write(text)

