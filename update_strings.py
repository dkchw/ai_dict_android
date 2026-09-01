import re

with open('android_app/app/src/main/res/values/strings.xml', 'r') as f:
    text = f.read()

if 'ask_ai_dict' not in text:
    text = text.replace('</resources>', '    <string name="ask_ai_dict">Ask AI Dict</string>\n</resources>')

with open('android_app/app/src/main/res/values/strings.xml', 'w') as f:
    f.write(text)

with open('android_app/app/src/main/AndroidManifest.xml', 'r') as f:
    text = f.read()

text = text.replace('android:label="Ask AI Dict"', 'android:label="@string/ask_ai_dict"')

with open('android_app/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(text)

