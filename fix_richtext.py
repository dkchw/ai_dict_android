import re

with open('android_app/app/build.gradle.kts', 'r') as f:
    text = f.read()

# Replace Mikepenz with Halilibo
text = text.replace('implementation("com.mikepenz:multiplatform-markdown-renderer-m3:0.21.0")', 
    'implementation("com.halilibo.compose-richtext:richtext-commonmark:1.0.0-alpha01")\n    implementation("com.halilibo.compose-richtext:richtext-ui-material3:1.0.0-alpha01")')
text = text.replace('implementation("com.mikepenz:multiplatform-markdown-renderer-m3:0.27.0-rc02")', '')

with open('android_app/app/build.gradle.kts', 'w') as f:
    f.write(text)

