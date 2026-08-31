#!/bin/bash
set -e

GRADLE_FILE="android_app/app/build.gradle.kts"

# 1. Extract current versions
OLD_VCODE=$(grep -oP 'versionCode\s*=\s*\K\d+' $GRADLE_FILE)
OLD_VNAME=$(grep -oP 'versionName\s*=\s*"\K[^"]+' $GRADLE_FILE)

# 2. Calculate new versions
NEW_VCODE=$((OLD_VCODE + 1))
MAJOR=$(echo $OLD_VNAME | cut -d. -f1)
MINOR=$(echo $OLD_VNAME | cut -d. -f2)
NEW_MINOR=$((MINOR + 1))
NEW_VNAME="${MAJOR}.${NEW_MINOR}"

echo "====================================="
echo "Bumping version: $OLD_VNAME -> $NEW_VNAME"
echo "====================================="

# 3. Apply to build.gradle.kts
sed -i "s/versionCode = $OLD_VCODE/versionCode = $NEW_VCODE/" $GRADLE_FILE
sed -i "s/versionName = \"$OLD_VNAME\"/versionName = \"$NEW_VNAME\"/" $GRADLE_FILE

# 4. Compile locally
echo "Compiling APK..."
cd android_app
./gradlew assembleDebug
cd ..

# 5. Copy APK for git tracking
echo "Copying APK to repository root..."
cp android_app/app/build/outputs/apk/debug/app-debug.apk release_latest.apk

# 6. Commit and Push
echo "Committing and pushing to GitHub..."
git add .
git commit -m "Auto-release v$NEW_VNAME"
git push

echo "====================================="
echo "Done! The GitHub Action will now instantly publish v$NEW_VNAME"
echo "====================================="
