import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Make sure Icons.Default.KeyboardArrowUp/Down are imported if needed. ArrowUpward is standard.
if 'import androidx.compose.material.icons.filled.ArrowUpward' not in text:
    text = text.replace('import androidx.compose.material.icons.filled.Delete', 'import androidx.compose.material.icons.filled.Delete\nimport androidx.compose.material.icons.filled.ArrowUpward\nimport androidx.compose.material.icons.filled.ArrowDownward')

# Update URL label
text = text.replace('Text("URL (use {word})")', 'Text("URL (use {{str}})")')

# Update the Button row to include move up/down
old_button_code = """                    Button(onClick = { 
                        val newLinks = externalLinks.toMutableList()
                        newLinks.removeAt(index)
                        viewModel.saveExternalLinks(newLinks)
                    }, modifier = Modifier.align(Alignment.End).padding(top = 8.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) {
                        Text("Remove")
                    }"""

new_button_code = """                    Row(modifier = Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Row {
                            IconButton(onClick = { 
                                if (index > 0) {
                                    val newLinks = externalLinks.toMutableList()
                                    val temp = newLinks[index]
                                    newLinks[index] = newLinks[index - 1]
                                    newLinks[index - 1] = temp
                                    viewModel.saveExternalLinks(newLinks)
                                }
                            }, enabled = index > 0) {
                                Icon(Icons.Default.ArrowUpward, contentDescription = "Move Up")
                            }
                            IconButton(onClick = { 
                                if (index < externalLinks.size - 1) {
                                    val newLinks = externalLinks.toMutableList()
                                    val temp = newLinks[index]
                                    newLinks[index] = newLinks[index + 1]
                                    newLinks[index + 1] = temp
                                    viewModel.saveExternalLinks(newLinks)
                                }
                            }, enabled = index < externalLinks.size - 1) {
                                Icon(Icons.Default.ArrowDownward, contentDescription = "Move Down")
                            }
                        }
                        Button(onClick = { 
                            val newLinks = externalLinks.toMutableList()
                            newLinks.removeAt(index)
                            viewModel.saveExternalLinks(newLinks)
                        }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) {
                            Text("Remove")
                        }
                    }"""

text = text.replace(old_button_code, new_button_code)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

