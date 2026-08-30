import re

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'r') as f:
    content = f.read()

# 1. Change `stream = true` to `stream = false` in all methods
content = content.replace("stream = true", "stream = false")

# 2. Refactor streamInternal to standard synchronous OkHttp call wrapped in try/catch and emit the full string.
new_stream_internal = """
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
                            scope.close(Exception("API Error: Valid response but no content found.\\n$bodyStr"))
                            return@launch
                        }
                    } catch (e: Exception) {
                        scope.close(Exception("API Error: Failed to parse JSON response.\\n$bodyStr"))
                        return@launch
                    }
                } else {
                    // Try parsing OpenRouter error format
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
"""

start_idx = content.find('private fun streamInternal(jsonBody: String, scope: kotlinx.coroutines.channels.ProducerScope<String>) {')
end_idx = content.find('suspend fun fetchModels(): List<String> {')
content = content[:start_idx] + new_stream_internal + "\n    " + content[end_idx:]

# Remove unused imports if we want, but not strictly necessary. Let's just write the file.
with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'w') as f:
    f.write(content)

