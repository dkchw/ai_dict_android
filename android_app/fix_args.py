with open('app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('viewModel.searchInput = viewModel.searchInput', 'inputTerm = viewModel.searchInput')
with open('app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt', 'w') as f: f.write(text)

with open('app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('viewModel.translateInput = viewModel.translateInput', 'inputTerm = viewModel.translateInput')
with open('app/src/main/java/com/aidict/app/ui/screens/TranslateScreen.kt', 'w') as f: f.write(text)

with open('app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('viewModel.explainInput = viewModel.explainInput', 'inputTerm = viewModel.explainInput')
with open('app/src/main/java/com/aidict/app/ui/screens/ExplainScreen.kt', 'w') as f: f.write(text)

with open('app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('viewModel.compareInput = viewModel.compareInput', 'inputTerm = viewModel.compareInput')
with open('app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt', 'w') as f: f.write(text)
