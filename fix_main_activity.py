import re

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'r') as f:
    text = f.read()

text = text.replace('import android.os.Bundle', 'import android.os.Bundle\nimport androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen')

old_oncreate = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)"""

new_oncreate = """    override fun onCreate(savedInstanceState: Bundle?) {
        installSplashScreen()
        super.onCreate(savedInstanceState)"""

text = text.replace(old_oncreate, new_oncreate)

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'w') as f:
    f.write(text)

