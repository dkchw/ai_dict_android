import re

screens = {
    'SearchScreen.kt': 'dict',
    'CompareScreen.kt': 'compare',
    'TranslateScreen.kt': 'translate',
    'ExplainScreen.kt': 'explain'
}

for screen, mode in screens.items():
    path = f'android_app/app/src/main/java/com/aidict/app/ui/screens/{screen}'
    with open(path, 'r') as f:
        text = f.read()

    # Find the row of buttons
    target = f"""                                IconButton(onClick = {{ viewModel.retryMessage(msg, true, "{mode}") }}, modifier = Modifier.size(32.dp)) {{ Icon(Icons.Default.Refresh, "Regenerate", modifier = Modifier.size(16.dp)) }}"""
    
    replacement = f"""                                IconButton(onClick = {{ viewModel.retryMessage(msg, false, "{mode}") }}, modifier = Modifier.size(32.dp)) {{ Icon(Icons.Default.Refresh, "Regenerate (Current)", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp)) }}
                                IconButton(onClick = {{ viewModel.retryMessage(msg, true, "{mode}") }}, modifier = Modifier.size(32.dp)) {{ Icon(Icons.Default.Autorenew, "Regenerate (Fallback)", tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(16.dp)) }}"""
    
    # We might have `Icons.Default.Refresh` or something else in the target depending on what it currently is.
    # Let's just use regex to find the Refresh button and replace it.
    
    # Let's inspect the target exactly
    
    text = re.sub(
        r'IconButton\(onClick = \{ viewModel\.retryMessage\(msg, (?:true|false), ".*?"\) \}, modifier = Modifier\.size\(32\.dp\)\) \{ Icon\(Icons\.Default\.Refresh, "Regenerate", modifier = Modifier\.size\(16\.dp\)\) \}',
        replacement,
        text
    )

    with open(path, 'w') as f:
        f.write(text)

print("Replaced buttons in chat screens.")
