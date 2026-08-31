import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

bad = """                            .androidx.compose.foundation.ExperimentalFoundationApi::class.let {
                                @OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
                                Modifier.androidx.compose.foundation.combinedClickable(
                                    onClick = onClear,
                                    onLongClick = onToggleAutoNewSearch
                                )
                            }"""

good = """                            .then(
                                @OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
                                Modifier.androidx.compose.foundation.combinedClickable(
                                    onClick = onClear,
                                    onLongClick = onToggleAutoNewSearch
                                )
                            )"""

text = text.replace(bad, good)

# Also let's import Bolt
text = text.replace("import androidx.compose.material.icons.filled.Add", "import androidx.compose.material.icons.filled.Add\nimport androidx.compose.material.icons.filled.Bolt")

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

