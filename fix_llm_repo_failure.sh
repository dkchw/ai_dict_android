sed -i '/override fun onFailure(eventSource: EventSource, t: Throwable?, response: okhttp3.Response?) {/a \
                val errorBody = try { response?.body?.string() } catch (e: Exception) { null }\n\
                val finalMessage = if (errorBody != null) "API Error: $errorBody" else t?.message ?: "Unknown SSE failure"\n\
                scope.close(Exception(finalMessage))' android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt
sed -i '/scope.close(t ?: Exception("Unknown SSE failure"))/d' android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt
