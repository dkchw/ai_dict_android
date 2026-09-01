import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Replace the state variables and nested scroll connection
target_conn = """        var leftOverscroll by remember { mutableFloatStateOf(0f) }
        val leftThreshold = 250f
        val haptic = androidx.compose.ui.platform.LocalHapticFeedback.current
        val context = androidx.compose.ui.platform.LocalContext.current
        
        val leftOverscrollConnection = remember(pagerState.currentPage) {
            object : NestedScrollConnection {
                var toggled = false
                
                override fun onPreScroll(available: Offset, source: NestedScrollSource): Offset {
                    if (pagerState.currentPage == 0) {
                        if (leftOverscroll > 0f && available.x < 0f) {
                            // Shrinking the overscroll
                            val consumedX = minOf(-available.x, leftOverscroll)
                            leftOverscroll -= consumedX
                            return Offset(-consumedX, 0f)
                        } else if (available.x > 0f) {
                            // Growing the overscroll
                            leftOverscroll += available.x * 0.5f // friction
                            
                            if (leftOverscroll > leftThreshold && !toggled) {
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
                    leftOverscroll = 0f
                    toggled = false
                    return Velocity.Zero
                }
                
                override suspend fun onPostFling(consumed: Velocity, available: Velocity): Velocity {
                    leftOverscroll = 0f
                    toggled = false
                    return Velocity.Zero
                }
            }
        }"""

new_conn = """        val coroutineScope = rememberCoroutineScope()
        val leftOverscrollAnim = remember { androidx.compose.animation.core.Animatable(0f) }
        val leftOverscroll = leftOverscrollAnim.value
        val leftThreshold = 250f
        val haptic = androidx.compose.ui.platform.LocalHapticFeedback.current
        val context = androidx.compose.ui.platform.LocalContext.current
        
        val leftOverscrollConnection = remember(pagerState) {
            object : NestedScrollConnection {
                var toggled = false
                
                override fun onPreScroll(available: Offset, source: NestedScrollSource): Offset {
                    // Only intercept if we are on the first page AND not already scrolled towards the second page!
                    if (pagerState.currentPage == 0 && pagerState.currentPageOffsetFraction <= 0.01f) {
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
text = text.replace(target_conn, new_conn)

# 3. Replace Modifier.offset with Modifier.graphicsLayer
target_pager = """                        androidx.compose.foundation.pager.HorizontalPager(
                            state = pagerState,
                            modifier = Modifier.fillMaxSize().offset(x = (leftOverscroll * 0.3f).dp),"""
new_pager = """                        androidx.compose.foundation.pager.HorizontalPager(
                            state = pagerState,
                            modifier = Modifier.fillMaxSize().graphicsLayer { translationX = leftOverscroll * 0.3f },"""
text = text.replace(target_pager, new_pager)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Patched AppNavigation.kt with graphicsLayer and Animatable")
