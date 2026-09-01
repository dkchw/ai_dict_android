import re

# 1. Fix PopupActivity stretching by remembering dimensions per orientation
def fix_popup():
    with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
        text = f.read()
    
    target = """                        val config = androidx.compose.ui.platform.LocalConfiguration.current
                        val screenHeight = config.screenHeightDp.dp
                        val screenWidth = config.screenWidthDp.dp"""
                        
    replacement = """                        val config = androidx.compose.ui.platform.LocalConfiguration.current
                        val orientation = config.orientation
                        val screenHeight = androidx.compose.runtime.remember(orientation) { config.screenHeightDp.dp }
                        val screenWidth = androidx.compose.runtime.remember(orientation) { config.screenWidthDp.dp }"""
                        
    if target in text:
        text = text.replace(target, replacement)
        with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
            f.write(text)
        print("Fixed PopupActivity")
    else:
        print("PopupActivity target not found")

# 2. Fix SettingsScreen AnimatedVisibility bug in LazyColumn
def fix_settings():
    with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
        text = f.read()
        
    target = """            androidx.compose.animation.AnimatedVisibility(visible = expanded) {
                Column(modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, bottom = 16.dp)) {
                    content()
                }
            }"""
            
    replacement = """            if (expanded) {
                Column(modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, bottom = 16.dp)) {
                    content()
                }
            }"""
            
    if target in text:
        text = text.replace(target, replacement)
        with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
            f.write(text)
        print("Fixed SettingsScreen")
    else:
        print("SettingsScreen target not found")

fix_popup()
fix_settings()

