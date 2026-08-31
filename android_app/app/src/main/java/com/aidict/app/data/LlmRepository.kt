package com.aidict.app.data
import kotlinx.coroutines.launch

import com.aidict.app.api.ChatRequest
import com.aidict.app.api.ChatMessageDto
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import kotlinx.coroutines.runBlocking
import com.aidict.app.data.AppDatabase

class LlmRepository(private val database: AppDatabase) {
    private val client = OkHttpClient.Builder().build()
    private val json = Json { ignoreUnknownKeys = true }

    private fun getApiKey(): String {
        return runBlocking(kotlinx.coroutines.Dispatchers.IO) {
            database.appDao().getSetting("OPENROUTER_API_KEY")?.value?.trim() ?: ""
        }
    }

    fun streamExplanation(term: String, sourceLang: String, targetLang: String): Flow<String> = callbackFlow {
        val model = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("DICT_MODEL")?.value ?: "inclusionai/ling-3.0-flash" }
        val promptTemplate = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("DICT_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.DICT_PROMPT }
        
        val fallbackModel = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest" }
        val modelsList = if (fallbackModel.isNotBlank() && fallbackModel != model) listOf(model, fallbackModel) else null
        val singleModel = if (modelsList == null) model else null
        val requestBody = ChatRequest(
            model = singleModel,
            models = modelsList,
            messages = listOf(
                ChatMessageDto(role = "system", content = promptTemplate),
                ChatMessageDto(role = "user", content = "Word/Phrase: $term\nSource language: $sourceLang\nTarget language: $targetLang")
            ),
            stream = false
        )
        streamInternal(json.encodeToString(requestBody), this)
        awaitClose {}
    }

    fun streamExplain(text: String, sourceLang: String, targetLang: String): Flow<String> = callbackFlow {
        val model = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("EXPLAIN_MODEL")?.value ?: "inclusionai/ling-3.0-flash" }
        val promptTemplate = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("EXPLAIN_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.EXPLAIN_PROMPT }
        
        val fallbackModel = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest" }
        val modelsList = if (fallbackModel.isNotBlank() && fallbackModel != model) listOf(model, fallbackModel) else null
        val singleModel = if (modelsList == null) model else null
        val requestBody = ChatRequest(
            model = singleModel,
            models = modelsList,
            messages = listOf(
                ChatMessageDto(role = "system", content = promptTemplate),
                ChatMessageDto(role = "user", content = "Source language: $sourceLang\nTarget language: $targetLang\nPlease explain this sentence/paragraph:\n$text")
            ),
            stream = false
        )
        streamInternal(json.encodeToString(requestBody), this)
        awaitClose {}
    }

    fun streamTranslation(sourceText: String, sourceLang: String, targetLang: String): Flow<String> = callbackFlow {
        val model = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("TRANSLATE_MODEL")?.value ?: "inclusionai/ling-3.0-flash" }
        val promptTemplate = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("TRANSLATE_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.TRANSLATE_PROMPT }
        
        val fallbackModel = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest" }
        val modelsList = if (fallbackModel.isNotBlank() && fallbackModel != model) listOf(model, fallbackModel) else null
        val singleModel = if (modelsList == null) model else null
        val requestBody = ChatRequest(
            model = singleModel,
            models = modelsList,
            messages = listOf(
                ChatMessageDto(role = "system", content = promptTemplate),
                ChatMessageDto(role = "user", content = "Source language: $sourceLang\nTarget language: $targetLang\nConcept: $sourceText")
            ),
            stream = false
        )
        streamInternal(json.encodeToString(requestBody), this)
        awaitClose {}
    }

    fun streamCompare(words: String, sourceLang: String, targetLang: String): Flow<String> = callbackFlow {
        val model = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("COMPARE_MODEL")?.value ?: "inclusionai/ling-3.0-flash" }
        val promptTemplate = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("COMPARE_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.COMPARE_PROMPT }
        
        val fallbackModel = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest" }
        val modelsList = if (fallbackModel.isNotBlank() && fallbackModel != model) listOf(model, fallbackModel) else null
        val singleModel = if (modelsList == null) model else null
        val requestBody = ChatRequest(
            model = singleModel,
            models = modelsList,
            messages = listOf(
                ChatMessageDto(role = "system", content = promptTemplate),
                ChatMessageDto(role = "user", content = "Source language: $sourceLang\nTarget language: $targetLang\nPlease compare the following words:\n$words")
            ),
            stream = false
        )
        streamInternal(json.encodeToString(requestBody), this)
        awaitClose {}
    }

    fun streamChat(word: com.aidict.app.data.entities.Word, messages: List<com.aidict.app.data.entities.ChatMessage>, forceFallback: Boolean = false): Flow<String> = callbackFlow {
        val model = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("CHAT_MODEL")?.value ?: "~deepseek/deepseek-v4-flash-latest" }
        
        val initialContext = mutableListOf<ChatMessageDto>()
        runBlocking(kotlinx.coroutines.Dispatchers.IO) {
            when (word.mode) {
                "dict" -> {
                    val prompt = database.appDao().getSetting("DICT_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.DICT_PROMPT
                    initialContext.add(ChatMessageDto(role = "system", content = prompt))
                    val langs = word.language?.split(" -> ")
                    val src = langs?.getOrNull(0) ?: ""
                    val tgt = langs?.getOrNull(1) ?: ""
                    initialContext.add(ChatMessageDto(role = "user", content = "Word/Phrase: ${word.term}\nSource language: $src\nTarget language: $tgt"))
                }
                "translate" -> {
                    val prompt = database.appDao().getSetting("TRANSLATE_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.TRANSLATE_PROMPT
                    initialContext.add(ChatMessageDto(role = "system", content = prompt))
                    val langs = word.language?.split(" -> ")
                    val src = langs?.getOrNull(0) ?: ""
                    val tgt = langs?.getOrNull(1) ?: ""
                    initialContext.add(ChatMessageDto(role = "user", content = "Source language: $src\nTarget language: $tgt\nConcept: ${word.term}"))
                }
                "explain" -> {
                    val prompt = database.appDao().getSetting("EXPLAIN_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.EXPLAIN_PROMPT
                    initialContext.add(ChatMessageDto(role = "system", content = prompt))
                    initialContext.add(ChatMessageDto(role = "user", content = "Please explain this sentence/paragraph:\n${word.term}"))
                }
                "compare" -> {
                    val prompt = database.appDao().getSetting("COMPARE_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.COMPARE_PROMPT
                    initialContext.add(ChatMessageDto(role = "system", content = prompt))
                    initialContext.add(ChatMessageDto(role = "user", content = "Please compare the following words:\n${word.term}"))
                }
                else -> {}
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
        )

        streamInternal(json.encodeToString(requestBody), this)
        awaitClose {}
    }

    private fun streamInternal(jsonBody: String, scope: kotlinx.coroutines.channels.ProducerScope<String>) {
        val apiKey = getApiKey()
        if (apiKey.isBlank()) {
            scope.close(Exception("API Key is missing. Please set it in Settings."))
            return
        }

        val request = Request.Builder()
            .url("https://openrouter.ai/api/v1/chat/completions")
            .post(jsonBody.toRequestBody("application/json".toMediaType()))
            .addHeader("Authorization", "Bearer $apiKey")
            .addHeader("HTTP-Referer", "https://github.com/aidict")
            .addHeader("X-Title", "AI Dict")
            .build()

        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            try {
                val response = client.newCall(request).execute()
                val bodyStr = response.body?.string()
                
                if (response.isSuccessful && bodyStr != null) {
                    try {
                        val obj = json.decodeFromString<JsonObject>(bodyStr)
                        val message = obj["choices"]?.jsonArray?.firstOrNull()?.jsonObject?.get("message")?.jsonObject
                        val content = message?.get("content")?.jsonPrimitive?.content
                        
                        if (content != null) {
                            scope.trySend(content)
                            scope.close()
                            return@launch
                        } else {
                            scope.close(Exception("API Error: Valid response but no content found.\n$bodyStr"))
                            return@launch
                        }
                    } catch (e: Exception) {
                        scope.close(Exception("API Error: Failed to parse JSON response.\n$bodyStr"))
                        return@launch
                    }
                } else {
                    var errMessage: String? = null
                    if (bodyStr != null) {
                        try {
                            val obj = json.decodeFromString<JsonObject>(bodyStr)
                            val errorElement = obj["error"]
                            if (errorElement != null) {
                                if (errorElement is kotlinx.serialization.json.JsonObject) {
                                    errMessage = errorElement["message"]?.jsonPrimitive?.content ?: errorElement.toString()
                                } else if (errorElement is kotlinx.serialization.json.JsonPrimitive) {
                                    errMessage = errorElement.content
                                } else {
                                    errMessage = errorElement.toString()
                                }
                            } else {
                                errMessage = obj["message"]?.jsonPrimitive?.content
                            }
                        } catch (e: Exception) {}
                    }
                    val finalMessage = errMessage ?: bodyStr ?: "${response.code} ${response.message}"
                    scope.close(Exception("API Error: $finalMessage"))
                }
            } catch (e: Exception) {
                scope.close(Exception("Network Error: ${e.localizedMessage}"))
            }
        }
    }

    suspend fun fetchModels(): List<String> {
        return kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
            try {
                val request = Request.Builder()
                    .url("https://openrouter.ai/api/v1/models")
                    .get()
                    .build()
                val response = client.newCall(request).execute()
                if (response.isSuccessful) {
                    val bodyStr = response.body?.string() ?: return@withContext emptyList()
                    val obj = json.decodeFromString<JsonObject>(bodyStr)
                    obj["data"]?.jsonArray?.mapNotNull { 
                        it.jsonObject["id"]?.jsonPrimitive?.content 
                    } ?: emptyList()
                } else {
                    emptyList()
                }
            } catch (e: Exception) {
                emptyList()
            }
        }
    }
}
