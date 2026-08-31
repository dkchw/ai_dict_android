import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'r') as f:
    text = f.read()

# Remove ExternalLink import
text = re.sub(r'import com\.aidict\.app\.models\.ExternalLink\n', '', text)

# Remove the block defining defaultLinks, externalLinks, and saveExternalLinks
pattern = r'private val defaultLinks = listOf\([\s\S]*?fun saveExternalLinks[\s\S]*?\}\n'
text = re.sub(pattern, '', text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'w') as f:
    f.write(text)

