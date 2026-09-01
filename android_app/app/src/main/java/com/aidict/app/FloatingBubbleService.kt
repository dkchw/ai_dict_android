package com.aidict.app

import android.app.Service
import android.content.Intent
import android.graphics.Color
import android.graphics.PixelFormat
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.IBinder
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.ImageView
import android.widget.TextView
import android.widget.FrameLayout
import android.widget.Toast
import kotlinx.coroutines.launch

class FloatingBubbleService : Service() {
    private lateinit var windowManager: WindowManager
    private lateinit var bubbleView: ImageView
    private var closeView: FrameLayout? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        windowManager = getSystemService(WINDOW_SERVICE) as WindowManager

        bubbleView = ImageView(this).apply {
            setImageResource(R.mipmap.app_icon_round)
            layoutParams = android.view.ViewGroup.LayoutParams(160, 160)
            setPadding(16, 16, 16, 16)
        }
        


        val layoutFlag = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_PHONE
        }

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutFlag,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = 0
            y = 300
        }

        bubbleView.setOnTouchListener(object : View.OnTouchListener {
            private var initialX = 0
            private var initialY = 0
            private var initialTouchX = 0f
            private var initialTouchY = 0f

            override fun onTouch(v: View, event: MotionEvent): Boolean {
                when (event.action) {
                    MotionEvent.ACTION_DOWN -> {
                        initialX = params.x
                        initialY = params.y
                        initialTouchX = event.rawX
                        initialTouchY = event.rawY

                        // Show close view
                        if (closeView == null) {
                            closeView = FrameLayout(this@FloatingBubbleService).apply {
                                val bg = GradientDrawable().apply {
                                    shape = GradientDrawable.OVAL
                                    setColor(Color.parseColor("#88000000"))
                                }
                                background = bg
                                
                                val tv = TextView(this@FloatingBubbleService).apply {
                                    text = "X"
                                    setTextColor(Color.WHITE)
                                    textSize = 24f
                                    gravity = Gravity.CENTER
                                }
                                addView(tv, FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT))
                            }

                            val closeParams = WindowManager.LayoutParams(
                                200, 200,
                                layoutFlag,
                                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
                                PixelFormat.TRANSLUCENT
                            ).apply {
                                gravity = Gravity.BOTTOM or Gravity.CENTER_HORIZONTAL
                                y = 150
                            }
                            windowManager.addView(closeView, closeParams)
                        }

                        return true
                    }
                    MotionEvent.ACTION_UP -> {
                        if (closeView != null) {
                            windowManager.removeView(closeView)
                            closeView = null
                        }

                        val xDiff = Math.abs(event.rawX - initialTouchX)
                        val yDiff = Math.abs(event.rawY - initialTouchY)
                        if (xDiff < 20 && yDiff < 20) {
                            if (PopupActivity.isVisible) {
                                val intent = Intent(this@FloatingBubbleService, PopupActivity::class.java).apply {
                                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
                                    action = "CLOSE_POPUP"
                                }
                                startActivity(intent)
                            } else {
                                val intent = Intent(this@FloatingBubbleService, PopupActivity::class.java).apply {
                                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)
                                }
                                startActivity(intent)
                            }
                        } else {
                            val displayMetrics = resources.displayMetrics
                            val screenHeight = displayMetrics.heightPixels
                            if (event.rawY > screenHeight - 350) {
                                stopSelf()
                            } else {
                                params.x = if (event.rawX > displayMetrics.widthPixels / 2) displayMetrics.widthPixels else 0
                                windowManager.updateViewLayout(bubbleView, params)
                            }
                        }
                        return true
                    }
                    MotionEvent.ACTION_MOVE -> {
                        params.x = initialX + (event.rawX - initialTouchX).toInt()
                        params.y = initialY + (event.rawY - initialTouchY).toInt()
                        windowManager.updateViewLayout(bubbleView, params)

                        // Highlight close view if close
                        val displayMetrics = resources.displayMetrics
                        val screenHeight = displayMetrics.heightPixels
                        if (event.rawY > screenHeight - 350) {
                            val bg = GradientDrawable().apply {
                                shape = GradientDrawable.OVAL
                                setColor(Color.parseColor("#CCFF0000"))
                            }
                            closeView?.background = bg
                        } else {
                            val bg = GradientDrawable().apply {
                                shape = GradientDrawable.OVAL
                                setColor(Color.parseColor("#88000000"))
                            }
                            closeView?.background = bg
                        }

                        return true
                    }
                }
                return false
            }
        })

        windowManager.addView(bubbleView, params)

        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
            val db = com.aidict.app.data.AppDatabase.getDatabase(this@FloatingBubbleService)
            val sizeStr = db.appDao().getSetting("BUBBLE_SIZE")?.value ?: "160"
            val size = sizeStr.toIntOrNull() ?: 160
            kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                params.width = size
                params.height = size
                windowManager.updateViewLayout(bubbleView, params)
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        if (::bubbleView.isInitialized) {
            windowManager.removeView(bubbleView)
        }
        if (closeView != null) {
            windowManager.removeView(closeView)
            closeView = null
        }
    }
}
