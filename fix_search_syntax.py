import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'r') as f:
    text = f.read()

bad_snippet = """                    IconButton(onClick = { 
                        val lastUserMsg = state.chatMessages.findLast { it.role == "assistant" }
                        if (lastUserMsg != null) viewModel.retryMessage(lastUserMsg, false, "dict")
                    }) {
                    IconButton(onClick = { isChatSearching = !isChatSearching }) {
                        Icon(Icons.Default.Search, contentDescription = "Search in Chat")
                    }
                    IconButton(onClick = {
                        val lastUserMsg = state.chatMessages.findLast { it.role == "assistant" }
                        if (lastUserMsg != null) viewModel.retryMessage(lastUserMsg, false, "dict")
                    }) {
                        Icon(Icons.Default.Refresh, contentDescription = "Restart with Current Model", tint = MaterialTheme.colorScheme.primary)
                    }"""

fixed_snippet = """                    IconButton(onClick = { isChatSearching = !isChatSearching }) {
                        Icon(Icons.Default.Search, contentDescription = "Search in Chat")
                    }
                    IconButton(onClick = {
                        val lastUserMsg = state.chatMessages.findLast { it.role == "assistant" }
                        if (lastUserMsg != null) viewModel.retryMessage(lastUserMsg, false, "dict")
                    }) {
                        Icon(Icons.Default.Refresh, contentDescription = "Restart with Current Model", tint = MaterialTheme.colorScheme.primary)
                    }"""

text = text.replace(bad_snippet, fixed_snippet)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'w') as f:
    f.write(text)
print("Fixed syntax in SearchScreen")
