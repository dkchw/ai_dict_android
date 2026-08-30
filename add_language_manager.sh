cat << 'INNER' > android_app/app/src/main/java/com/aidict/app/utils/LanguageManager.kt
package com.aidict.app.utils

import java.util.Locale

object LanguageManager {
    val allLanguages: List<String> by lazy {
        val locales = Locale.getISOLanguages().map { Locale(it).getDisplayLanguage(Locale.ENGLISH) }
        listOf("Auto Detect") + locales.distinct().sorted().filter { it.isNotBlank() }
    }

    fun getOrderedLanguages(starredCsv: String?): List<String> {
        val starred = starredCsv?.split(",")?.map { it.trim() }?.filter { it.isNotBlank() } ?: listOf("English", "Vietnamese", "German", "Spanish", "French")
        
        val autoDetect = if (starred.contains("Auto Detect")) emptyList() else listOf("Auto Detect")
        val orderedStarred = autoDetect + starred
        
        val remaining = allLanguages.filter { !orderedStarred.contains(it) }
        return orderedStarred + remaining
    }
}
INNER
