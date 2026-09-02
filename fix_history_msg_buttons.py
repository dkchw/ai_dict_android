import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

target = """                        Row(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth(if (isUser) 0.85f else 1f)
                                    .background(
                                        color = if (isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.secondaryContainer,
                                        shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp)
                                    )
                                    .padding(12.dp)
                            ) {
                                com.aidict.app.ui.components.MarkdownText(
                                    text = msg.content,
                                    color = if (isUser) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSecondaryContainer
                                )
                            }
                        }"""

replacement = """                        Row(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
                        ) {
                            Column(modifier = Modifier.fillMaxWidth(if (isUser) 0.85f else 1f)) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth(if (isUser) 1f else 0.85f)
                                        .background(
                                            color = if (isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.secondaryContainer,
                                            shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp)
                                        )
                                        .padding(12.dp)
                                ) {
                                    com.aidict.app.ui.components.MarkdownText(
                                        text = msg.content,
                                        color = if (isUser) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSecondaryContainer
                                    )
                                }
                                if (!isUser) {
                                    Row(modifier = Modifier.fillMaxWidth(0.85f), horizontalArrangement = Arrangement.Start) {
                                        IconButton(onClick = {
                                            val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                                            clipboard.setPrimaryClip(android.content.ClipData.newPlainText("AI Dict", msg.content))
                                            android.widget.Toast.makeText(context, "Copied", android.widget.Toast.LENGTH_SHORT).show()
                                        }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.ContentCopy, "Copy", modifier = Modifier.size(16.dp)) }
                                        IconButton(onClick = { onRestartChat(selectedWord!!, msg, false) }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Refresh, "Regenerate (Current)", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp)) }
                                        IconButton(onClick = { onRestartChat(selectedWord!!, msg, true) }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Autorenew, "Regenerate (Fallback)", tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(16.dp)) }
                                    }
                                }
                            }
                        }"""

text = text.replace(target, replacement)

# We need `context` in HistoryScreen for the copy feature.
if "val context = LocalContext.current" not in text:
    # Add it at the top of HistoryScreen
    text = text.replace("    val scope = rememberCoroutineScope()", "    val scope = rememberCoroutineScope()\n    val context = androidx.compose.ui.platform.LocalContext.current")

# Add ContentCopy icon import if missing
if "import androidx.compose.material.icons.filled.ContentCopy" not in text:
    text = text.replace("import androidx.compose.material.icons.filled.Add", "import androidx.compose.material.icons.filled.Add\nimport androidx.compose.material.icons.filled.ContentCopy")

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

print("Added buttons to HistoryScreen detail view")
