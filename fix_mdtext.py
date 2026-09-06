import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/MarkdownText.kt', 'r') as f:
    text = f.read()

# Make sure we have AnnotatedString imports
imports = """import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.foundation.text.selection.SelectionContainer"""
text = text.replace("import androidx.compose.foundation.text.selection.SelectionContainer", imports)

# Modify signature
target_sig = "fun MarkdownText(text: String, color: Color, modifier: Modifier = Modifier) {"
replacement_sig = "fun MarkdownText(text: String, color: Color, modifier: Modifier = Modifier, searchQuery: String = \"\") {"
text = text.replace(target_sig, replacement_sig)

# Modify the body
target_body = """    SelectionContainer(modifier = modifier) {
        RichText(
            style = tokyoNightStyle
        ) {
            Markdown(content = text)
        }
    }"""
replacement_body = """    SelectionContainer(modifier = modifier) {
        if (searchQuery.isNotBlank()) {
            val annotatedString = buildAnnotatedString {
                append(text)
                var index = text.indexOf(searchQuery, ignoreCase = true)
                while (index >= 0) {
                    addStyle(
                        style = SpanStyle(background = Color.Yellow, color = Color.Black),
                        start = index,
                        end = index + searchQuery.length
                    )
                    index = text.indexOf(searchQuery, startIndex = index + searchQuery.length, ignoreCase = true)
                }
            }
            androidx.compose.material3.Text(
                text = annotatedString,
                color = color
            )
        } else {
            RichText(
                style = tokyoNightStyle
            ) {
                Markdown(content = text)
            }
        }
    }"""
text = text.replace(target_body, replacement_body)

with open('android_app/app/src/main/java/com/aidict/app/ui/components/MarkdownText.kt', 'w') as f:
    f.write(text)
print("Updated MarkdownText.kt")
