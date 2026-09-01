import re

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
    text = f.read()

# Replace the hardcoded Surface modifier with one that reads from settings
target_surface = """                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = MaterialTheme.colorScheme.background,
                            modifier = Modifier
                                .fillMaxWidth(0.95f)
                                .fillMaxHeight(0.9f)
                                .clickable(
                                    interactionSource = remember { MutableInteractionSource() },
                                    indication = null
                                ) {
                                    // Do nothing on internal clicks
                                }
                                .clip(RoundedCornerShape(16.dp))
                        ) {"""

replacement_surface = """                        val isTablet = windowSizeClass.widthSizeClass == androidx.compose.material3.windowsizeclass.WindowWidthSizeClass.Expanded || windowSizeClass.widthSizeClass == androidx.compose.material3.windowsizeclass.WindowWidthSizeClass.Medium
                        val defaultWidth = if (isTablet) 0.6f else 0.95f
                        val defaultHeight = if (isTablet) 0.8f else 0.9f
                        
                        val popupWidthStr by settingsViewModel.getSettingFlow("POPUP_WIDTH", defaultWidth.toString()).collectAsState()
                        val popupHeightStr by settingsViewModel.getSettingFlow("POPUP_HEIGHT", defaultHeight.toString()).collectAsState()
                        
                        val popupWidth = popupWidthStr.toFloatOrNull()?.coerceIn(0.3f, 1.0f) ?: defaultWidth
                        val popupHeight = popupHeightStr.toFloatOrNull()?.coerceIn(0.3f, 1.0f) ?: defaultHeight

                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = MaterialTheme.colorScheme.background,
                            modifier = Modifier
                                .fillMaxWidth(popupWidth)
                                .fillMaxHeight(popupHeight)
                                .clickable(
                                    interactionSource = remember { MutableInteractionSource() },
                                    indication = null
                                ) {
                                    // Do nothing on internal clicks
                                }
                                .clip(RoundedCornerShape(16.dp))
                        ) {"""

if 'popupWidthStr' not in text:
    text = text.replace(target_surface, replacement_surface)
    with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
        f.write(text)

