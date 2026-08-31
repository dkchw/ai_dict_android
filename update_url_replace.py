import re

def update_replace(filename):
    with open(filename, 'r') as f:
        text = f.read()
    
    text = text.replace('link.url.replace("{word}", term.trim())', 'link.url.replace("{word}", term.trim()).replace("{{str}}", term.trim())')
    
    with open(filename, 'w') as f:
        f.write(text)

update_replace('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt')
update_replace('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt')

