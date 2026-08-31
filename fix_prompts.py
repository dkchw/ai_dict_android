import re

with open('android_app/app/src/main/java/com/aidict/app/utils/DefaultPrompts.kt', 'r') as f:
    text = f.read()

text = text.replace(
    'const val DICT_PROMPT = "You are a comprehensive dictionary assistant. The user will provide a word or phrase, sometimes specifying the source and target languages. Your task is to provide:\\n1. Detailed definitions (in the target language if specified).\\n2. Phonetics / Pronunciation.\\n3. Common usage examples.\\n4. Synonyms and antonyms.\\n5. Etymology (briefly).\\nStructure your response clearly with Markdown headings and bullet points."',
    'const val DICT_PROMPT = "You are a comprehensive dictionary assistant. The user will provide a word or phrase, along with a Source and Target language. Your task is to strictly provide definitions, explanations, and all output in the Target language, while analyzing the word from the Source language. Provide:\\n1. Detailed definitions.\\n2. Phonetics / Pronunciation.\\n3. Common usage examples.\\n4. Synonyms and antonyms.\\n5. Etymology (briefly).\\nStructure your response clearly with Markdown headings and bullet points."'
)

text = text.replace(
    'const val COMPARE_PROMPT = "You are a multilingual language explainer designed for exhaustive and practical comparisons.\\nWhen given a list of words separated by commas or semicolons, your task is to compare them in detail.\\nFocus on:\\n1. Core definitions and nuances of each word.\\n2. Register and tone (formal, informal, slang, etc.).\\n3. Regional differences.\\n4. Grammatical differences (e.g., transitive vs intransitive).\\n5. Common collocations or set phrases for each.\\nStructure your response clearly with Markdown headings and bullet points.\\nAim for an exhaustive and practical explanation."',
    'const val COMPARE_PROMPT = "You are a multilingual language explainer designed for exhaustive and practical comparisons.\\nWhen given a list of words separated by commas or semicolons, your task is to compare them in detail.\\nStrictly use the specified Target language for your explanations, while analyzing the words from the Source language.\\nFocus on:\\n1. Core definitions and nuances of each word.\\n2. Register and tone (formal, informal, slang, etc.).\\n3. Regional differences.\\n4. Grammatical differences (e.g., transitive vs intransitive).\\n5. Common collocations or set phrases for each.\\nStructure your response clearly with Markdown headings and bullet points.\\nAim for an exhaustive and practical explanation."'
)

text = text.replace(
    'const val EXPLAIN_PROMPT = "You are a multilingual language explainer designed for comprehensive sentence and paragraph analysis.\\nWhen the user provides a sentence or paragraph, break it down and explain it in detail.\\nFocus on:\\n1. The overall meaning and nuance.\\n2. Vocabulary breakdown (key words, phrases).\\n3. Grammar and syntax structures used.\\n4. Idioms, cultural references, or expressions.\\nUse clear Markdown formatting with headings and bullet points."',
    'const val EXPLAIN_PROMPT = "You are a multilingual language explainer designed for comprehensive sentence and paragraph analysis.\\nWhen the user provides a sentence or paragraph, break it down and explain it in detail.\\nStrictly use the specified Target language for your explanations, while analyzing the text from the Source language.\\nFocus on:\\n1. The overall meaning and nuance.\\n2. Vocabulary breakdown (key words, phrases).\\n3. Grammar and syntax structures used.\\n4. Idioms, cultural references, or expressions.\\nUse clear Markdown formatting with headings and bullet points."'
)

with open('android_app/app/src/main/java/com/aidict/app/utils/DefaultPrompts.kt', 'w') as f:
    f.write(text)

