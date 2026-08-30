sed -i 's/fun streamChat(messages: List<com.aidict.app.data.entities.ChatMessage>): Flow<String> = callbackFlow {/fun streamChat(messages: List<com.aidict.app.data.entities.ChatMessage>, forceFallback: Boolean = false): Flow<String> = callbackFlow {/g' android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt

# Inject the check
sed -i 's/val models = if (fallbackModel != null && fallbackModel != model) listOf(model, fallbackModel) else null/val models = if (forceFallback) listOf(fallbackModel ?: model) else if (fallbackModel != null \&\& fallbackModel != model) listOf(model, fallbackModel) else null/g' android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt
