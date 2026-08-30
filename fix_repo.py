with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'r') as f:
    text = f.read()

text = text.replace('word.language.split', 'word.language?.split')
text = text.replace('} // end when', '                else -> { }\n            }')
text = text.replace('                "compare" -> {', '                "compare" -> {\n                    val prompt = database.appDao().getSetting("COMPARE_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.COMPARE_PROMPT\n                    initialContext.add(ChatMessageDto(role = "system", content = prompt))\n                    initialContext.add(ChatMessageDto(role = "user", content = "Please compare the following words:\\n${word.term}"))\n                }\n                else -> {}')
# Wait I just need to insert else -> {} before the closing brace of when
text = text.replace('}\n        }\n        \n        val mappedMessages = initialContext', '    else -> {}\n            }\n        }\n        \n        val mappedMessages = initialContext')

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'w') as f:
    f.write(text)
