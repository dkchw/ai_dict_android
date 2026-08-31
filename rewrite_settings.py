import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# I will replace the headers with SettingsGroup(
# But wait, the content of SettingsGroup needs to be nested!
# It's easier to just do it via regex for each block.

# Block 1: App Behavior
text = re.sub(
    r'item \{ Text\("App Behavior"[^\n]+\n\s*item \{\s*(.*?)\s*\}\s*item \{\s*(.*?)\s*\}\s*item \{ Spacer\(modifier = Modifier\.height\(16\.dp\)\) \}',
    r'item { SettingsGroup("App Behavior") { \1 \2 } }',
    text,
    flags=re.DOTALL
)

# Block 2: Display & Scaling
text = re.sub(
    r'item \{ Text\("Display & Scaling"[^\n]+\n\s*item \{\s*(.*?)\s*\}\s*item \{\s*(.*?)\s*\}\s*item \{ Spacer\(modifier = Modifier\.height\(16\.dp\)\) \}',
    r'item { SettingsGroup("Display & Scaling") { \1 \2 } }',
    text,
    flags=re.DOTALL
)

# Block 3: Backgrounds
text = re.sub(
    r'item \{\s*Column \{\s*Text\("Backgrounds"[^\n]+\n(.*?)\}\s*\}',
    r'item { SettingsGroup("Backgrounds") { \1 } }',
    text,
    flags=re.DOTALL
)

# Block 4: Inspirational Quote
text = re.sub(
    r'item \{ Text\("Inspirational Quote"[^\n]+\n\s*item \{\s*(.*?)\s*\}\s*item \{\s*(.*?)\s*\}\s*item \{ Spacer\(modifier = Modifier\.height\(16\.dp\)\) \}',
    r'item { SettingsGroup("Inspirational Quote") { \1 \2 } }',
    text,
    flags=re.DOTALL
)

# Block 5: General
# General has multiple items...
text = re.sub(
    r'item \{ Text\("General"[^\n]+\n\s*item \{\s*(.*?)\s*\}\s*item \{\s*(.*?)\s*\}\s*item \{ Spacer\(Modifier\.height\(16\.dp\)\) \}\s*item \{\s*(.*?)\s*\}',
    r'item { SettingsGroup("General") { \1 \2 \3 } }',
    text,
    flags=re.DOTALL
)

# Block 6: API Configuration
text = re.sub(
    r'item \{ Text\("API Configuration"[^\n]+\n\s*item \{\s*(.*?)\s*\}\s*item \{ Spacer\(Modifier\.height\(16\.dp\)\) \}',
    r'item { SettingsGroup("API Configuration") { \1 } }',
    text,
    flags=re.DOTALL
)

# Block 7: Models
text = re.sub(
    r'item \{ Row[^\n]+Text\("Models"[^\n]+\n\s*item \{\s*Column \{\s*(.*?)\}\s*\}\s*item \{ Spacer\(Modifier\.height\(16\.dp\)\) \}',
    r'item { SettingsGroup("Models") { \1 } }',
    text,
    flags=re.DOTALL
)

# Block 8: Prompts
text = re.sub(
    r'item \{\s*Column \{\s*Text\("Prompts"[^\n]+\n(.*?)\}\s*\}',
    r'item { SettingsGroup("Prompts") { \1 } }',
    text,
    flags=re.DOTALL
)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

