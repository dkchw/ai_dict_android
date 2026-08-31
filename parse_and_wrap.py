import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()


# 1. App Behavior
# Starts at `item { Text("App Behavior"`
# Ends before `item { Text("Display & Scaling"`
patt_app = r'item \{ Text\("App Behavior", style = MaterialTheme\.typography\.titleLarge\) \}\s*item \{\s*val autoNewSearchStr.*?\)\s*\}\s*Spacer\(modifier = Modifier\.height\(16\.dp\)\)\s*\}'
def repl_app(m):
    inner = m.group(0).replace('item { Text("App Behavior", style = MaterialTheme.typography.titleLarge) }', '').strip()
    # strip `item {` and `}` wrapper
    inner = re.sub(r'^item\s*\{', '', inner).strip()
    inner = inner.rsplit('}', 1)[0].strip()
    return f'item {{\n            SettingsGroup("App Behavior") {{\n                {inner}\n            }}\n        }}'

text = re.sub(patt_app, repl_app, text, flags=re.DOTALL)


# 2. Display & Scaling
patt_disp = r'item \{ Text\("Display & Scaling", style = MaterialTheme\.typography\.titleLarge\) \}\s*item \{\s*val uiScaleStr.*?item \{ Spacer\(modifier = Modifier\.height\(16\.dp\)\) \}'
def repl_disp(m):
    original = m.group(0)
    lines = original.split('\n')
    inner = []
    for line in lines:
        if 'item { Text("Display & Scaling"' in line or 'item { Spacer' in line:
            continue
        if 'item {' in line or re.match(r'^\s*\}\s*$', line):
            continue
        inner.append(line)
    
    return 'item {\n            SettingsGroup("Display & Scaling") {\n' + '\n'.join(inner) + '\n            }\n        }'

text = re.sub(patt_disp, repl_disp, text, flags=re.DOTALL)

# 4. Inspirational Quote
patt_quote = r'item \{ Text\("Inspirational Quote", style = MaterialTheme\.typography\.titleLarge\) \}\s*item \{\s*val quote by viewModel.*?item \{ Spacer\(Modifier\.height\(16\.dp\)\) \}'
def repl_quote(m):
    original = m.group(0)
    lines = original.split('\n')
    inner = []
    in_item = False
    for line in lines:
        if 'item { Text("Inspirational Quote"' in line or 'item { Spacer' in line:
            continue
        if line.strip() == 'item {':
            in_item = True
            continue
        if in_item and line.strip() == '}':
            in_item = False
            continue
        inner.append(line)
    
    return 'item {\n            SettingsGroup("Inspirational Quote") {\n' + '\n'.join(inner) + '\n            }\n        }'
    
text = re.sub(patt_quote, repl_quote, text, flags=re.DOTALL)

# 5. General
patt_gen = r'item \{ Text\("General", style = MaterialTheme\.typography\.titleLarge\) \}\s*item \{\s*Row\(modifier = Modifier\.fillMaxWidth\(\).*?item \{ com\.aidict\.app\.ui\.components\.MultiSelectSearchableDropdown.*?\)\s*\}'
def repl_gen(m):
    original = m.group(0)
    lines = original.split('\n')
    inner = []
    for line in lines:
        if 'item { Text("General"' in line or 'item { Spacer' in line:
            continue
        # For general, we can just replace `item {` and `}` that are at indentation 8.
        if line == '        item {':
            continue
        if line == '        }':
            continue
        # Also fix the MultiSelect line wrapper
        if line.startswith('        item { com.aidict'):
            inner.append(line.replace('item { com.aidict', 'com.aidict').rstrip('}'))
            continue
        inner.append(line)
        
    return 'item {\n            SettingsGroup("General") {\n' + '\n'.join(inner) + '\n            }\n        }'

text = re.sub(patt_gen, repl_gen, text, flags=re.DOTALL)


# 6. API Configuration
patt_api = r'item \{ Text\("API Configuration", style = MaterialTheme\.typography\.titleLarge\) \}\s*item \{\s*var passwordVisible.*?item \{ Spacer\(Modifier\.height\(16\.dp\)\) \}'
def repl_api(m):
    original = m.group(0)
    lines = original.split('\n')
    inner = []
    for line in lines:
        if 'item { Text("API Configuration"' in line or 'item { Spacer' in line:
            continue
        if line == '        item {':
            continue
        if line == '        }':
            continue
        inner.append(line)
    
    return 'item {\n            SettingsGroup("API Configuration") {\n' + '\n'.join(inner) + '\n            }\n        }'
    
text = re.sub(patt_api, repl_api, text, flags=re.DOTALL)


# 7. Models
patt_models = r'item \{ Row.*?Text\("Models".*?\}\s*item \{\s*Column \{\s*SearchableModelDropdown.*?\)\s*\}\s*\}\s*\}'
def repl_models(m):
    original = m.group(0)
    # extract everything inside `item { Column { ... } }` and the button in the header
    refresh_button = re.search(r'Button.*?Text\("Refresh"\) \}', original).group(0)
    dropdowns = re.findall(r'SearchableModelDropdown\(.*?\)\s*\}', original)
    
    inner = f'Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.End) {{ {refresh_button} }}\n'
    inner += '\n                '.join(dropdowns)
    
    return f'item {{\n            SettingsGroup("Models") {{\n                {inner}\n            }}\n        }}'

text = re.sub(patt_models, repl_models, text, flags=re.DOTALL)

# 8. Prompts
patt_prompts = r'item \{ Text\("Prompts", style = MaterialTheme\.typography\.titleLarge\) \}\s*item \{\s*OutlinedTextField.*?\)\s*\}\s*\}'
def repl_prompts(m):
    original = m.group(0)
    text_fields = re.findall(r'OutlinedTextField\(.*?\)\s*\}', original, re.DOTALL)
    inner = '\n                '.join([tf.replace('\n', '') for tf in text_fields])
    return f'item {{\n            SettingsGroup("Prompts") {{\n                {inner}\n            }}\n        }}'

text = re.sub(patt_prompts, repl_prompts, text, flags=re.DOTALL)


with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

