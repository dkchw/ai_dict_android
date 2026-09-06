import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

# Add suggestions to ChatInputBar parameters
params_target = """fun ChatInputBar(
    availableLanguages: List<String> = emptyList(),
    inputTerm: String,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit,
    isLoading: Boolean,
    placeholder: String = "Type a word...",
    isFollowUp: Boolean = false,
    sourceLang: String? = null,
    targetLang: String? = null,
    onSourceLangChange: ((String) -> Unit)? = null,
    onTargetLangChange: ((String) -> Unit)? = null,
    onClear: (() -> Unit)? = null,
    autoNewSearch: Boolean = false,
    onToggleAutoNewSearch: (() -> Unit)? = null,
    enterToSend: Boolean = false,
    modifier: Modifier = Modifier
) {"""

params_replacement = """fun ChatInputBar(
    availableLanguages: List<String> = emptyList(),
    inputTerm: String,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit,
    isLoading: Boolean,
    placeholder: String = "Type a word...",
    isFollowUp: Boolean = false,
    sourceLang: String? = null,
    targetLang: String? = null,
    onSourceLangChange: ((String) -> Unit)? = null,
    onTargetLangChange: ((String) -> Unit)? = null,
    onClear: (() -> Unit)? = null,
    autoNewSearch: Boolean = false,
    onToggleAutoNewSearch: (() -> Unit)? = null,
    enterToSend: Boolean = false,
    suggestions: List<com.aidict.app.data.entities.Word> = emptyList(),
    onSuggestionClick: ((com.aidict.app.data.entities.Word) -> Unit)? = null,
    modifier: Modifier = Modifier
) {"""

text = text.replace(params_target, params_replacement)

# Add suggestions UI before the input Row
ui_target = """            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.Bottom
            ) {"""

ui_replacement = """            if (suggestions.isNotEmpty() && onSuggestionClick != null) {
                androidx.compose.foundation.lazy.LazyColumn(
                    modifier = Modifier.fillMaxWidth().heightIn(max = 120.dp).padding(horizontal = 8.dp, vertical = 4.dp),
                    reverseLayout = true
                ) {
                    items(suggestions) { word ->
                        Text(
                            text = word.term,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { onSuggestionClick(word) }
                                .padding(vertical = 8.dp, horizontal = 4.dp)
                        )
                    }
                }
                HorizontalDivider(modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp))
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.Bottom
            ) {"""

text = text.replace(ui_target, ui_replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

print("Updated ChatInputBar in SharedUI.kt")
