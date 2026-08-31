import re

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'r') as f:
    text = f.read()

text = text.replace('AppViewModel() as T', 'AppViewModel(database) as T')

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'w') as f:
    f.write(text)

