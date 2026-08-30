sed -i 's/import androidx.compose.material.icons.filled.Star/import androidx.compose.material.icons.filled.Star\nimport androidx.compose.material.icons.filled.Refresh\nimport androidx.compose.material.icons.filled.Warning\nimport androidx.compose.material.icons.filled.Edit\nimport androidx.compose.material.icons.filled.Clear\n/' android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt

cat << 'INNER' > patch.txt
                    Column(modifier = Modifier.fillMaxWidth(0.85f)) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp)
                                .background(
                                    color = if (isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.secondaryContainer,
                                    shape = RoundedCornerShape(12.dp)
                                )
                                .padding(12.dp)
                        ) {
                            if (isUser) {
                                Text(text = msg.content, color = MaterialTheme.colorScheme.onPrimary)
                            } else {
                                Text(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer)
                            }
                        }
                        
                        if (!isUser) {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Start) {
                                IconButton(onClick = {
                                    val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                                    clipboard.setPrimaryClip(ClipData.newPlainText("AI Dict", msg.content))
                                    Toast.makeText(context, "Copied", Toast.LENGTH_SHORT).show()
                                }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.ContentCopy, "Copy", modifier = Modifier.size(16.dp)) }
                                
                                IconButton(onClick = { viewModel.retryMessage(msg, false) }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Refresh, "Retry", modifier = Modifier.size(16.dp)) }
                                
                                IconButton(onClick = { viewModel.retryMessage(msg, true) }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Warning, "Retry Fallback", modifier = Modifier.size(16.dp)) }
                                
                                IconButton(onClick = { viewModel.deleteMessage(msg) }, modifier = Modifier.size(32.dp)) { Icon(Icons.Default.Delete, "Delete", modifier = Modifier.size(16.dp)) }
                            }
                        }
                    }
INNER

# We need to replace the Box with the Column
# The original is:
#                     Box(
#                         modifier = Modifier
#                             .fillMaxWidth(0.85f)
#                             .padding(vertical = 4.dp)
#                             .background(
#                                 color = if (isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.secondaryContainer,
#                                 shape = RoundedCornerShape(12.dp)
#                             )
#                             .padding(12.dp)
#                     ) {
#                         if (isUser) {
#                             Text(text = msg.content, color = MaterialTheme.colorScheme.onPrimary)
#                         } else {
#                             Text(text = msg.content, color = MaterialTheme.colorScheme.onSecondaryContainer)
#                         }
#                     }

