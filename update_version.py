with open('android_app/app/build.gradle.kts', 'r') as f:
    text = f.read()
import re
old_vcode = int(re.search(r'versionCode\s*=\s*(\d+)', text).group(1))
new_vcode = old_vcode + 1
text = re.sub(r'versionCode\s*=\s*\d+', f'versionCode = {new_vcode}', text)
text = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "3.0"', text)
with open('android_app/app/build.gradle.kts', 'w') as f:
    f.write(text)

with open('build_and_push.sh', 'r') as f:
    script = f.read()

# Make the script NOT bump version if it's already 3.0
script = script.replace('NEW_VNAME="${MAJOR}.${NEW_MINOR}"', 'if [ "$OLD_VNAME" = "3.0" ]; then\n  NEW_VNAME="3.0"\n  NEW_VCODE=$OLD_VCODE\nelse\n  NEW_VNAME="${MAJOR}.${NEW_MINOR}"\nfi')
with open('build_and_push.sh', 'w') as f:
    f.write(script)
