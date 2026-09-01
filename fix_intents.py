import re

with open('android_app/app/src/main/AndroidManifest.xml', 'r') as f:
    text = f.read()

new_filters = """
            <intent-filter>
                <action android:name="android.intent.action.PROCESS_TEXT" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="text/plain" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.SEND" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="text/plain" />
            </intent-filter>
            <intent-filter>
                <action android:name="colordict.intent.action.SEARCH" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
"""

# Replace the single intent-filter in PopupActivity
pattern = r'<intent-filter>\s*<action android:name="android\.intent\.action\.PROCESS_TEXT"\s*/>\s*<category android:name="android\.intent\.category\.DEFAULT"\s*/>\s*<data android:mimeType="text/plain"\s*/>\s*</intent-filter>'

text = re.sub(pattern, new_filters.strip(), text)

with open('android_app/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(text)

