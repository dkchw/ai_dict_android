import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'r') as f:
    text = f.read()

text = text.replace('val comparePrompt = getSettingFlow("COMPARE_PROMPT", DefaultPrompts.COMPARE_PROMPT)', 'val comparePrompt = getSettingFlow("COMPARE_PROMPT", DefaultPrompts.COMPARE_PROMPT)\n    val externalLinkTemplate = getSettingFlow("EXTERNAL_LINK", "https://dictionary.cambridge.org/dictionary/english/{word}")')

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'w') as f:
    f.write(text)

