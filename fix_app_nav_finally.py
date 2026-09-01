import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# I will find the exact leftOverscrollConnection block and replace it.
# Instead of string replace, I'll use regex to match the whole connection.
pattern = re.compile(r"val leftOverscrollConnection = remember\(pagerState\.currentPage\) \{.*?return Velocity\.Zero\n\s*\}\n\s*\}\n\s*\}", re.DOTALL)

new_conn = """val coroutineScope = rememberCoroutineScope()
        val leftOverscrollAnim = remember { androidx.compose.animation.core.Animatable(0f) }
        val leftOverscroll = leftOverscrollAnim.value
        
        val leftOverscrollConnection = remember(pagerState) {
            object : NestedScrollConnection {
                var toggled = false
                
                override fun onPreScroll(available: Offset, source: NestedScrollSource): Offset {
                    if (pagerState.currentPage == 0 && kotlin.math.abs(pagerState.currentPageOffsetFraction) <= 0.05f) {
                        if (leftOverscrollAnim.value > 0f && available.x < 0f) {
                            val consumedX = minOf(-available.x, leftOverscrollAnim.value)
                            coroutineScope.launch { leftOverscrollAnim.snapTo(leftOverscrollAnim.value - consumedX) }
                            return Offset(-consumedX, 0f)
                        } else if (available.x > 0f) {
                            coroutineScope.launch { leftOverscrollAnim.snapTo(leftOverscrollAnim.value + available.x * 0.5f) }
                            
                            if (leftOverscrollAnim.value > leftThreshold && !toggled) {
                                toggled = true
                                haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress)
                                if (com.aidict.app.FloatingBubbleService.isRunning) {
                                    val intent = android.content.Intent(context, com.aidict.app.FloatingBubbleService::class.java)
                                    context.stopService(intent)
                                    android.widget.Toast.makeText(context, "Bubble Disabled", android.widget.Toast.LENGTH_SHORT).show()
                                } else {
                                    if (android.provider.Settings.canDrawOverlays(context)) {
                                        val intent = android.content.Intent(context, com.aidict.app.FloatingBubbleService::class.java)
                                        context.startService(intent)
                                        android.widget.Toast.makeText(context, "Bubble Enabled", android.widget.Toast.LENGTH_SHORT).show()
                                    } else {
                                        android.widget.Toast.makeText(context, "Overlay permission required", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                }
                            }
                            return Offset(available.x, 0f)
                        }
                    }
                    return Offset.Zero
                }

                override suspend fun onPreFling(available: Velocity): Velocity {
                    if (leftOverscrollAnim.value > 0f) {
                        coroutineScope.launch { leftOverscrollAnim.animateTo(0f) }
                        toggled = false
                    }
                    return Velocity.Zero
                }
                
                override suspend fun onPostFling(consumed: Velocity, available: Velocity): Velocity {
                    if (leftOverscrollAnim.value > 0f) {
                        coroutineScope.launch { leftOverscrollAnim.animateTo(0f) }
                        toggled = false
                    }
                    return Velocity.Zero
                }
            }
        }"""

text = pattern.sub(new_conn, text)

# Remove the old state var if it exists
text = text.replace("var leftOverscroll by remember { mutableFloatStateOf(0f) }", "")

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Applied Animatable and abs offset check")
