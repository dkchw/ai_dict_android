import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'r') as f:
    text = f.read()

settings_start = """    val explainModel = getSettingFlow("EXPLAIN_MODEL", "inclusionai/ling-3.0-flash")
    val translateModel = getSettingFlow("TRANSLATE_MODEL", "inclusionai/ling-3.0-flash")"""

settings_new = """    val explainModel = getSettingFlow("EXPLAIN_MODEL", "inclusionai/ling-3.0-flash")
    val translateModel = getSettingFlow("TRANSLATE_MODEL", "inclusionai/ling-3.0-flash")
    
    val autoNewSearch = getSettingFlow("AUTO_NEW_SEARCH", "false")
    val enterToSend = getSettingFlow("ENTER_TO_SEND", "false")"""

text = text.replace(settings_start, settings_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt', 'w') as f:
    f.write(text)

