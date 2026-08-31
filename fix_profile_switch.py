import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

old_click = """                                        onClick = { 
                                            appViewModel.setActiveProfile(profile)
                                            expanded = false 
                                        }"""

new_click = """                                        onClick = { 
                                            appViewModel.setActiveProfile(profile)
                                            searchViewModel.clearCurrentSearch()
                                            historyViewModel.setActiveSession(null)
                                            expanded = false 
                                        }"""

text = text.replace(old_click, new_click)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

