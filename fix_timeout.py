import re

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'r') as f:
    text = f.read()

text = text.replace("connectTimeout(60, java.util.concurrent.TimeUnit.SECONDS)", "connectTimeout(120, java.util.concurrent.TimeUnit.SECONDS)")
text = text.replace("writeTimeout(60, java.util.concurrent.TimeUnit.SECONDS)", "writeTimeout(120, java.util.concurrent.TimeUnit.SECONDS)")
text = text.replace("readTimeout(60, java.util.concurrent.TimeUnit.SECONDS)", "readTimeout(120, java.util.concurrent.TimeUnit.SECONDS)")

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'w') as f:
    f.write(text)

print("Increased OkHttpClient timeout to 120s")
