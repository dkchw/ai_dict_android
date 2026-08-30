import re

with open('app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# 1. Add Notes to Screen enum
text = text.replace('enum class Screen { MAIN, SETTINGS, HISTORY }', 'enum class Screen { MAIN, SETTINGS, HISTORY, NOTES }')

# 2. Add EditNote import
text = text.replace('import androidx.compose.material.icons.filled.Translate', 'import androidx.compose.material.icons.filled.Translate\nimport androidx.compose.material.icons.filled.EditNote')

# 3. Add NotesScreen import
text = text.replace('import com.aidict.app.ui.screens.TranslateScreen', 'import com.aidict.app.ui.screens.TranslateScreen\nimport com.aidict.app.ui.screens.NotesScreen')

# 4. Add NotesViewModel import
text = text.replace('import com.aidict.app.ui.viewmodels.TranslateViewModel', 'import com.aidict.app.ui.viewmodels.TranslateViewModel\nimport com.aidict.app.ui.viewmodels.NotesViewModel')

# 5. Add notesViewModel to AppNavigation params
text = text.replace('settingsViewModel: SettingsViewModel,', 'settingsViewModel: SettingsViewModel,\n    notesViewModel: NotesViewModel,')

# 6. Add Notes icon button next to Settings
nav_icons = """
                    if (currentScreen == Screen.MAIN) {
                        IconButton(onClick = { currentScreen = Screen.NOTES }) {
                            Icon(Icons.Default.EditNote, contentDescription = "Notes")
                        }
                        IconButton(onClick = { currentScreen = Screen.SETTINGS }) {
                            Icon(Icons.Default.Settings, contentDescription = "Settings")
                        }
                    } else {
"""
text = text.replace("""                    if (currentScreen == Screen.MAIN) {
                        IconButton(onClick = { currentScreen = Screen.SETTINGS }) {
                            Icon(Icons.Default.Settings, contentDescription = "Settings")
                        }
                    } else {""", nav_icons)

# 7. Add Screen.NOTES to when block
when_block = """
                Screen.SETTINGS -> SettingsScreen(settingsViewModel)
                Screen.NOTES -> NotesScreen(notesViewModel)
"""
text = text.replace('Screen.SETTINGS -> SettingsScreen(settingsViewModel)', when_block.strip('\n'))

with open('app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

