import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

# Add import
if "import androidx.compose.foundation.text.selection.SelectionContainer" not in text:
    import_target = "import androidx.compose.ui.unit.sp"
    import_replacement = "import androidx.compose.ui.unit.sp\nimport androidx.compose.foundation.text.selection.SelectionContainer"
    text = text.replace(import_target, import_replacement)

# Wrap term in SelectionContainer
target = "Text(text = word.term, style = MaterialTheme.typography.bodyLarge)"
replacement = "SelectionContainer { Text(text = word.term, style = MaterialTheme.typography.bodyLarge) }"
text = text.replace(target, replacement)

# Wrap details header in SelectionContainer
target_2 = "Text(text = \"Details\", style = MaterialTheme.typography.titleLarge, modifier = Modifier.weight(1f))"
replacement_2 = "SelectionContainer(modifier = Modifier.weight(1f)) { Text(text = \"Details\", style = MaterialTheme.typography.titleLarge) }"
text = text.replace(target_2, replacement_2)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

print("Patched HistoryScreen.kt")
