sed -i 's/val model: String,/val model: String? = null,\n    val models: List<String>? = null,/' android_app/app/src/main/java/com/aidict/app/api/OpenRouterApi.kt
