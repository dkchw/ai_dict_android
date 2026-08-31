import re

def update_defaults(filename):
    with open(filename, 'r') as f:
        text = f.read()
    
    text = text.replace('https://dictionary.cambridge.org/dictionary/english/{word}', 'https://dictionary.cambridge.org/dictionary/english/{{str}}')
    text = text.replace('https://www.google.com/search?q={word}', 'https://www.google.com/search?q={{str}}')
    text = text.replace('https://en.wikipedia.org/wiki/{word}', 'https://en.wikipedia.org/wiki/{{str}}')
    
    with open(filename, 'w') as f:
        f.write(text)

update_defaults('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SettingsViewModel.kt')
update_defaults('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt')

