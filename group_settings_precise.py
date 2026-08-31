import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Add imports
if 'import androidx.compose.foundation.shape.RoundedCornerShape' not in text:
    text = text.replace('import androidx.compose.foundation.shape.CircleShape', 'import androidx.compose.foundation.shape.CircleShape\nimport androidx.compose.foundation.shape.RoundedCornerShape')

# Add SettingsGroup
group_composable = """
@Composable
fun SettingsGroup(title: String, content: @Composable () -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    Card(
        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { expanded = !expanded }
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(title, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
                Icon(if (expanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown, contentDescription = "Toggle")
            }
            androidx.compose.animation.AnimatedVisibility(visible = expanded) {
                Column(modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, bottom = 16.dp)) {
                    content()
                }
            }
        }
    }
}
"""

if 'fun SettingsGroup(' not in text:
    text = text.replace('@Composable\nfun SettingsScreen(', group_composable + '\n@Composable\nfun SettingsScreen(')


# 1. Models
# Find:
# item { Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Models", style = MaterialTheme.typography.titleLarge); Button(onClick = { viewModel.refreshModels() }) { Icon(Icons.Default.Refresh, contentDescription = "Refresh Models", modifier = Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Refresh") } } }
# ...
# item { SearchableModelDropdown("Chat Model", chatModel, availableModels) { viewModel.saveSetting("CHAT_MODEL", it) } }

models_regex = r'item \{ Row.*?Text\("Models".*?\}\s*item \{ SearchableModelDropdown\("Dict Model".*?item \{ SearchableModelDropdown\("Chat Model", chatModel, availableModels\) \{ viewModel\.saveSetting\("CHAT_MODEL", it\) \} \}'
models_match = re.search(models_regex, text, re.DOTALL)
if models_match:
    original = models_match.group(0)
    # Extract the internal SearchableModelDropdown lines
    lines = [line.strip() for line in original.split('\n') if 'SearchableModelDropdown' in line]
    inner = '\n                '.join(lines)
    new_models = f"""item {{
            SettingsGroup("Models") {{
                Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.End) {{
                    Button(onClick = {{ viewModel.refreshModels() }}) {{ Icon(Icons.Default.Refresh, contentDescription = "Refresh Models", modifier = Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Refresh") }}
                }}
                {inner}
            }}
        }}"""
    text = text.replace(original, new_models)


# 2. Prompts
# Find:
# item { Text("Prompts", style = MaterialTheme.typography.titleLarge) }
# item { OutlinedTextField(value = dictPrompt...
# item { Spacer(Modifier.height(16.dp)) }
# item { OutlinedTextField(value = comparePrompt...
# item { OutlinedTextField(value = explainPrompt...
# item { OutlinedTextField(value = translatePrompt...

prompts_regex = r'item \{ Text\("Prompts", style = MaterialTheme.typography.titleLarge\) \}\s*item \{\s*OutlinedTextField\(\s*value = dictPrompt[\s\S]*?item \{\s*OutlinedTextField\(\s*value = translatePrompt[\s\S]*?\}\s*\}'
prompts_match = re.search(prompts_regex, text)
if prompts_match:
    original = prompts_match.group(0)
    
    # We will just rewrite the Prompts section entirely since we know its exact shape.
    new_prompts = """item {
            SettingsGroup("Prompts") {
                OutlinedTextField(value = dictPrompt, onValueChange = { viewModel.saveSetting("DICT_PROMPT", it) }, label = { Text("Dict Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), minLines = 3)
                OutlinedTextField(value = comparePrompt, onValueChange = { viewModel.saveSetting("COMPARE_PROMPT", it) }, label = { Text("Compare Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), minLines = 3)
                OutlinedTextField(value = explainPrompt, onValueChange = { viewModel.saveSetting("EXPLAIN_PROMPT", it) }, label = { Text("Explain Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), minLines = 3)
                OutlinedTextField(value = translatePrompt, onValueChange = { viewModel.saveSetting("TRANSLATE_PROMPT", it) }, label = { Text("Translate Prompt") }, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), minLines = 3)
            }
        }"""
    text = text.replace(original, new_prompts)

# 3. Backgrounds
# It spans from `item { Text("Backgrounds"...` to the `Explain Mode BG` block.
bgs_regex = r'item \{ Text\("Backgrounds", style = MaterialTheme.typography.titleLarge\) \}[\s\S]*?viewModel\.saveSetting\("BG_EXPLAIN", ""\) \}\) \{ Icon\(Icons\.Default\.Delete, "Clear"\) \}\s*\}\s*\}'
bgs_match = re.search(bgs_regex, text)
if bgs_match:
    original = bgs_match.group(0)
    # Simply remove all `item {` and `}` wrappers inside it.
    inner = original.replace('item { Text("Backgrounds", style = MaterialTheme.typography.titleLarge) }', '')
    # Now remove all `item {` and the corresponding `}`.
    # It's easier to just construct it manually.
    new_bgs = """item {
            SettingsGroup("Backgrounds") {
                val bgUniversal by viewModel.bgUniversal.collectAsState()
                val universalLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_UNIVERSAL", it.toString()) } }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Universal BG (Fallback)"); Button(onClick = { universalLauncher.launch(arrayOf("image/*")) }) { Text(if (bgUniversal == null) "Select" else "Change") }; if (bgUniversal != null) IconButton(onClick = { viewModel.saveSetting("BG_UNIVERSAL", "") }) { Icon(Icons.Default.Delete, "Clear") } }
                
                val bgDict by viewModel.bgDict.collectAsState()
                val dictLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_DICT", it.toString()) } }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Dict Mode BG"); Button(onClick = { dictLauncher.launch(arrayOf("image/*")) }) { Text(if (bgDict == null) "Select" else "Change") }; if (bgDict != null) IconButton(onClick = { viewModel.saveSetting("BG_DICT", "") }) { Icon(Icons.Default.Delete, "Clear") } }

                val bgCompare by viewModel.bgCompare.collectAsState()
                val compareLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_COMPARE", it.toString()) } }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Compare Mode BG"); Button(onClick = { compareLauncher.launch(arrayOf("image/*")) }) { Text(if (bgCompare == null) "Select" else "Change") }; if (bgCompare != null) IconButton(onClick = { viewModel.saveSetting("BG_COMPARE", "") }) { Icon(Icons.Default.Delete, "Clear") } }

                val bgTranslate by viewModel.bgTranslate.collectAsState()
                val translateLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_TRANSLATE", it.toString()) } }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Translate Mode BG"); Button(onClick = { translateLauncher.launch(arrayOf("image/*")) }) { Text(if (bgTranslate == null) "Select" else "Change") }; if (bgTranslate != null) IconButton(onClick = { viewModel.saveSetting("BG_TRANSLATE", "") }) { Icon(Icons.Default.Delete, "Clear") } }

                val bgExplain by viewModel.bgExplain.collectAsState()
                val explainLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_EXPLAIN", it.toString()) } }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) { Text("Explain Mode BG"); Button(onClick = { explainLauncher.launch(arrayOf("image/*")) }) { Text(if (bgExplain == null) "Select" else "Change") }; if (bgExplain != null) IconButton(onClick = { viewModel.saveSetting("BG_EXPLAIN", "") }) { Icon(Icons.Default.Delete, "Clear") } }
            }
        }"""
    text = text.replace(original, new_bgs)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

