import re

with open('android_app/app/build.gradle.kts', 'r') as f:
    text = f.read()

bad_block = """    }
    implementation("androidx.core:core-splashscreen:1.0.1")
}"""

good_block = """    }
}"""

text = text.replace(bad_block, good_block)

deps_start = """dependencies {
    implementation("io.coil-kt:coil-compose:2.6.0")"""

deps_new = """dependencies {
    implementation("androidx.core:core-splashscreen:1.0.1")
    implementation("io.coil-kt:coil-compose:2.6.0")"""

text = text.replace(deps_start, deps_new)

with open('android_app/app/build.gradle.kts', 'w') as f:
    f.write(text)
