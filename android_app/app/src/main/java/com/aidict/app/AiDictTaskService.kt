package com.aidict.app

import android.app.Notification
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import java.util.concurrent.atomic.AtomicInteger

class AiDictTaskService : Service() {
    companion object {
        private const val NOTIFICATION_ID = 2001
        private val activeTasks = AtomicInteger(0)

        fun startTask(context: Context, taskDescription: String = "Looking up definition...") {
            val count = activeTasks.incrementAndGet()
            val intent = Intent(context, AiDictTaskService::class.java).apply {
                putExtra("TASK_DESC", taskDescription)
            }
            try {
                ContextCompat.startForegroundService(context, intent)
            } catch (e: Exception) {
                // If starting foreground service fails, the task will still proceed on IO scope.
            }
        }

        fun stopTask(context: Context) {
            val count = activeTasks.decrementAndGet()
            if (count <= 0) {
                activeTasks.set(0)
                val intent = Intent(context, AiDictTaskService::class.java)
                try {
                    context.stopService(intent)
                } catch (e: Exception) {}
            }
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val taskDesc = intent?.getStringExtra("TASK_DESC") ?: "Looking up definition in background..."
        val notification = buildNotification(taskDesc)

        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
                startForeground(
                    NOTIFICATION_ID,
                    notification,
                    ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC
                )
            } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                startForeground(
                    NOTIFICATION_ID,
                    notification,
                    ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC
                )
            } else {
                startForeground(NOTIFICATION_ID, notification)
            }
        } catch (e: Exception) {
            try {
                startForeground(NOTIFICATION_ID, notification)
            } catch (e2: Exception) {}
        }

        return START_NOT_STICKY
    }

    private fun buildNotification(text: String): Notification {
        val openIntent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, AiDictApplication.TASK_CHANNEL_ID)
            .setSmallIcon(R.mipmap.app_icon)
            .setContentTitle("AI Dict")
            .setContentText(text)
            .setOngoing(true)
            .setSilent(true)
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    override fun onDestroy() {
        super.onDestroy()
        stopForeground(STOP_FOREGROUND_REMOVE)
    }
}
