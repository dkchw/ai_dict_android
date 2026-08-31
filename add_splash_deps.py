import re

with open('android_app/app/build.gradle.kts', 'r') as f:
    text = f.read()

deps_end = """}

dependencies {"""

new_deps_end = """    implementation("androidx.core:core-splashscreen:1.0.1")
}

dependencies {"""

text = text.replace(deps_end, new_deps_end)

with open('android_app/app/build.gradle.kts', 'w') as f:
    f.write(text)

