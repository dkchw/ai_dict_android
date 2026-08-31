import re

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'r') as f:
    text = f.read()

# Explain
text = text.replace('fun streamExplain(text: String): Flow<String> = callbackFlow {', 'fun streamExplain(text: String, sourceLang: String, targetLang: String): Flow<String> = callbackFlow {')
text = text.replace('ChatMessageDto(role = "user", content = "Please explain this sentence/paragraph:\\n$text")', 'ChatMessageDto(role = "user", content = "Source language: $sourceLang\\nTarget language: $targetLang\\nPlease explain this sentence/paragraph:\\n$text")')

# Compare
text = text.replace('fun streamCompare(words: String): Flow<String> = callbackFlow {', 'fun streamCompare(words: String, sourceLang: String, targetLang: String): Flow<String> = callbackFlow {')
text = text.replace('ChatMessageDto(role = "user", content = "Please compare the following words:\\n$words")', 'ChatMessageDto(role = "user", content = "Source language: $sourceLang\\nTarget language: $targetLang\\nPlease compare the following words:\\n$words")')

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'w') as f:
    f.write(text)

