with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()

text = text.replace(
    'val s = database.appDao().getSetting("ACTIVE_SESSION_ID")\n                if (s != null) database.appDao().deleteSetting(s)',
    'database.appDao().insertSetting(AppSetting("ACTIVE_SESSION_ID", ""))'
)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)
