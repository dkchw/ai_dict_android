import re

with open('android_app/app/src/main/java/com/aidict/app/FloatingBubbleService.kt', 'r') as f:
    text = f.read()

companion_code = """
    companion object {
        var isRunning = false
    }
"""

text = text.replace("class FloatingBubbleService : Service() {", "class FloatingBubbleService : Service() {" + companion_code)

text = text.replace("    override fun onCreate() {\n        super.onCreate()", "    override fun onCreate() {\n        super.onCreate()\n        isRunning = true")

text = text.replace("    override fun onDestroy() {\n        super.onDestroy()", "    override fun onDestroy() {\n        super.onDestroy()\n        isRunning = false")

with open('android_app/app/src/main/java/com/aidict/app/FloatingBubbleService.kt', 'w') as f:
    f.write(text)

print("Patched FloatingBubbleService.kt")
