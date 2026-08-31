import re
import os

screens = [
    'android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt',
    'android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt'
]

for file_path in screens:
    with open(file_path, 'r') as f:
        text = f.read()
    
    # Add imports
    if 'import androidx.compose.foundation.gestures.Orientation' not in text:
        text = text.replace('import androidx.compose.foundation.layout.*', 'import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.gestures.Orientation\nimport androidx.compose.foundation.gestures.scrollable\nimport androidx.compose.foundation.rememberScrollState')
    
    # Update Column
    if 'Column(modifier = modifier.fillMaxSize().padding(16.dp)) {' in text:
        text = text.replace(
            'Column(modifier = modifier.fillMaxSize().padding(16.dp)) {',
            'Column(modifier = modifier.fillMaxSize().scrollable(rememberScrollState(), Orientation.Vertical).padding(16.dp)) {'
        )
    
    with open(file_path, 'w') as f:
        f.write(text)

