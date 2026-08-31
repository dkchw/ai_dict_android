import re

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'r') as f:
    text = f.read()

text = text.replace('import com.aidict.app.ui.viewmodels.SettingsViewModel', 'import com.aidict.app.ui.viewmodels.SettingsViewModel\nimport com.aidict.app.ui.viewmodels.AppViewModel')
text = text.replace('modelClass.isAssignableFrom(SearchViewModel::class.java) -> SearchViewModel(repository, database) as T', 'modelClass.isAssignableFrom(SearchViewModel::class.java) -> SearchViewModel(repository, database) as T\n                    modelClass.isAssignableFrom(AppViewModel::class.java) -> AppViewModel() as T')
text = text.replace('val searchViewModel: SearchViewModel = viewModel(factory = factory)', 'val appViewModel: AppViewModel = viewModel(factory = factory)\n            val searchViewModel: SearchViewModel = viewModel(factory = factory)')
text = text.replace('AppNavigation(', 'AppNavigation(\n                        appViewModel = appViewModel,')

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'w') as f:
    f.write(text)

