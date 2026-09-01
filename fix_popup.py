import re

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'r') as f:
    text = f.read()

old_extra = 'val textExtra = intent.getCharSequenceExtra(Intent.EXTRA_PROCESS_TEXT)?.toString() ?: ""'
new_extra = """val textExtra = intent.getCharSequenceExtra(Intent.EXTRA_PROCESS_TEXT)?.toString()
            ?: intent.getStringExtra(Intent.EXTRA_TEXT)
            ?: intent.getStringExtra("EXTRA_QUERY")
            ?: intent.getStringExtra(android.app.SearchManager.QUERY)
            ?: ""
"""
text = text.replace(old_extra, new_extra)

with open('android_app/app/src/main/java/com/aidict/app/PopupActivity.kt', 'w') as f:
    f.write(text)

