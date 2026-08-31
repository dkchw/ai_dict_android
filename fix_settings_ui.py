import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Replace single external link with list
old_ui = """        item {
            OutlinedTextField(
                value = externalLinkTemplate, 
                onValueChange = { viewModel.saveSetting("EXTERNAL_LINK", it) }, 
                label = { Text("External Link Template (use {word})") }, 
                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), 
                singleLine = true
            )
        }"""
        
new_ui = """        items(externalLinks.size) { index ->
            val link = externalLinks[index]
            Card(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                Column(modifier = Modifier.padding(8.dp)) {
                    OutlinedTextField(value = link.name, onValueChange = { 
                        val newLinks = externalLinks.toMutableList()
                        newLinks[index] = link.copy(name = it)
                        viewModel.saveExternalLinks(newLinks)
                    }, label = { Text("Name") }, modifier = Modifier.fillMaxWidth())
                    
                    OutlinedTextField(value = link.url, onValueChange = { 
                        val newLinks = externalLinks.toMutableList()
                        newLinks[index] = link.copy(url = it)
                        viewModel.saveExternalLinks(newLinks)
                    }, label = { Text("URL (use {word})") }, modifier = Modifier.fillMaxWidth())
                    
                    OutlinedTextField(value = link.iconUrl, onValueChange = { 
                        val newLinks = externalLinks.toMutableList()
                        newLinks[index] = link.copy(iconUrl = it)
                        viewModel.saveExternalLinks(newLinks)
                    }, label = { Text("Icon URL (optional)") }, modifier = Modifier.fillMaxWidth())
                    
                    Button(onClick = { 
                        val newLinks = externalLinks.toMutableList()
                        newLinks.removeAt(index)
                        viewModel.saveExternalLinks(newLinks)
                    }, modifier = Modifier.align(Alignment.End).padding(top = 8.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) {
                        Text("Remove")
                    }
                }
            }
        }
        item {
            Button(onClick = {
                val newLinks = externalLinks.toMutableList()
                newLinks.add(com.aidict.app.models.ExternalLink("New Link", "https://"))
                viewModel.saveExternalLinks(newLinks)
            }, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                Text("Add External Link")
            }
        }"""

text = text.replace(old_ui, new_ui)
text = text.replace('val externalLinkTemplate by viewModel.externalLinkTemplate.collectAsState()', 'val externalLinks by viewModel.externalLinks.collectAsState()')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

