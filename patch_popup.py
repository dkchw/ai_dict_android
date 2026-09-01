import re

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
    text = f.read()

# Add isVisible to companion object
companion_code = """
    companion object {
        var isVisible = false
    }
"""
text = text.replace("class PopupActivity : ComponentActivity() {", "class PopupActivity : ComponentActivity() {" + companion_code)

# Add onStart and onStop
lifecycle_code = """
    override fun onStart() {
        super.onStart()
        isVisible = true
    }

    override fun onStop() {
        super.onStop()
        isVisible = false
    }
    
    override fun onNewIntent(intent: android.content.Intent) {
        super.onNewIntent(intent)
        if (intent.action == "CLOSE_POPUP") {
            finish()
        }
    }
"""

text = text.replace("    override fun onCreate(", lifecycle_code + "\n    override fun onCreate(")

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
    f.write(text)

print("Patched PopupActivity.kt")
