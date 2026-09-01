import re

with open('android_app/app/src/main/AndroidManifest.xml', 'r') as f:
    text = f.read()

text = text.replace('<data android:mimeType="text/plain" />', '<data android:mimeType="text/plain" />\n                <data android:mimeType="text/*" />')

with open('android_app/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(text)

