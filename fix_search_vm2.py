import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

# Remove import
text = re.sub(r'import com\.aidict\.app\.models\.ExternalLink\n', '', text)

# Remove the block defining defaultLinks and externalLinks
pattern = r'private val defaultLinks = listOf\([\s\S]*?\}\n\s*\} else defaultLinks\n\s*\}\.stateIn\(viewModelScope, SharingStarted\.Lazily, defaultLinks\)\n'
text = re.sub(pattern, '', text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

