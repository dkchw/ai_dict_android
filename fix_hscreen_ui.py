import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

# Add searchInOutput flow collection
state_vars = """    val colorFilter by viewModel.colorFilter.collectAsState()
    val starsFilter by viewModel.starsFilter.collectAsState()
    val activeSessionId by viewModel.activeSessionId.collectAsState()
    val searchInOutput by viewModel.searchInOutput.collectAsState()"""

text = text.replace('    val colorFilter by viewModel.colorFilter.collectAsState()\n    val starsFilter by viewModel.starsFilter.collectAsState()\n    val activeSessionId by viewModel.activeSessionId.collectAsState()', state_vars)

# Add FilterChip
target_filters = """            Row(
                modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {"""

replacement_filters = """            Row(
                modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                FilterChip(
                    selected = searchInOutput,
                    onClick = { viewModel.toggleSearchInOutput() },
                    label = { Text("Search Output") },
                    leadingIcon = { if (searchInOutput) Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                )
                HorizontalDivider(modifier = Modifier.width(1.dp).height(24.dp))"""

text = text.replace(target_filters, replacement_filters)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

print("Updated HistoryScreen UI")
