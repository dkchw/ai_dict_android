import re

with open('app/src/main/java/com/aidict/app/MainActivity.kt', 'r') as f:
    text = f.read()

# import NotesViewModel
text = text.replace('import com.aidict.app.ui.viewmodels.TranslateViewModel', 'import com.aidict.app.ui.viewmodels.TranslateViewModel\nimport com.aidict.app.ui.viewmodels.NotesViewModel')

# Init NotesViewModel
text = text.replace('val settingsViewModel = ViewModelProvider(this, AppViewModelFactory(database, llmRepository))[SettingsViewModel::class.java]', 'val settingsViewModel = ViewModelProvider(this, AppViewModelFactory(database, llmRepository))[SettingsViewModel::class.java]\n        val notesViewModel = ViewModelProvider(this, AppViewModelFactory(database, llmRepository))[NotesViewModel::class.java]')

# Pass NotesViewModel to AppNavigation
text = text.replace('settingsViewModel = settingsViewModel,', 'settingsViewModel = settingsViewModel,\n                    notesViewModel = notesViewModel,')

with open('app/src/main/java/com/aidict/app/MainActivity.kt', 'w') as f:
    f.write(text)

