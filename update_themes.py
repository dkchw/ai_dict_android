import re

with open('android_app/app/src/main/res/values/themes.xml', 'r') as f:
    text = f.read()

transparent_theme = """
    <style name="Theme.AIDict.Transparent" parent="Theme.AIDict">
        <item name="android:windowIsTranslucent">true</item>
        <item name="android:windowBackground">@android:color/transparent</item>
        <item name="android:windowContentOverlay">@null</item>
        <item name="android:windowNoTitle">true</item>
        <item name="android:windowIsFloating">false</item>
        <item name="android:backgroundDimEnabled">true</item>
    </style>
"""

if 'Theme.AIDict.Transparent' not in text:
    text = text.replace('</resources>', transparent_theme + '</resources>')

with open('android_app/app/src/main/res/values/themes.xml', 'w') as f:
    f.write(text)
