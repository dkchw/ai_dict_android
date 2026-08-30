import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace('fun streamCompare(word1: String, word2: String, profileId: Int)', 'fun streamCompare(words: String, profileId: Int)')
content = content.replace('llmRepository.streamCompare(word1, word2).collect', 'llmRepository.streamCompare(words).collect')
content = content.replace('term = "$word1 vs $word2"', 'term = words')

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(content)
