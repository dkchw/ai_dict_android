import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

# Replace the delete button block in ExternalDictManager
target = """                    IconButton(onClick = {
                        val newList = dicts.toMutableList().apply { removeAt(index) }
                        viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}" })
                    }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                    }"""

replacement = """                    if (index > 0) {
                        IconButton(onClick = {
                            val newList = dicts.toMutableList()
                            val temp = newList[index]
                            newList[index] = newList[index - 1]
                            newList[index - 1] = temp
                            viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}|${it.third}" })
                        }, modifier = Modifier.size(32.dp)) {
                            Icon(androidx.compose.material.icons.Icons.Default.KeyboardArrowUp, contentDescription = "Up")
                        }
                    }
                    if (index < dicts.size - 1) {
                        IconButton(onClick = {
                            val newList = dicts.toMutableList()
                            val temp = newList[index]
                            newList[index] = newList[index + 1]
                            newList[index + 1] = temp
                            viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}|${it.third}" })
                        }, modifier = Modifier.size(32.dp)) {
                            Icon(androidx.compose.material.icons.Icons.Default.KeyboardArrowDown, contentDescription = "Down")
                        }
                    }
                    IconButton(onClick = {
                        val newList = dicts.toMutableList().apply { removeAt(index) }
                        viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}|${it.third}" })
                    }, modifier = Modifier.size(32.dp)) {
                        Icon(androidx.compose.material.icons.Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                    }"""

text = text.replace(target, replacement)

# We also need to fix the case where the target was already partially modified or if it had it.third
target2 = """                    IconButton(onClick = {
                        val newList = dicts.toMutableList().apply { removeAt(index) }
                        viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}|${it.third}" })
                    }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error)
                    }"""
text = text.replace(target2, replacement)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(text)

