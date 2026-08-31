with open('android_app/app/src/main/AndroidManifest.xml', 'r') as f:
    text = f.read()

permissions = """    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />
    <uses-permission android:name="android.permission.INTERNET" />"""
text = text.replace('    <uses-permission android:name="android.permission.INTERNET" />', permissions)

provider = """        </activity>
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.provider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/provider_paths" />
        </provider>
    </application>"""
text = text.replace('        </activity>\n    </application>', provider)

with open('android_app/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(text)
