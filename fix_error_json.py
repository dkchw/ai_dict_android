import re

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'r') as f:
    content = f.read()

replacement = """
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
"""

pattern = r'                var finalMessage = "API Error: \$\{response\?\.code\} \$\{response\?\.message\} \$\{t\?\.message \?: ""\}"\n                if \(errorBody != null && errorBody\.isNotBlank\(\)\) \{\n                    try \{\n                        val obj = json\.decodeFromString<JsonObject>\(errorBody\)\n                        val errMessage = obj\["error"\]\?\.jsonObject\?\.get\("message"\)\?\.jsonPrimitive\?\.content\n                        if \(errMessage != null\) \{\n                            finalMessage = "API Error: \$errMessage"\n                        \} else \{\n                            finalMessage = "API Error: \$errorBody"\n                        \}\n                    \} catch \(e: Exception\) \{\n                        finalMessage = "API Error: \$errorBody"\n                    \}\n                \}'
content = re.sub(pattern, replacement.strip('\n'), content, flags=re.DOTALL)

with open('android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt', 'w') as f:
    f.write(content)
