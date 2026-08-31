import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

bg_old = """        item { Text("Backgrounds", style = MaterialTheme.typography.titleLarge) }

        item {

            val bgDict by viewModel.bgDict.collectAsState()
            val bgUniversal by viewModel.bgUniversal.collectAsState()
            
            val universalLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->

                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_UNIVERSAL", it.toString()) }

            }

            val dictLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->

                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_DICT", it.toString()) }
            }

            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {

                Text("Universal BG (Fallback)")
                Button(onClick = { universalLauncher.launch(arrayOf("image/*")) }) { Text(if (bgUniversal == null) "Select" else "Change") }
                if (bgUniversal != null) IconButton(onClick = { viewModel.saveSetting("BG_UNIVERSAL", "") }) { Icon(Icons.Default.Delete, "Clear") }
            }
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Dict Mode BG")

                Button(onClick = { dictLauncher.launch(arrayOf("image/*")) }) { Text(if (bgDict == null) "Select" else "Change") }

                if (bgDict != null) IconButton(onClick = { viewModel.saveSetting("BG_DICT", "") }) { Icon(Icons.Default.Delete, "Clear") }

            }

        }

        item {

            val bgCompare by viewModel.bgCompare.collectAsState()

            val compareLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->

                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_COMPARE", it.toString()) }

            }

            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {

                Text("Compare Mode BG")

                Button(onClick = { compareLauncher.launch(arrayOf("image/*")) }) { Text(if (bgCompare == null) "Select" else "Change") }

                if (bgCompare != null) IconButton(onClick = { viewModel.saveSetting("BG_COMPARE", "") }) { Icon(Icons.Default.Delete, "Clear") }

            }

        }

        item {

            val bgTranslate by viewModel.bgTranslate.collectAsState()

            val translateLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->

                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_TRANSLATE", it.toString()) }

            }

            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {

                Text("Translate Mode BG")

                Button(onClick = { translateLauncher.launch(arrayOf("image/*")) }) { Text(if (bgTranslate == null) "Select" else "Change") }

                if (bgTranslate != null) IconButton(onClick = { viewModel.saveSetting("BG_TRANSLATE", "") }) { Icon(Icons.Default.Delete, "Clear") }

            }

        }

        item {

            val bgExplain by viewModel.bgExplain.collectAsState()

            val explainLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->

                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_EXPLAIN", it.toString()) }

            }

            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {

                Text("Explain Mode BG")

                Button(onClick = { explainLauncher.launch(arrayOf("image/*")) }) { Text(if (bgExplain == null) "Select" else "Change") }

                if (bgExplain != null) IconButton(onClick = { viewModel.saveSetting("BG_EXPLAIN", "") }) { Icon(Icons.Default.Delete, "Clear") }

            }

        }"""

bg_new = """        item {
            Column {
                Text("Backgrounds", style = MaterialTheme.typography.titleLarge)

                val bgUniversal by viewModel.bgUniversal.collectAsState()
                val universalLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
                    uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_UNIVERSAL", it.toString()) }
                }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text("Universal BG (Fallback)")
                    Button(onClick = { universalLauncher.launch(arrayOf("image/*")) }) { Text(if (bgUniversal == null) "Select" else "Change") }
                    if (bgUniversal != null) IconButton(onClick = { viewModel.saveSetting("BG_UNIVERSAL", "") }) { Icon(Icons.Default.Delete, "Clear") }
                }

                val bgDict by viewModel.bgDict.collectAsState()
                val dictLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
                    uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_DICT", it.toString()) }
                }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text("Dict Mode BG")
                    Button(onClick = { dictLauncher.launch(arrayOf("image/*")) }) { Text(if (bgDict == null) "Select" else "Change") }
                    if (bgDict != null) IconButton(onClick = { viewModel.saveSetting("BG_DICT", "") }) { Icon(Icons.Default.Delete, "Clear") }
                }

                val bgCompare by viewModel.bgCompare.collectAsState()
                val compareLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
                    uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_COMPARE", it.toString()) }
                }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text("Compare Mode BG")
                    Button(onClick = { compareLauncher.launch(arrayOf("image/*")) }) { Text(if (bgCompare == null) "Select" else "Change") }
                    if (bgCompare != null) IconButton(onClick = { viewModel.saveSetting("BG_COMPARE", "") }) { Icon(Icons.Default.Delete, "Clear") }
                }

                val bgTranslate by viewModel.bgTranslate.collectAsState()
                val translateLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
                    uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_TRANSLATE", it.toString()) }
                }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text("Translate Mode BG")
                    Button(onClick = { translateLauncher.launch(arrayOf("image/*")) }) { Text(if (bgTranslate == null) "Select" else "Change") }
                    if (bgTranslate != null) IconButton(onClick = { viewModel.saveSetting("BG_TRANSLATE", "") }) { Icon(Icons.Default.Delete, "Clear") }
                }

                val bgExplain by viewModel.bgExplain.collectAsState()
                val explainLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
                    uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_EXPLAIN", it.toString()) }
                }
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text("Explain Mode BG")
                    Button(onClick = { explainLauncher.launch(arrayOf("image/*")) }) { Text(if (bgExplain == null) "Select" else "Change") }
                    if (bgExplain != null) IconButton(onClick = { viewModel.saveSetting("BG_EXPLAIN", "") }) { Icon(Icons.Default.Delete, "Clear") }
                }
            }
        }"""

text = text.replace(bg_old, bg_new)
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

