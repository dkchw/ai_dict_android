import re

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'r') as f:
    text = f.read()

text = re.sub(r'import com\.aidict\.app\.ui\.viewmodels\.CompareViewModel\n', '', text)
text = re.sub(r'import com\.aidict\.app\.ui\.viewmodels\.ExplainViewModel\n', '', text)
text = re.sub(r'import com\.aidict\.app\.ui\.viewmodels\.TranslateViewModel\n', '', text)

text = re.sub(r'        val explainViewModel: ExplainViewModel by viewModels \{.*?\}\n', '', text, flags=re.DOTALL)
text = re.sub(r'        val translateViewModel: TranslateViewModel by viewModels \{.*?\}\n', '', text, flags=re.DOTALL)
text = re.sub(r'        val compareViewModel: CompareViewModel by viewModels \{.*?\}\n', '', text, flags=re.DOTALL)

text = re.sub(r',\n\s*explainViewModel = explainViewModel', '', text)
text = re.sub(r',\n\s*translateViewModel = translateViewModel', '', text)
text = re.sub(r',\n\s*compareViewModel = compareViewModel', '', text)

with open('android_app/app/src/main/java/com/aidict/app/MainActivity.kt', 'w') as f:
    f.write(text)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

text = re.sub(r'import com\.aidict\.app\.ui\.viewmodels\.CompareViewModel\n', '', text)
text = re.sub(r'import com\.aidict\.app\.ui\.viewmodels\.ExplainViewModel\n', '', text)
text = re.sub(r'import com\.aidict\.app\.ui\.viewmodels\.TranslateViewModel\n', '', text)

text = re.sub(r',\n\s*explainViewModel: ExplainViewModel', '', text)
text = re.sub(r',\n\s*translateViewModel: TranslateViewModel', '', text)
text = re.sub(r',\n\s*compareViewModel: CompareViewModel', '', text)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

for file in ['android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 
             'android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 
             'android_app/app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt']:
    with open(file, 'r') as f:
        text = f.read()
    text = re.sub(r'import com\.aidict\.app\.ui\.viewmodels\.CompareViewModel\n', '', text)
    text = re.sub(r'import com\.aidict\.app\.ui\.viewmodels\.ExplainViewModel\n', '', text)
    text = re.sub(r'import com\.aidict\.app\.ui\.viewmodels\.TranslateViewModel\n', '', text)
    with open(file, 'w') as f:
        f.write(text)

