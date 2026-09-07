package com.aidict.app

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build

class AiDictApplication : Application() {
    companion object {
        lateinit var instance: AiDictApplication
            private set

        const val BUBBLE_CHANNEL_ID = "ai_dict_bubble_channel"
        const val TASK_CHANNEL_ID = "ai_dict_task_channel"
    }

    override fun onCreate() {
        super.onCreate()
        instance = this
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val notificationManager = getSystemService(NotificationManager::class.java)

            // Bubble channel: low importance (silent)
            val bubbleChannel = NotificationChannel(
                BUBBLE_CHANNEL_ID,
                "Floating Bubble Service",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Keeps the AI Dict floating bubble and background engine active"
                setShowBadge(false)
            }

            // Background generation task channel: low importance (silent)
            val taskChannel = NotificationChannel(
                TASK_CHANNEL_ID,
                "Background AI Lookup",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Shows progress when querying AI dictionary in the background"
                setShowBadge(false)
            }

            notificationManager.createNotificationChannel(bubbleChannel)
            notificationManager.createNotificationChannel(taskChannel)
        }
    }
}
