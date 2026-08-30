import re

with open('app/src/main/java/com/aidict/app/MainActivity.kt', 'r') as f:
    text = f.read()

# 1. Add NotesViewModel to factory
factory_addition = """                    modelClass.isAssignableFrom(SettingsViewModel::class.java) -> SettingsViewModel(database, repository) as T
                    modelClass.isAssignableFrom(NotesViewModel::class.java) -> NotesViewModel(database) as T"""
text = text.replace('modelClass.isAssignableFrom(SettingsViewModel::class.java) -> SettingsViewModel(database, repository) as T', factory_addition)

# 2. Instantiate notesViewModel
vm_instantiation = """            val settingsViewModel: SettingsViewModel = viewModel(factory = factory)
            val notesViewModel: NotesViewModel = viewModel(factory = factory)"""
text = text.replace('val settingsViewModel: SettingsViewModel = viewModel(factory = factory)', vm_instantiation)

with open('app/src/main/java/com/aidict/app/MainActivity.kt', 'w') as f:
    f.write(text)

