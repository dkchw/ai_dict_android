import re

with open('android_app/app/src/main/java/com/aidict/app/FloatingBubbleService.kt', 'r') as f:
    text = f.read()

coroutine_block = """        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            val db = com.aidict.app.data.AppDatabase.getDatabase(this@FloatingBubbleService)
            val sizeStr = db.appDao().getSetting("BUBBLE_SIZE")?.value ?: "160"
            val size = sizeStr.toIntOrNull() ?: 160
            kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                params.width = size
                params.height = size
                windowManager.updateViewLayout(bubbleView, params)
            }
        }"""

text = text.replace(coroutine_block, "")

# Find windowManager.addView(bubbleView, params)
text = text.replace('windowManager.addView(bubbleView, params)\n    }', 'windowManager.addView(bubbleView, params)\n\n' + coroutine_block + '\n    }')

with open('android_app/app/src/main/java/com/aidict/app/FloatingBubbleService.kt', 'w') as f:
    f.write(text)
