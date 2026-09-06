import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

target = """fun ChatInputBar(
    availableLanguages: List<String> = com.aidict.app.utils.LanguageManager.defaultLanguages,

    inputTerm: String,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit,
    isLoading: Boolean,
    placeholder: String,
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
)"""

replacement = """fun ChatInputBar(
    availableLanguages: List<String> = com.aidict.app.utils.LanguageManager.defaultLanguages,
    inputTerm: String,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit,
    isLoading: Boolean,
    placeholder: String,
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
)"""

text = text.replace(target, replacement)

# We also need to fix `clickable` unresolved reference in SharedUI.kt
if "import androidx.compose.foundation.clickable" not in text:
    text = text.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.clickable")

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)
print("Updated signature")
