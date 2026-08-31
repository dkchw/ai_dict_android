import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

# Add imports
text = text.replace('import androidx.compose.ui.Modifier', 'import androidx.compose.ui.Modifier\nimport androidx.compose.foundation.lazy.LazyRow\nimport androidx.compose.foundation.lazy.items')

# Remove the old icon button block from the Row
old_icon_block = """                                if (onExternalLinkClick != null && externalLinks.isNotEmpty()) {
                    val firstLink = externalLinks.first()
                    IconButton(
                        onClick = { onExternalLinkClick(firstLink) },
                        modifier = Modifier
                            .padding(bottom = 8.dp, end = if (externalLinks.size > 1) 0.dp else 8.dp)
                            .background(MaterialTheme.colorScheme.tertiaryContainer, CircleShape)
                    ) {
                        if (firstLink.iconUrl.isNotBlank()) {
                            AsyncImage(model = firstLink.iconUrl, contentDescription = firstLink.name, modifier = Modifier.size(24.dp))
                        } else {
                            Icon(Icons.Default.Language, contentDescription = firstLink.name, tint = MaterialTheme.colorScheme.onTertiaryContainer)
                        }
                    }
                    if (externalLinks.size > 1) {
                        var expanded by remember { mutableStateOf(false) }
                        Box(modifier = Modifier.padding(bottom = 8.dp, end = 8.dp)) {
                            IconButton(onClick = { expanded = true }) {
                                Icon(Icons.Default.MoreVert, contentDescription = "More Links")
                            }
                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                externalLinks.drop(1).forEach { link ->
                                    DropdownMenuItem(
                                        text = { Text(link.name) },
                                        onClick = { onExternalLinkClick(link); expanded = false },
                                        leadingIcon = {
                                            if (link.iconUrl.isNotBlank()) {
                                                AsyncImage(model = link.iconUrl, contentDescription = link.name, modifier = Modifier.size(20.dp))
                                            } else {
                                                Icon(Icons.Default.Language, contentDescription = link.name)
                                            }
                                        }
                                    )
                                }
                            }
                        }
                    }
                }"""

if old_icon_block in text:
    text = text.replace(old_icon_block, "")
else:
    print("Warning: old block not found exactly. Check regex if needed.")

# We want to insert the new addon row right above the `Row` for the text input
new_addon_block = """            if (onExternalLinkClick != null && externalLinks.isNotEmpty()) {
                LazyRow(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 4.dp, start = 8.dp, end = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    items(externalLinks) { link ->
                        AssistChip(
                            onClick = { onExternalLinkClick(link) },
                            label = { Text(link.name, style = MaterialTheme.typography.labelSmall) },
                            leadingIcon = {
                                if (link.iconUrl.isNotBlank()) {
                                    AsyncImage(model = link.iconUrl, contentDescription = link.name, modifier = Modifier.size(16.dp))
                                } else {
                                    Icon(Icons.Default.Language, contentDescription = link.name, modifier = Modifier.size(16.dp))
                                }
                            },
                            shape = CircleShape,
                            colors = AssistChipDefaults.assistChipColors(containerColor = MaterialTheme.colorScheme.tertiaryContainer, labelColor = MaterialTheme.colorScheme.onTertiaryContainer)
                        )
                    }
                }
            }
"""

text = text.replace('            Row(\n                modifier = Modifier.fillMaxWidth(),', new_addon_block + '            Row(\n                modifier = Modifier.fillMaxWidth(),')

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

