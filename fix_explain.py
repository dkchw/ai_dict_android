import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'r') as f:
    text = f.read()

# Remove scrollable from ExplainScreen
text = text.replace('.scrollable(rememberScrollState(), Orientation.Vertical)', '')

# Add fillParentMaxSize to ExplainScreen
old_lazy = """                androidx.compose.foundation.lazy.LazyColumn(modifier = Modifier.fillMaxSize()) {
                    item { Text(text = state.currentStream) }"""

new_lazy = """                androidx.compose.foundation.lazy.LazyColumn(modifier = Modifier.fillMaxSize()) {
                    if (state.chatMessages.isEmpty()) {
                        item { Spacer(modifier = Modifier.fillParentMaxSize()) }
                    }
                    item { Text(text = state.currentStream) }"""
                    
text = text.replace(old_lazy, new_lazy)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'w') as f:
    f.write(text)

