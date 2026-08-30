package com.aidict.app.data

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
import okhttp3.sse.EventSource
import okhttp3.sse.EventSourceListener
import okhttp3.sse.EventSources
import kotlinx.coroutines.runBlocking
import com.aidict.app.data.AppDatabase

class LlmRepository(private val database: AppDatabase) {
    private val client = OkHttpClient.Builder().build()
    private val eventSourceFactory = EventSources.createFactory(client)
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
            stream = true
        )
        streamInternal(json.encodeToString(requestBody), this)
        awaitClose {}
    }

    fun streamExplain(text: String): Flow<String> = callbackFlow {
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
                ChatMessageDto(role = "user", content = "Please explain this sentence/paragraph:\n$text")
            ),
            stream = true
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
            stream = true
        )
        streamInternal(json.encodeToString(requestBody), this)
        awaitClose {}
    }

    fun streamCompare(words: String): Flow<String> = callbackFlow {
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
                ChatMessageDto(role = "user", content = "Please compare the following words:\n$words")
            ),
            stream = true
        )
        streamInternal(json.encodeToString(requestBody), this)
        awaitClose {}
    }

    fun streamChat(messages: List<com.aidict.app.data.entities.ChatMessage>, forceFallback: Boolean = false): Flow<String> = callbackFlow {
        val model = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("CHAT_MODEL")?.value ?: "~deepseek/deepseek-v4-flash-latest" }
        val mappedMessages = messages.map { ChatMessageDto(role = it.role, content = it.content) }
        val fallbackModel = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest" }
        val modelsList = if (fallbackModel.isNotBlank() && fallbackModel != model) listOf(model, fallbackModel) else null
        val singleModel = if (modelsList == null) model else null
        val requestBody = ChatRequest(
            model = singleModel,
            models = modelsList,
            messages = mappedMessages,
            stream = true
        )
        streamInternal(json.encodeToString(requestBody), this)
        awaitClose {}
    }

    private fun streamInternal(bodyStr: String, scope: kotlinx.coroutines.channels.ProducerScope<String>) {
        val request = Request.Builder()
            .url("https://openrouter.ai/api/v1/chat/completions")
            .addHeader("Authorization", "Bearer ${getApiKey()}")
            .addHeader("HTTP-Referer", "https://aidict.app")
            .addHeader("X-Title", "AI Dict Android")
            .post(bodyStr.toRequestBody("application/json".toMediaType()))
            .build()

        var currentText = ""

        val listener = object : EventSourceListener() {
            override fun onEvent(eventSource: EventSource, id: String?, type: String?, data: String) {
                if (data == "[DONE]") {
                    scope.close()
                    return
                }
                try {
                    val obj = json.decodeFromString<JsonObject>(data)
                    val content = obj["choices"]?.jsonArray?.get(0)?.jsonObject?.get("delta")?.jsonObject?.get("content")?.jsonPrimitive?.content
                    if (content != null) {
                        currentText += content
                        scope.trySend(currentText)
                    }
                } catch (e: Exception) {
                    // Ignore partial json parse errors
                }
            }

override fun onFailure(eventSource: EventSource, t: Throwable?, response: okhttp3.Response?) {
                val errorBody = try { response?.body?.string() } catch (e: Exception) { null }
                if (response?.isSuccessful == true && errorBody != null) {
                    try {
                        val obj = json.decodeFromString<JsonObject>(errorBody)
                        val content = obj["choices"]?.jsonArray?.get(0)?.jsonObject?.get("message")?.jsonObject?.get("content")?.jsonPrimitive?.content
                        if (content != null) {
                            currentText += content
                            scope.trySend(currentText)
                            scope.close()
                            return
                        }
                    } catch (e: Exception) {}
                }
                
                var finalMessage = "API Error: ${response?.code} ${response?.message} ${t?.message ?: ""}"
                if (errorBody != null && errorBody.isNotBlank()) {
                    try {
                        val obj = json.decodeFromString<JsonObject>(errorBody)
                        var errMessage: String? = null
                        
                        // Try various common error JSON formats
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
                        
                        if (errMessage != null) {
                            finalMessage = "API Error: $errMessage"
                        } else {
                            finalMessage = "API Error: $errorBody"
                        }
                    } catch (e: Exception) {
                        finalMessage = "API Error: $errorBody"
                    }
                }

                scope.close(Exception(finalMessage))
            }

            override fun onClosed(eventSource: EventSource) {
                scope.close()
            }
        }

        eventSourceFactory.newEventSource(request, listener)
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
