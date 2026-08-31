import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Add to imports if necessary
if 'import kotlinx.serialization.json.Json' not in text:
    text = text.replace('import androidx.compose.runtime.*', 'import androidx.compose.runtime.*\nimport kotlinx.serialization.json.Json\nimport kotlinx.serialization.encodeToString')

# Find the place where the SearchableDropdown for quotes is
old_quote_dropdown = """            com.aidict.app.ui.components.SearchableDropdown(

                label = "Display Quote on Empty Screens",

                currentValue = quote,

                options = quotes,

                onSelected = { viewModel.saveSetting("QUOTE_MODE", it) }

            )"""

new_quote_dropdown = """            com.aidict.app.ui.components.SearchableDropdown(
                label = "Display Quote on Empty Screens",
                currentValue = quote,
                options = quotes,
                onSelected = { viewModel.saveSetting("QUOTE_MODE", it) }
            )

            if (quote == "Shuffle") {
                val enabledQuotes by viewModel.shuffleEnabledQuotes.collectAsState()
                val currentEnabled = enabledQuotes ?: allQuotesList
                
                Card(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Quotes included in Shuffle:", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(bottom = 8.dp))
                        allQuotesList.forEach { q ->
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable {
                                val newSet = currentEnabled.toMutableSet()
                                if (newSet.contains(q)) newSet.remove(q) else newSet.add(q)
                                if (newSet.isEmpty()) newSet.add(q) // Ensure at least one
                                viewModel.saveSetting("SHUFFLE_ENABLED_QUOTES", Json.encodeToString(newSet.toList()))
                            }.padding(vertical = 4.dp)) {
                                androidx.compose.material3.Checkbox(
                                    checked = currentEnabled.contains(q),
                                    onCheckedChange = null
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(q, style = MaterialTheme.typography.bodyMedium)
                            }
                        }
                    }
                }
            }"""

text = text.replace(old_quote_dropdown, new_quote_dropdown)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

