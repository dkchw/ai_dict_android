import re

with open('android_app/app/src/main/AndroidManifest.xml', 'r') as f:
    text = f.read()

perm = '<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />'
if 'SYSTEM_ALERT_WINDOW' not in text:
    text = text.replace('<uses-permission android:name="android.permission.INTERNET" />', '<uses-permission android:name="android.permission.INTERNET" />\n    ' + perm)

srv = '<service android:name=".FloatingBubbleService" />'
if 'FloatingBubbleService' not in text:
    text = text.replace('</application>', '    ' + srv + '\n    </application>')

with open('android_app/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(text)

