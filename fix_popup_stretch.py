import re

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
    text = f.read()

target = """                        val popupWidth = popupWidthStr.toFloatOrNull()?.coerceIn(0.3f, 1.0f) ?: defaultWidth
                        val popupHeight = popupHeightStr.toFloatOrNull()?.coerceIn(0.3f, 1.0f) ?: defaultHeight

                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = MaterialTheme.colorScheme.background,
                            modifier = Modifier
                                .fillMaxWidth(popupWidth)
                                .fillMaxHeight(popupHeight)
                                .clickable("""

replacement = """                        val popupWidth = popupWidthStr.toFloatOrNull()?.coerceIn(0.3f, 1.0f) ?: defaultWidth
                        val popupHeight = popupHeightStr.toFloatOrNull()?.coerceIn(0.3f, 1.0f) ?: defaultHeight
                        
                        val config = androidx.compose.ui.platform.LocalConfiguration.current
                        val screenHeight = config.screenHeightDp.dp
                        val screenWidth = config.screenWidthDp.dp

                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = MaterialTheme.colorScheme.background,
                            modifier = Modifier
                                .androidx.compose.foundation.layout.width(screenWidth * popupWidth)
                                .androidx.compose.foundation.layout.heightIn(max = screenHeight * popupHeight)
                                .clickable("""

text = text.replace(target, replacement)

# Change alignment to BottomCenter so it sits on the keyboard smoothly
text = text.replace(
    'contentAlignment = Alignment.Center',
    'contentAlignment = Alignment.BottomCenter'
)

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
    f.write(text)

