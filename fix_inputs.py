import re

# CompareScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'r') as f:
    text = f.read()

text = text.replace('var text by remember { mutableStateOf("") }', '')
text = text.replace('inputTerm = text,', 'inputTerm = viewModel.compareInput,')
text = text.replace('onValueChange = { text = it },', 'onValueChange = { viewModel.compareInput = it },')
text = text.replace('viewModel.sendFollowUpMessage(text, "compare")', 'viewModel.sendFollowUpMessage(viewModel.compareInput, "compare")')
text = text.replace('viewModel.streamCompare(text, profileId); text = ""', 'viewModel.streamCompare(viewModel.compareInput, profileId); viewModel.compareInput = ""')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'w') as f:
    f.write(text)

# ExplainScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'r') as f:
    text = f.read()

text = text.replace('var text by remember { mutableStateOf("") }', '')
text = text.replace('inputTerm = text,', 'inputTerm = viewModel.explainInput,')
text = text.replace('onValueChange = { text = it },', 'onValueChange = { viewModel.explainInput = it },')
text = text.replace('viewModel.sendFollowUpMessage(text, "explain")', 'viewModel.sendFollowUpMessage(viewModel.explainInput, "explain")')
text = text.replace('viewModel.streamExplain(text, profileId); text = ""', 'viewModel.streamExplain(viewModel.explainInput, profileId); viewModel.explainInput = ""')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'w') as f:
    f.write(text)
