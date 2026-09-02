import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    text = f.read()

text = text.replace('Text(\n                    text = "Searches: ${selectedWord!!.searchCount} | Views: ${selectedWord!!.viewCount}",', 
                    'Text(\n                    text = "Searches: ${selectedWord!!.searchCount} | Views: ${selectedWord!!.viewCount} | Gens: ${selectedWord!!.generationCount}",')

# Some places it might be on the same line depending on formatting.
text = text.replace('text = "Searches: ${selectedWord!!.searchCount} | Views: ${selectedWord!!.viewCount}"', 
                    'text = "Searches: ${selectedWord!!.searchCount} | Views: ${selectedWord!!.viewCount} | Gens: ${selectedWord!!.generationCount}"')

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(text)

print("Updated stats in HistoryScreen")
