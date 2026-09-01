import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

# Add imports
if "import androidx.compose.ui.input.nestedscroll.NestedScrollConnection" not in text:
    import_target = "import androidx.compose.ui.unit.dp"
    import_replacement = "import androidx.compose.ui.unit.dp\nimport androidx.compose.ui.input.nestedscroll.NestedScrollConnection\nimport androidx.compose.ui.input.nestedscroll.NestedScrollSource\nimport androidx.compose.ui.geometry.Offset\nimport androidx.compose.ui.unit.Velocity"
    text = text.replace(import_target, import_replacement)

# Create the nested scroll connection
scroll_conn_code = """
        val leftOverscrollConnection = remember(pagerState.currentPage) {
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
        }
"""

target = "val pullRefreshState = rememberPullToRefreshState()"
text = text.replace(target, scroll_conn_code + "\n        " + target)

# Apply to the Box
target_box = "Box(modifier = Modifier.fillMaxSize().nestedScroll(pullRefreshState.nestedScrollConnection).nestedScroll(bottomOverscrollConnection)) {"
replacement_box = "Box(modifier = Modifier.fillMaxSize().nestedScroll(pullRefreshState.nestedScrollConnection).nestedScroll(bottomOverscrollConnection).nestedScroll(leftOverscrollConnection)) {"
text = text.replace(target_box, replacement_box)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

print("Patched AppNavigation.kt")
