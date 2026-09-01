import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# 1. Extract the Floating UI group from ExternalDictManager
floating_group_start = text.find('    SettingsGroup("Floating UI & Bubble Sizing") {')
floating_group_end = text.find('    Spacer(Modifier.height(16.dp))\n    SettingsGroup("External Dictionaries") {')

if floating_group_start != -1 and floating_group_end != -1:
    floating_group = text[floating_group_start:floating_group_end]
    
    # Remove it from its current location
    text = text[:floating_group_start] + text[floating_group_end:]
    
    # 2. Insert it back into the LazyColumn before ExternalDictManager
    lazy_column_target = "        item { ExternalDictManager(viewModel) }"
    
    # Wrap it in item { }
    wrapped_group = "        item {\n"
    for line in floating_group.split('\n'):
        if line.strip():
            wrapped_group += "    " + line + "\n"
        else:
            wrapped_group += "\n"
    wrapped_group += "        }\n"
    
    text = text.replace(lazy_column_target, wrapped_group + "\n" + lazy_column_target)
    
    with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
        f.write(text)
    print("Fixed SettingsScreen structure")
else:
    print("Could not find Floating UI group bounds")
