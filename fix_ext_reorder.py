import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    text = f.read()

target = """                    IconButton(onClick = {
                        val newList = dicts.toMutableList().apply { removeAt(index) }
                        viewModel.saveSetting("EXTERNAL_DICTS", newList.joinToString(",") { "${it.first}|${it.second}|${it.third}" })
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

if "KeyboardArrowUp" not in target and "KeyboardArrowUp" not in text.split("SettingsGroup(\"External Dictionaries\")")[1]:
    text = text.replace(target, replacement)
    with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
        f.write(text)

