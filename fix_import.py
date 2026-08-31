with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'r') as f:
    lines = f.readlines()

if 'import androidx.compose.foundation.clickable\n' in lines:
    lines.remove('import androidx.compose.foundation.clickable\n')

lines.insert(1, '\nimport androidx.compose.foundation.clickable\n')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/SettingsScreen.kt', 'w') as f:
    f.writelines(lines)
