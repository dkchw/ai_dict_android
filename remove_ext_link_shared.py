import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

# Remove external link block in ChatInputBar arguments
args_old = """    onClear: (() -> Unit)? = null,
    externalLinks: List<ExternalLink> = emptyList(),
    onExternalLinkClick: ((ExternalLink) -> Unit)? = null,
    modifier: Modifier = Modifier"""
args_new = """    onClear: (() -> Unit)? = null,
    modifier: Modifier = Modifier"""
text = text.replace(args_old, args_new)

# Remove the LazyRow block inside ChatInputBar
lazy_row_block = """            if (onExternalLinkClick != null && externalLinks.isNotEmpty()) {
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
text = text.replace(lazy_row_block, "")

# Remove imports
text = text.replace('import com.aidict.app.models.ExternalLink\n', '')
text = text.replace('import androidx.compose.foundation.lazy.LazyRow\nimport androidx.compose.foundation.lazy.items\n', '')

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)
