import re

with open('android_app/app/src/main/AndroidManifest.xml', 'r') as f:
    text = f.read()

popup_activity = """
        <activity
            android:name=".PopupActivity"
            android:theme="@style/Theme.AIDict.Transparent"
            android:windowSoftInputMode="adjustResize"
            android:exported="true"
            android:label="Ask AI Dict">
            <intent-filter>
                <action android:name="android.intent.action.PROCESS_TEXT" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="text/plain" />
            </intent-filter>
        </activity>
"""

if 'PopupActivity' not in text:
    text = text.replace('</application>', popup_activity + '    </application>')

with open('android_app/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(text)
