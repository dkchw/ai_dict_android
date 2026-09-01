import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# 1. Add state variable
state_code = """
        var leftOverscroll by remember { mutableFloatStateOf(0f) }
        val leftThreshold = 250f
        val density = androidx.compose.ui.platform.LocalDensity.current
"""

# Replace the old connection
old_conn_target = """        val leftOverscrollConnection = remember(pagerState.currentPage) {
            object : NestedScrollConnection {
                var accumulatedOverscroll = 0f
                var toggled = false
                
                override fun onPostScroll(
                    consumed: Offset,
                    available: Offset,
                    source: NestedScrollSource
                ): Offset {
                    if (pagerState.currentPage == 0 && available.x > 0) {
                        accumulatedOverscroll += available.x
                        if (accumulatedOverscroll > 150f && !toggled) {
                            toggled = true
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
                    } else if (available.x <= 0) {
                        accumulatedOverscroll = 0f
                        toggled = false
                    }
                    return Offset.Zero
                }
                
                override suspend fun onPostFling(consumed: Velocity, available: Velocity): Velocity {
                    accumulatedOverscroll = 0f
                    toggled = false
                    return Velocity.Zero
                }
            }
        }"""

new_conn_code = """
        var leftOverscroll by remember { mutableFloatStateOf(0f) }
        val leftThreshold = 250f
        val haptic = androidx.compose.ui.platform.LocalHapticFeedback.current
        
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
        }
"""
text = text.replace(old_conn_target, new_conn_code)

# 2. Add visual indicator
visual_target = """                        androidx.compose.material3.pulltorefresh.PullToRefreshContainer(
                            state = pullRefreshState,
                            modifier = Modifier.align(Alignment.TopCenter)
                        )"""

visual_replacement = """                        androidx.compose.material3.pulltorefresh.PullToRefreshContainer(
                            state = pullRefreshState,
                            modifier = Modifier.align(Alignment.TopCenter)
                        )
                        
                        // Left Edge Bubble Toggle Indicator
                        if (leftOverscroll > 0f) {
                            val progress = (leftOverscroll / leftThreshold).coerceIn(0f, 1f)
                            val iconOffset = (leftOverscroll - 50f).coerceAtMost(100f)
                            if (iconOffset > 0f) {
                                androidx.compose.foundation.layout.Box(
                                    modifier = Modifier
                                        .align(Alignment.CenterStart)
                                        .offset(x = (iconOffset - 24f).dp)
                                        .size(48.dp)
                                        .background(
                                            if (progress >= 1f) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                            shape = androidx.compose.foundation.shape.CircleShape
                                        )
                                        .padding(12.dp)
                                ) {
                                    Icon(
                                        imageVector = if (com.aidict.app.FloatingBubbleService.isRunning) androidx.compose.material.icons.Icons.Default.Close else androidx.compose.material.icons.Icons.Default.Add,
                                        contentDescription = "Toggle Bubble",
                                        tint = if (progress >= 1f) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                                        modifier = Modifier.fillMaxSize().alpha(progress)
                                    )
                                }
                            }
                        }"""
text = text.replace(visual_target, visual_replacement)

# Apply offset to pager!
pager_target = """                        androidx.compose.foundation.pager.HorizontalPager(
                            state = pagerState,
                            modifier = Modifier.fillMaxSize(),"""
pager_replacement = """                        androidx.compose.foundation.pager.HorizontalPager(
                            state = pagerState,
                            modifier = Modifier.fillMaxSize().offset(x = (leftOverscroll * 0.3f).dp),"""
text = text.replace(pager_target, pager_replacement)


with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Patched AppNavigation.kt for visual left pull")
