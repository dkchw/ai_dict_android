import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/MarkdownText.kt', 'r') as f:
    text = f.read()

# Add import
import_target = "import androidx.compose.ui.unit.sp"
import_replacement = "import androidx.compose.ui.unit.sp\nimport androidx.compose.foundation.text.selection.SelectionContainer"
text = text.replace(import_target, import_replacement)

# Wrap RichText
target = """    RichText(
        modifier = modifier,
        style = tokyoNightStyle
    ) {
        Markdown(content = text)
    }"""
replacement = """    SelectionContainer(modifier = modifier) {
        RichText(
            style = tokyoNightStyle
        ) {
            Markdown(content = text)
        }
    }"""
text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/components/MarkdownText.kt', 'w') as f:
    f.write(text)

print("Patched MarkdownText.kt")
