import re

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'r') as f:
    text = f.read()

replacement = """    fun streamChat(word: com.aidict.app.data.entities.Word, messages: List<com.aidict.app.data.entities.ChatMessage>, forceFallback: Boolean = false): Flow<String> = callbackFlow {
        val model = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("CHAT_MODEL")?.value ?: "~deepseek/deepseek-v4-flash-latest" }
        
        // Reconstruct initial context
        val initialContext = mutableListOf<ChatMessageDto>()
        runBlocking(kotlinx.coroutines.Dispatchers.IO) {
            when (word.mode) {
                "dict" -> {
                    val prompt = database.appDao().getSetting("DICT_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.DICT_PROMPT
                    initialContext.add(ChatMessageDto(role = "system", content = prompt))
                    val langs = word.language.split(" -> ")
                    val src = langs.getOrNull(0) ?: ""
                    val tgt = langs.getOrNull(1) ?: ""
                    initialContext.add(ChatMessageDto(role = "user", content = "Word/Phrase: ${word.term}\\nSource language: $src\\nTarget language: $tgt"))
                }
                "translate" -> {
                    val prompt = database.appDao().getSetting("TRANSLATE_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.TRANSLATE_PROMPT
                    initialContext.add(ChatMessageDto(role = "system", content = prompt))
                    val langs = word.language.split(" -> ")
                    val src = langs.getOrNull(0) ?: ""
                    val tgt = langs.getOrNull(1) ?: ""
                    initialContext.add(ChatMessageDto(role = "user", content = "Source language: $src\\nTarget language: $tgt\\nConcept: ${word.term}"))
                }
                "explain" -> {
                    val prompt = database.appDao().getSetting("EXPLAIN_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.EXPLAIN_PROMPT
                    initialContext.add(ChatMessageDto(role = "system", content = prompt))
                    initialContext.add(ChatMessageDto(role = "user", content = "Please explain this sentence/paragraph:\\n${word.term}"))
                }
                "compare" -> {
                    val prompt = database.appDao().getSetting("COMPARE_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.COMPARE_PROMPT
                    initialContext.add(ChatMessageDto(role = "system", content = prompt))
                    initialContext.add(ChatMessageDto(role = "user", content = "Please compare the following words:\\n${word.term}"))
                }
            }
        }
        
        val mappedMessages = initialContext + messages.map { ChatMessageDto(role = it.role, content = it.content) }
        val fallbackModel = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest" }
        val modelsList = if (fallbackModel.isNotBlank() && fallbackModel != model) listOf(model, fallbackModel) else null
        val singleModel = if (modelsList == null) model else null

        val requestBody = ChatRequest(
            model = singleModel,
            models = modelsList,
            messages = mappedMessages,
            stream = false
        )"""

pattern = r'    fun streamChat\(messages: List<com\.aidict\.app\.data\.entities\.ChatMessage>, forceFallback: Boolean = false\): Flow<String> = callbackFlow \{.*?\n        val requestBody = ChatRequest\(\n            model = singleModel,\n            models = modelsList,\n            messages = mappedMessages,\n            stream = false\n        \)'
text = re.sub(pattern, replacement.strip('\n'), text, flags=re.DOTALL)

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'w') as f:
    f.write(text)

