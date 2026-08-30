sed -i '/val quoteMode by settingsViewModel.quoteMode.collectAsState()/a \        val quoteStyleStr by settingsViewModel.quoteStyle.collectAsState()\n        val fontFamily = when(quoteStyleStr) { "Serif" -> androidx.compose.ui.text.font.FontFamily.Serif; "Sans Serif" -> androidx.compose.ui.text.font.FontFamily.SansSerif; "Monospace" -> androidx.compose.ui.text.font.FontFamily.Monospace; "Cursive" -> androidx.compose.ui.text.font.FontFamily.Cursive; else -> androidx.compose.ui.text.font.FontFamily.Default }' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt

sed -i 's/Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {/Box(modifier = Modifier.fillMaxSize().padding(bottom = 120.dp), contentAlignment = Alignment.Center) {/' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt

sed -i 's/style = MaterialTheme.typography.headlineMedium,/style = MaterialTheme.typography.headlineMedium.copy(fontFamily = fontFamily, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic),/' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt

