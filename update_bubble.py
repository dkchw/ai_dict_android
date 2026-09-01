import re

with open('android_app/app/src/main/java/com/aidict/app/FloatingBubbleService.kt', 'r') as f:
    text = f.read()

target = """        bubbleView = ImageView(this).apply {
            setImageResource(R.mipmap.app_icon_round)
            layoutParams = android.view.ViewGroup.LayoutParams(160, 160)
            setPadding(16, 16, 16, 16)
        }"""

replacement = """        bubbleView = ImageView(this).apply {
            setImageResource(R.mipmap.app_icon_round)
            layoutParams = android.view.ViewGroup.LayoutParams(160, 160)
            setPadding(16, 16, 16, 16)
        }
        
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            val db = com.aidict.app.data.AppDatabase.getDatabase(this@FloatingBubbleService)
            val sizeStr = db.appDao().getSettingById("BUBBLE_SIZE")?.value ?: "160"
            val size = sizeStr.toIntOrNull() ?: 160
            kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                bubbleView.layoutParams = android.view.ViewGroup.LayoutParams(size, size)
                windowManager.updateViewLayout(bubbleView, params)
            }
        }"""

if 'CoroutineScope' not in text:
    text = text.replace(target, replacement)
    text = text.replace('import android.widget.Toast', 'import android.widget.Toast\nimport kotlinx.coroutines.launch')
    with open('android_app/app/src/main/java/com/aidict/app/FloatingBubbleService.kt', 'w') as f:
        f.write(text)
