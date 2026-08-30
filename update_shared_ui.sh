cat << 'INNER_EOF' >> android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt

val LANGUAGE_CODES = mapOf(
    "Auto Detect" to "🤖 Auto",
    "English" to "🇬🇧 EN",
    "Vietnamese" to "🇻🇳 VI",
    "French" to "🇫🇷 FR",
    "Spanish" to "🇪🇸 ES",
    "German" to "🇩🇪 DE",
    "Japanese" to "🇯🇵 JA",
    "Chinese" to "🇨🇳 ZH",
    "Korean" to "🇰🇷 KO",
    "Russian" to "🇷🇺 RU",
    "Italian" to "🇮🇹 IT",
    "Portuguese" to "🇵🇹 PT",
    "Dutch" to "🇳🇱 NL",
    "Arabic" to "🇸🇦 AR"
)

@Composable
fun SmallLanguageSelector(
    currentValue: String,
    onSelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var expanded by remember { mutableStateOf(false) }
    Box(modifier = modifier) {
        TextButton(
            onClick = { expanded = true },
            contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)
        ) {
            val display = LANGUAGE_CODES[currentValue] ?: currentValue.take(4)
            Text(display, style = MaterialTheme.typography.labelLarge)
            Icon(Icons.Default.ArrowDropDown, contentDescription = null, modifier = Modifier.size(16.dp))
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            SUPPORTED_LANGUAGES.forEach { lang ->
                DropdownMenuItem(
                    text = { Text("${LANGUAGE_CODES[lang] ?: ""} $lang") },
                    onClick = {
                        onSelected(lang)
                        expanded = false
                    }
                )
            }
        }
    }
}
INNER_EOF
