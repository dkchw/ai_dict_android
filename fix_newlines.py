with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'r') as f:
    text = f.read()

text = text.replace('Word/Phrase: ${word.term}\nSource language: $src\nTarget language: $tgt', 'Word/Phrase: ${word.term}\\nSource language: $src\\nTarget language: $tgt')
text = text.replace('Source language: $src\nTarget language: $tgt\nConcept: ${word.term}', 'Source language: $src\\nTarget language: $tgt\\nConcept: ${word.term}')
text = text.replace('Please explain this sentence/paragraph:\n${word.term}', 'Please explain this sentence/paragraph:\\n${word.term}')
text = text.replace('Please compare the following words:\n${word.term}', 'Please compare the following words:\\n${word.term}')

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'w') as f:
    f.write(text)
