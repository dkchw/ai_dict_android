import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/MarkdownText.kt', 'r') as f:
    text = f.read()

# Replace textStyle.copy with textStyle.copy + fontWeight
text = text.replace("textStyle.copy(color = Color(0xFFBB9AF7))", "textStyle.copy(color = Color(0xFFBB9AF7), fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)")
text = text.replace("textStyle.copy(color = Color(0xFF7DCFFF))", "textStyle.copy(color = Color(0xFF7DCFFF), fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)")
text = text.replace("textStyle.copy(color = Color(0xFF7AA2F7))", "textStyle.copy(color = Color(0xFF7AA2F7), fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)")
text = text.replace("textStyle.copy(color = Color(0xFFE0AF68))", "textStyle.copy(color = Color(0xFFE0AF68), fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)")
text = text.replace("textStyle.copy(color = Color(0xFFF7768E))", "textStyle.copy(color = Color(0xFFF7768E), fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)")
text = text.replace("textStyle.copy(color = Color(0xFF9ECE6A))", "textStyle.copy(color = Color(0xFF9ECE6A), fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)")
text = text.replace("textStyle.copy(color = Color(0xFFC0CAF5))", "textStyle.copy(color = Color(0xFFC0CAF5), fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)")

with open('android_app/app/src/main/java/com/aidict/app/ui/components/MarkdownText.kt', 'w') as f:
    f.write(text)
