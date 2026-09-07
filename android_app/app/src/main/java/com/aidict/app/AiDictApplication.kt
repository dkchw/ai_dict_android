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
    }

    override fun onCreate() {
        super.onCreate()
        instance = this
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val notificationManager = getSystemService(NotificationManager::class.java)

            // Bubble channel: low importance (silent, no sound/vibrate)
            val bubbleChannel = NotificationChannel(
                BUBBLE_CHANNEL_ID,
                "Floating Bubble Service",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Keeps the AI Dict floating bubble active"
                setShowBadge(false)
            }

            notificationManager?.createNotificationChannel(bubbleChannel)
        }
    }
}
