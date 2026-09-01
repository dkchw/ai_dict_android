with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
    text = f.read()

text = text.replace("@OptIn(ExperimentalMaterial3WindowSizeClassApi::class)\n\n    override fun onStart()", "override fun onStart()")
text = text.replace("override fun onCreate(", "@OptIn(ExperimentalMaterial3WindowSizeClassApi::class)\n    override fun onCreate(")

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
    f.write(text)

print("Fixed annotation position")
