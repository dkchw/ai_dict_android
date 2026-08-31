import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

text = text.replace('fun streamExplain(text: String, profileId: Int) {', 'fun streamExplain(text: String, sourceLang: String, targetLang: String, profileId: Int) {')
text = text.replace('llmRepository.streamExplain(text).collect {', 'llmRepository.streamExplain(text, sourceLang, targetLang).collect {')
text = text.replace('Word(id = wordId, profileId = profileId, term = text, mode = "explain", sessionId = "")', 'Word(id = wordId, profileId = profileId, term = text, language = "$sourceLang -> $targetLang", mode = "explain", sessionId = "")')

text = text.replace('fun streamCompare(words: String, profileId: Int) {', 'fun streamCompare(words: String, sourceLang: String, targetLang: String, profileId: Int) {')
text = text.replace('llmRepository.streamCompare(words).collect {', 'llmRepository.streamCompare(words, sourceLang, targetLang).collect {')
text = text.replace('Word(id = wordId, profileId = profileId, term = words, mode = "compare", sessionId = "")', 'Word(id = wordId, profileId = profileId, term = words, language = "$sourceLang -> $targetLang", mode = "compare", sessionId = "")')

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(text)

