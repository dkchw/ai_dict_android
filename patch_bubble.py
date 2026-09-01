import re

with open('android_app/app/src/main/java/com/aidict/app/FloatingBubbleService.kt', 'r') as f:
    text = f.read()

target = """                        if (xDiff < 20 && yDiff < 20) {
                            val intent = Intent(this@FloatingBubbleService, PopupActivity::class.java).apply {
                                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)
                            }
                            startActivity(intent)
                        } else {"""

replacement = """                        if (xDiff < 20 && yDiff < 20) {
                            if (PopupActivity.isVisible) {
                                val intent = Intent(this@FloatingBubbleService, PopupActivity::class.java).apply {
                                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
                                    action = "CLOSE_POPUP"
                                }
                                startActivity(intent)
                            } else {
                                val intent = Intent(this@FloatingBubbleService, PopupActivity::class.java).apply {
                                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)
                                }
                                startActivity(intent)
                            }
                        } else {"""

text = text.replace(target, replacement)

with open('android_app/app/src/main/java/com/aidict/app/FloatingBubbleService.kt', 'w') as f:
    f.write(text)

print("Patched FloatingBubbleService.kt")
