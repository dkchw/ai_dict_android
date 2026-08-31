import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

old_actions = """                    if (currentScreen == Screen.MAIN) {
                        IconButton(onClick = { currentScreen = Screen.NOTES }) {"""

new_actions = """                    if (currentScreen == Screen.MAIN) {
                        androidx.compose.material3.Text(
                            text = modes[currentMode].title,
                            style = androidx.compose.material3.MaterialTheme.typography.titleMedium,
                            modifier = androidx.compose.ui.Modifier.padding(end = 8.dp).align(androidx.compose.ui.Alignment.CenterVertically),
                            color = androidx.compose.material3.MaterialTheme.colorScheme.primary.copy(alpha = 0.7f)
                        )
                        IconButton(onClick = { currentScreen = Screen.NOTES }) {"""

text = text.replace(old_actions, new_actions)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)
