# For streamExplanation
sed -i '/val requestBody = ChatRequest(/i \        val fallbackModel = runBlocking(kotlinx.coroutines.Dispatchers.IO) { database.appDao().getSetting("FALLBACK_MODELS")?.value ?: "~deepseek/deepseek-v4-flash-latest" }\n        val modelsList = if (fallbackModel.isNotBlank() && fallbackModel != model) listOf(model, fallbackModel) else null\n        val singleModel = if (modelsList == null) model else null' android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt

# Replace "model = model," with "model = singleModel,\n            models = modelsList,"
sed -i 's/model = model,/model = singleModel,\n            models = modelsList,/g' android_app/app/src/main/java/com/aidict/app/data/LlmRepository.kt
