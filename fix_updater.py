import re

with open('android_app/app/src/main/java/com/aidict/app/utils/AutoUpdater.kt', 'r') as f:
    text = f.read()

# 1. Use applicationContext for the broadcast receiver to prevent leak/destruction
# 2. Use downloadManager.getUriForDownloadedFile(downloadId) for better compatibility

old_install = """    private fun installApk(filename: String) {
        try {
            val file = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), filename)
            if (file.exists()) {
                val intent = Intent(Intent.ACTION_VIEW)
                val apkUri = FileProvider.getUriForFile(context, "${context.packageName}.provider", file)
                intent.setDataAndType(apkUri, "application/vnd.android.package-archive")
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                context.startActivity(intent)
            }
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(context, "Failed to install update.", Toast.LENGTH_SHORT).show()
        }
    }"""

new_install = """    private fun installApk(filename: String, downloadId: Long) {
        try {
            val downloadManager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
            var apkUri = downloadManager.getUriForDownloadedFile(downloadId)
            
            if (apkUri == null) {
                val file = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), filename)
                if (file.exists()) {
                    apkUri = FileProvider.getUriForFile(context, "${context.packageName}.provider", file)
                }
            }
            
            if (apkUri != null) {
                val intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(apkUri, "application/vnd.android.package-archive")
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                context.startActivity(intent)
            } else {
                Toast.makeText(context, "Downloaded file not found.", Toast.LENGTH_SHORT).show()
            }
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(context, "Failed to install update: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }"""

text = text.replace(old_install, new_install)

text = text.replace("installApk(\"ai_dict_$version.apk\")", "installApk(\"ai_dict_$version.apk\", downloadId)")

old_receiver = """        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            context.registerReceiver(onComplete, IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE), Context.RECEIVER_EXPORTED)
        } else {
            context.registerReceiver(onComplete, IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE))
        }"""

new_receiver = """        val appContext = context.applicationContext
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            appContext.registerReceiver(onComplete, IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE), Context.RECEIVER_EXPORTED)
        } else {
            appContext.registerReceiver(onComplete, IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE))
        }"""
        
text = text.replace(old_receiver, new_receiver)

# In the BroadcastReceiver, we must unregister from appContext
text = text.replace("context.unregisterReceiver(this)", "ctxt.applicationContext.unregisterReceiver(this)")

with open('android_app/app/src/main/java/com/aidict/app/utils/AutoUpdater.kt', 'w') as f:
    f.write(text)

