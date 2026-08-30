import re

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'r') as f:
    content = f.read()

replacement = """
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
                        val errMessage = obj["error"]?.jsonObject?.get("message")?.jsonPrimitive?.content
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
"""

# Replace the onFailure method
pattern = r'            override fun onFailure\(eventSource: EventSource, t: Throwable\?, response: okhttp3\.Response\?\) \{.*?scope\.close\(Exception\(finalMessage\)\)\n            \}'
content = re.sub(pattern, replacement.strip(), content, flags=re.DOTALL)

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'w') as f:
    f.write(content)
