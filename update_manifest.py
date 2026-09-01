import re

with open('android_app/app/src/main/AndroidManifest.xml', 'r') as f:
    text = f.read()

# Make sure taskAffinity and excludeFromRecents are there
target = """            android:name=".PopupActivity"
            android:theme="@style/Theme.AIDict.Transparent"
            android:windowSoftInputMode="adjustResize"
            android:exported="true"
            android:launchMode="singleTop"
            android:label="@string/ask_ai_dict">"""

replacement = """            android:name=".PopupActivity"
            android:theme="@style/Theme.AIDict.Transparent"
            android:windowSoftInputMode="adjustResize"
            android:exported="true"
            android:taskAffinity=".PopupTask"
            android:excludeFromRecents="true"
            android:launchMode="singleTop"
            android:label="@string/ask_ai_dict">"""

if 'android:taskAffinity=".PopupTask"' not in text:
    text = text.replace(target, replacement)

with open('android_app/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(text)

