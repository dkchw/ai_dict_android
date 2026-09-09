package com.aidict.app.services

import android.app.Notification
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.os.Build
import android.os.IBinder
import android.os.PowerManager
import androidx.core.app.NotificationCompat
import com.aidict.app.AiDictApplication
import com.aidict.app.MainActivity
import com.aidict.app.R
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.concurrent.atomic.AtomicInteger

class BackgroundSyncService : Service() {

    companion object {
        private const val NOTIFICATION_ID = 2002
        const val ACTION_START = "com.aidict.app.action.START_BACKGROUND_SERVICE"
        const val ACTION_STOP = "com.aidict.app.action.STOP_BACKGROUND_SERVICE"

        private val _isRunning = MutableStateFlow(false)
        val isRunning: StateFlow<Boolean> = _isRunning.asStateFlow()

        private val _isNetworkOnline = MutableStateFlow(true)
        val isNetworkOnline: StateFlow<Boolean> = _isNetworkOnline.asStateFlow()

        private var wakeLock: PowerManager.WakeLock? = null
        private val wakeLockCounter = AtomicInteger(0)

        @Synchronized
        fun acquireWakeLock(context: Context, timeoutMs: Long = 180_000L) {
            try {
                wakeLockCounter.incrementAndGet()
                if (wakeLock == null || !wakeLock!!.isHeld) {
                    val powerManager = context.getSystemService(Context.POWER_SERVICE) as? PowerManager
                    wakeLock = powerManager?.newWakeLock(
                        PowerManager.PARTIAL_WAKE_LOCK,
                        "AIDict:BackgroundApiWakeLock"
                    )?.apply {
                        setReferenceCounted(false)
                        acquire(timeoutMs)
                    }
                }
            } catch (e: Exception) {
                android.util.Log.e("BackgroundSyncService", "Failed to acquire wake lock", e)
            }
        }

        @Synchronized
        fun releaseWakeLock() {
            try {
                val remaining = wakeLockCounter.decrementAndGet()
                if (remaining <= 0) {
                    wakeLockCounter.set(0)
                    if (wakeLock != null && wakeLock!!.isHeld) {
                        wakeLock?.release()
                    }
                    wakeLock = null
                }
            } catch (e: Exception) {
                android.util.Log.e("BackgroundSyncService", "Failed to release wake lock", e)
            }
        }

        fun start(context: Context) {
            val intent = Intent(context, BackgroundSyncService::class.java).apply {
                action = ACTION_START
            }
            try {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    context.startForegroundService(intent)
                } else {
                    context.startService(intent)
                }
            } catch (e: Exception) {
                android.util.Log.e("BackgroundSyncService", "Error starting BackgroundSyncService", e)
            }
        }

        fun stop(context: Context) {
            val intent = Intent(context, BackgroundSyncService::class.java).apply {
                action = ACTION_STOP
            }
            try {
                context.startService(intent)
            } catch (e: Exception) {
                try {
                    context.stopService(intent)
                } catch (ignored: Exception) {}
            }
        }
        fun buildNotification(context: Context, statusText: String): Notification {
            val openIntent = Intent(context, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            val pendingOpen = PendingIntent.getActivity(
                context,
                0,
                openIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )

            val stopIntent = Intent(context, BackgroundSyncService::class.java).apply {
                action = ACTION_STOP
            }
            val pendingStop = PendingIntent.getService(
                context,
                1,
                stopIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )

            return NotificationCompat.Builder(context, AiDictApplication.BACKGROUND_CHANNEL_ID)
                .setSmallIcon(R.drawable.ic_notification)
                .setContentTitle("AI Dict 24/7 Engine")
                .setContentText(statusText)
                .setOngoing(true)
                .setSilent(true)
                .setContentIntent(pendingOpen)
                .addAction(android.R.drawable.ic_menu_close_clear_cancel, "Stop 24/7 Mode", pendingStop)
                .setPriority(NotificationCompat.PRIORITY_LOW)
                .build()
        }

        fun updateNotification(context: Context, statusText: String) {
            if (!_isRunning.value) return
            try {
                val notification = buildNotification(context, statusText)
                val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager
                manager?.notify(NOTIFICATION_ID, notification)
            } catch (ignored: Exception) {}
        }
    }

    private var connectivityManager: ConnectivityManager? = null
    private var networkCallback: ConnectivityManager.NetworkCallback? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        _isRunning.value = true
        setupNetworkMonitoring()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            _isRunning.value = false
            stopForeground(STOP_FOREGROUND_REMOVE)
            stopSelf()
            return START_NOT_STICKY
        }

        startInForeground()
        return START_STICKY
    }

    private fun startInForeground() {
        val notification = buildNotification(this, "Running 24/7 in background. API calls & searches active.")
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
                startForeground(
                    NOTIFICATION_ID,
                    notification,
                    ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC or ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE
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
            } catch (ignored: Exception) {}
        }
    }

    private fun setupNetworkMonitoring() {
        try {
            connectivityManager = getSystemService(Context.CONNECTIVITY_SERVICE) as? ConnectivityManager
            val request = NetworkRequest.Builder()
                .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
                .build()

            networkCallback = object : ConnectivityManager.NetworkCallback() {
                override fun onAvailable(network: Network) {
                    _isNetworkOnline.value = true
                    updateNotification("Online - Background search & API ready.")
                }

                override fun onLost(network: Network) {
                    _isNetworkOnline.value = false
                    updateNotification("Waiting for internet connection...")
                }
            }
            connectivityManager?.registerNetworkCallback(request, networkCallback!!)
        } catch (e: Exception) {
            android.util.Log.e("BackgroundSyncService", "Failed to register network callback", e)
        }
    }

    private fun updateNotification(text: String) {
        updateNotification(this, text)
    }

    override fun onDestroy() {
        super.onDestroy()
        _isRunning.value = false
        try {
            networkCallback?.let { connectivityManager?.unregisterNetworkCallback(it) }
        } catch (ignored: Exception) {}
        try {
            if (wakeLock != null && wakeLock!!.isHeld) {
                wakeLock?.release()
            }
            wakeLock = null
            wakeLockCounter.set(0)
        } catch (ignored: Exception) {}
    }
}
