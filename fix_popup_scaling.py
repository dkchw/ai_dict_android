import re

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
    text = f.read()

target = """                        val config = androidx.compose.ui.platform.LocalConfiguration.current
                        val orientation = config.orientation
                        val screenHeight = androidx.compose.runtime.remember(orientation) { config.screenHeightDp.dp }
                        val screenWidth = androidx.compose.runtime.remember(orientation) { config.screenWidthDp.dp }

                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = MaterialTheme.colorScheme.background,
                            modifier = Modifier
                                .width(screenWidth * popupWidth)
                                .heightIn(max = screenHeight * popupHeight)"""
                                
replacement = """                        val config = androidx.compose.ui.platform.LocalConfiguration.current
                        val orientation = config.orientation
                        val screenHeight = androidx.compose.runtime.remember(orientation) { config.screenHeightDp.dp }

                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = MaterialTheme.colorScheme.background,
                            modifier = Modifier
                                .fillMaxWidth(popupWidth)
                                .heightIn(max = (screenHeight * popupHeight) / uiScale)"""

if target in text:
    text = text.replace(target, replacement)
    with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
        f.write(text)
    print("Fixed scaling issue in PopupActivity")
else:
    print("Target not found")
