import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

text = text.replace('import androidx.compose.ui.Modifier', 'import androidx.compose.ui.Modifier\nimport androidx.compose.runtime.*\nimport coil.compose.AsyncImage\nimport com.aidict.app.models.ExternalLink\nimport androidx.compose.material.icons.filled.MoreVert')

# Update ChatInputBar signature
text = text.replace('onExternalLink: (() -> Unit)? = null,', 'externalLinks: List<ExternalLink> = emptyList(),\n    onExternalLinkClick: ((ExternalLink) -> Unit)? = null,')

# Update Icon implementation
old_icon_impl = """                if (onExternalLink != null) {
                    IconButton(
                        onClick = onExternalLink, 
                        modifier = Modifier
                            .padding(bottom = 8.dp, end = 8.dp)
                            .background(MaterialTheme.colorScheme.tertiaryContainer, CircleShape)
                    ) {
                        Icon(Icons.Default.Language, contentDescription = "External Link", tint = MaterialTheme.colorScheme.onTertiaryContainer)
                    }
                }"""

new_icon_impl = """                if (onExternalLinkClick != null && externalLinks.isNotEmpty()) {
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

text = text.replace(old_icon_impl, new_icon_impl)

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

