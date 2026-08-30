sed -i '/item { Text("General", style = MaterialTheme.typography.titleLarge) }/i \
        item { Text("Backgrounds", style = MaterialTheme.typography.titleLarge) }\n\
        item {\n\
            val bgDict by viewModel.bgDict.collectAsState()\n\
            val dictLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->\n\
                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_DICT", it.toString()) }\n\
            }\n\
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {\n\
                Text("Dict Mode BG")\n\
                Button(onClick = { dictLauncher.launch(arrayOf("image/*")) }) { Text(if (bgDict == null) "Select" else "Change") }\n\
                if (bgDict != null) IconButton(onClick = { viewModel.saveSetting("BG_DICT", "") }) { Icon(Icons.Default.Delete, "Clear") }\n\
            }\n\
        }\n\
        item {\n\
            val bgCompare by viewModel.bgCompare.collectAsState()\n\
            val compareLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->\n\
                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_COMPARE", it.toString()) }\n\
            }\n\
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {\n\
                Text("Compare Mode BG")\n\
                Button(onClick = { compareLauncher.launch(arrayOf("image/*")) }) { Text(if (bgCompare == null) "Select" else "Change") }\n\
                if (bgCompare != null) IconButton(onClick = { viewModel.saveSetting("BG_COMPARE", "") }) { Icon(Icons.Default.Delete, "Clear") }\n\
            }\n\
        }\n\
        item {\n\
            val bgTranslate by viewModel.bgTranslate.collectAsState()\n\
            val translateLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->\n\
                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_TRANSLATE", it.toString()) }\n\
            }\n\
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {\n\
                Text("Translate Mode BG")\n\
                Button(onClick = { translateLauncher.launch(arrayOf("image/*")) }) { Text(if (bgTranslate == null) "Select" else "Change") }\n\
                if (bgTranslate != null) IconButton(onClick = { viewModel.saveSetting("BG_TRANSLATE", "") }) { Icon(Icons.Default.Delete, "Clear") }\n\
            }\n\
        }\n\
        item {\n\
            val bgExplain by viewModel.bgExplain.collectAsState()\n\
            val explainLauncher = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->\n\
                uri?.let { context.contentResolver.takePersistableUriPermission(it, Intent.FLAG_GRANT_READ_URI_PERMISSION); viewModel.saveSetting("BG_EXPLAIN", it.toString()) }\n\
            }\n\
            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {\n\
                Text("Explain Mode BG")\n\
                Button(onClick = { explainLauncher.launch(arrayOf("image/*")) }) { Text(if (bgExplain == null) "Select" else "Change") }\n\
                if (bgExplain != null) IconButton(onClick = { viewModel.saveSetting("BG_EXPLAIN", "") }) { Icon(Icons.Default.Delete, "Clear") }\n\
            }\n\
        }\n\
        item {\n\
            val blur by viewModel.bgBlurRadius.collectAsState()\n\
            Column(modifier = Modifier.padding(vertical = 8.dp)) {\n\
                Text("Background Blur Radius: ${blur.toInt()} dp")\n\
                Slider(value = blur, onValueChange = { viewModel.saveSetting("BG_BLUR_RADIUS", it.toString()) }, valueRange = 0f..50f)\n\
            }\n\
        }\n\
        item {\n\
            val opacity by viewModel.bgOpacity.collectAsState()\n\
            Column(modifier = Modifier.padding(vertical = 8.dp)) {\n\
                Text("Background Opacity: ${(opacity * 100).toInt()}%")\n\
                Slider(value = opacity, onValueChange = { viewModel.saveSetting("BG_OPACITY", it.toString()) }, valueRange = 0f..1f)\n\
            }\n\
        }\n\
        item { Text("Inspirational Quote", style = MaterialTheme.typography.titleLarge) }\n\
        item {\n\
            val quote by viewModel.quoteMode.collectAsState()\n\
            val quotes = listOf("None", "Shuffle", "Per studium ad sapientiam", "Labor omnia vincit", "Assiduitas mater scientiae", "Nulla dies sine linea", "Carpe diem", "Vincit qui se vincit")\n\
            com.aidict.app.ui.components.SearchableDropdown(\n\
                label = "Display Quote on Empty Screens",\n\
                currentValue = quote,\n\
                options = quotes,\n\
                onSelected = { viewModel.saveSetting("QUOTE_MODE", it) }\n\
            )\n\
        }\n\
        item { Spacer(Modifier.height(16.dp)) }\n' android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt
