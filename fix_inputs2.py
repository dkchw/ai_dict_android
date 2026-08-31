import re

# CompareScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'r') as f:
    text = f.read()

text = text.replace('viewModel.sendFollowUpMessage(text)', 'viewModel.sendFollowUpMessage(viewModel.compareInput, "compare")')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'w') as f:
    f.write(text)

# ExplainScreen
with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'r') as f:
    text = f.read()

text = text.replace('viewModel.sendFollowUpMessage(text)', 'viewModel.sendFollowUpMessage(viewModel.explainInput, "explain")')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'w') as f:
    f.write(text)

