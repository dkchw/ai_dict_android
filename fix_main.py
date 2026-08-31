import re

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'r') as f:
    text = f.read()

# Remove anything related to ExplainViewModel, TranslateViewModel, CompareViewModel
text = re.sub(r'\s*val explainViewModel.*?\}', '', text, flags=re.DOTALL)
text = re.sub(r'\s*val translateViewModel.*?\}', '', text, flags=re.DOTALL)
text = re.sub(r'\s*val compareViewModel.*?\}', '', text, flags=re.DOTALL)

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'w') as f:
    f.write(text)
