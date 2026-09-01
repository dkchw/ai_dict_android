import re
import os

files_modes = {
    'SearchScreen.kt': '"dict"',
    'CompareScreen.kt': '"compare"',
    'TranslateScreen.kt': '"translate"',
    'ExplainScreen.kt': '"explain"'
}

for file_name, mode_str in files_modes.items():
    path = f'android_app/app/src/main/java/com/aidict/app/ui/screens/{file_name}'
    with open(path, 'r') as f:
        text = f.read()
    
    # We will insert the buttons right BEFORE the delete button in the Action Bar.
    # The delete button looks like:
    # IconButton(onClick = { viewModel.deleteCurrentWord(...) })
    
    # First, let's make sure we have the Refresh and Autorenew icons imported
    if "import androidx.compose.material.icons.filled.Refresh" not in text:
        text = text.replace("import androidx.compose.material.icons.filled.Delete", "import androidx.compose.material.icons.filled.Delete\nimport androidx.compose.material.icons.filled.Refresh")
    if "import androidx.compose.material.icons.filled.Autorenew" not in text:
        text = text.replace("import androidx.compose.material.icons.filled.Delete", "import androidx.compose.material.icons.filled.Delete\nimport androidx.compose.material.icons.filled.Autorenew")
    
    restart_buttons = f"""                    IconButton(onClick = {{ 
                        val lastUserMsg = state.chatMessages.findLast {{ it.role == "user" }}
                        if (lastUserMsg != null) viewModel.retryMessage(lastUserMsg, false, {mode_str})
                    }}) {{
                        Icon(Icons.Default.Refresh, contentDescription = "Restart with Current Model", tint = MaterialTheme.colorScheme.primary)
                    }}
                    
                    IconButton(onClick = {{ 
                        val lastUserMsg = state.chatMessages.findLast {{ it.role == "user" }}
                        if (lastUserMsg != null) viewModel.retryMessage(lastUserMsg, true, {mode_str})
                    }}) {{
                        Icon(Icons.Default.Autorenew, contentDescription = "Restart with Fallback Model", tint = MaterialTheme.colorScheme.error)
                    }}
                    
                    IconButton"""
                    
    text = re.sub(r'                    IconButton\(onClick = \{ viewModel\.deleteCurrentWord.*?\}', restart_buttons, text, count=1)
    
    with open(path, 'w') as f:
        f.write(text)

print("Added top buttons to all normal chat screens")
