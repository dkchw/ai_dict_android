with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

# 1. Fix Language Selector Alignment
text = text.replace('horizontalArrangement = Arrangement.Start,', 'horizontalArrangement = Arrangement.Center,')

# 2. Fix Left Add Button Style
old_add_btn = """                if (onClear != null) {

                    IconButton(onClick = onClear, modifier = Modifier.padding(bottom = 8.dp)) {

                        Icon(Icons.Default.Add, contentDescription = "New Search", tint = MaterialTheme.colorScheme.primary)

                    }

                }"""

new_add_btn = """                if (onClear != null) {
                    IconButton(
                        onClick = onClear, 
                        modifier = Modifier
                            .padding(bottom = 8.dp, start = 8.dp, end = 8.dp)
                            .background(MaterialTheme.colorScheme.secondaryContainer, CircleShape)
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "New Search", tint = MaterialTheme.colorScheme.onSecondaryContainer)
                    }
                }"""

text = text.replace(old_add_btn, new_add_btn)

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)
