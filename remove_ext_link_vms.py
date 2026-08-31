import re

# SearchViewModel
with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Match the externalLinks Flow definition
pattern = r'private val _externalLinks = MutableStateFlow<List<com\.aidict\.app\.models\.ExternalLink>>\(emptyList\(\)\)\n\s*val externalLinks: StateFlow<List<com\.aidict\.app\.models\.ExternalLink>> = _externalLinks\.asStateFlow\(\)\n'
text = re.sub(pattern, '', text)

# Match the load block inside init
init_pattern = r'database\.appDao\(\)\.getSettingsFlow\(\)\.collectLatest \{ settings ->\n\s*val linksJson = settings\.find \{ it\.key == "EXTERNAL_LINKS" \}\?\.value\n\s*if \(\!linksJson\.isNullOrBlank\(\)\) \{\n\s*try \{\n\s*_externalLinks\.value = kotlinx\.serialization\.json\.Json\.decodeFromString\(linksJson\)\n\s*\} catch \(e: Exception\) \{\n\s*_externalLinks\.value = emptyList\(\)\n\s*\}\n\s*\} else \{\n\s*_externalLinks\.value = emptyList\(\)\n\s*\}\n\s*\}'

text = re.sub(init_pattern, '', text)

# Cleanup any stray database.appDao().getSettingsFlow().collectLatest {} if it's empty
text = re.sub(r'viewModelScope\.launch \{\n\s*database\.appDao\(\)\.getSettingsFlow\(\)\.collectLatest \{\s*\}\n\s*\}\n', '', text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

# SettingsViewModel
with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'r') as f:
    text = f.read()

text = re.sub(pattern, '', text)
text = re.sub(init_pattern, '', text)

# Match saveExternalLinks function
save_pattern = r'fun saveExternalLinks\(links: List<com\.aidict\.app\.models\.ExternalLink>\) \{.*?\}\n'
text = re.sub(save_pattern, '', text, flags=re.DOTALL)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'w') as f:
    f.write(text)

