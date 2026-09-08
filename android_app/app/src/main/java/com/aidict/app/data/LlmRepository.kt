package com.aidict.app.data

import com.aidict.app.api.ChatRequest
import com.aidict.app.api.ChatMessageDto
import com.aidict.app.data.AppDatabase
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.withContext
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

class LlmRepository(private val database: AppDatabase) {
    private val client = OkHttpClient.Builder()
        .connectTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
        .writeTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
        .readTimeout(120, java.util.concurrent.TimeUnit.SECONDS)
        .pingInterval(15, java.util.concurrent.TimeUnit.SECONDS)
        .retryOnConnectionFailure(true)
        .connectionPool(okhttp3.ConnectionPool(10, 5, java.util.concurrent.TimeUnit.MINUTES))
        .dispatcher(okhttp3.Dispatcher().apply {
            maxRequests = 32
            maxRequestsPerHost = 10
        })
        .build()
    private val json = Json { ignoreUnknownKeys = true }

    private suspend fun getApiKey(): String {
        return database.appDao().getSetting("OPENROUTER_API_KEY")?.value?.trim() ?: ""
    }

    private suspend fun executeRequest(jsonBody: String): String = withContext(Dispatchers.IO) {
        val apiKey = getApiKey()
        if (apiKey.isBlank()) {
            throw Exception("API Key is missing. Please set it in Settings.")
        }

        val request = Request.Builder()
            .url("https://openrouter.ai/api/v1/chat/completions")
            .post(jsonBody.toRequestBody("application/json".toMediaType()))
            .addHeader("Authorization", "Bearer $apiKey")
            .addHeader("HTTP-Referer", "https://github.com/aidict")
            .addHeader("X-Title", "AI Dict")
            .build()

        var lastException: Exception? = null

        for (attempt in 1..2) {
            val call = client.newCall(request)
            try {
                val response = suspendCancellableCoroutine { continuation ->
                    continuation.invokeOnCancellation {
                        try {
                            call.cancel()
                        } catch (ignored: Throwable) {}
                    }
                    call.enqueue(object : okhttp3.Callback {
                        override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
                            continuation.resumeWith(Result.success(response))
                        }
                        override fun onFailure(call: okhttp3.Call, e: java.io.IOException) {
                            continuation.resumeWith(Result.failure(e))
                        }
                    })
                }

                val bodyStr = response.body?.string()

                if (response.isSuccessful && bodyStr != null) {
                    try {
                        val obj = json.decodeFromString<JsonObject>(bodyStr)
                        val message = obj["choices"]?.jsonArray?.firstOrNull()?.jsonObject?.get("message")?.jsonObject
                        val content = message?.get("content")?.jsonPrimitive?.content

                        if (content != null) {
                            return@withContext content
                        } else {
                            throw Exception("API Error: Valid response but no content found.\n$bodyStr")
                        }
                    } catch (e: Exception) {
                        throw Exception("API Error: Failed to parse JSON response.\n$bodyStr")
                    }
                } else {
                    if (attempt == 1 && response.code in listOf(429, 500, 502, 503, 504)) {
                        delay(1500)
                        continue
                    }

                    var errMessage: String? = null
                    if (bodyStr != null) {
                        try {
                            val obj = json.decodeFromString<JsonObject>(bodyStr)
                            val errorElement = obj["error"]
                            if (errorElement != null) {
                                if (errorElement is JsonObject) {
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
                    throw Exception("API Error: $finalMessage")
                }
            } catch (e: Exception) {
                lastException = e
                if (e is kotlinx.coroutines.CancellationException) {
                    throw e
                }
                if (attempt == 1 && (e is java.net.SocketTimeoutException || e is java.io.IOException)) {
                    delay(1000)
                    continue
                }
                break
            }
        }

        throw lastException ?: Exception("Network request failed")
    }

    fun streamExplanation(term: String, sourceLang: String, targetLang: String): Flow<String> = flow {
        val model = database.appDao().getSetting("DICT_MODEL")?.value ?: "inclusionai/ling-3.0-flash"
        val promptTemplate = database.appDao().getSetting("DICT_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.DICT_PROMPT
        val fallbackModel = database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest"
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
        val content = executeRequest(json.encodeToString(requestBody))
        emit(content)
    }.flowOn(Dispatchers.IO)

    fun streamExplain(text: String, sourceLang: String, targetLang: String): Flow<String> = flow {
        val model = database.appDao().getSetting("EXPLAIN_MODEL")?.value ?: "inclusionai/ling-3.0-flash"
        val promptTemplate = database.appDao().getSetting("EXPLAIN_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.EXPLAIN_PROMPT
        val fallbackModel = database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest"
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
        val content = executeRequest(json.encodeToString(requestBody))
        emit(content)
    }.flowOn(Dispatchers.IO)

    fun streamTranslation(sourceText: String, sourceLang: String, targetLang: String): Flow<String> = flow {
        val model = database.appDao().getSetting("TRANSLATE_MODEL")?.value ?: "inclusionai/ling-3.0-flash"
        val promptTemplate = database.appDao().getSetting("TRANSLATE_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.TRANSLATE_PROMPT
        val fallbackModel = database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest"
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
        val content = executeRequest(json.encodeToString(requestBody))
        emit(content)
    }.flowOn(Dispatchers.IO)

    fun streamCompare(words: String, sourceLang: String, targetLang: String): Flow<String> = flow {
        val model = database.appDao().getSetting("COMPARE_MODEL")?.value ?: "inclusionai/ling-3.0-flash"
        val promptTemplate = database.appDao().getSetting("COMPARE_PROMPT")?.value ?: com.aidict.app.utils.DefaultPrompts.COMPARE_PROMPT
        val fallbackModel = database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest"
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
        val content = executeRequest(json.encodeToString(requestBody))
        emit(content)
    }.flowOn(Dispatchers.IO)

    fun streamChat(word: com.aidict.app.data.entities.Word, messages: List<com.aidict.app.data.entities.ChatMessage>, forceFallback: Boolean = false): Flow<String> = flow {
        val configuredModel = database.appDao().getSetting("CHAT_MODEL")?.value ?: "~deepseek/deepseek-v4-flash-latest"
        val fallbackModel = database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest"
        val model = if (forceFallback && fallbackModel.isNotBlank()) fallbackModel else configuredModel
        val modelsList = if (!forceFallback && fallbackModel.isNotBlank() && fallbackModel != model) listOf(model, fallbackModel) else null
        val singleModel = if (modelsList == null) model else null

        val initialContext = mutableListOf<ChatMessageDto>()
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

        val mappedMessages = initialContext + messages.map { ChatMessageDto(role = it.role, content = it.content) }

        val requestBody = ChatRequest(
            model = singleModel,
            models = modelsList,
            messages = mappedMessages,
            stream = false
        )

        val content = executeRequest(json.encodeToString(requestBody))
        emit(content)
    }.flowOn(Dispatchers.IO)



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
