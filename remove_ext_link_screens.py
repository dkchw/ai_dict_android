import re

def clean_screen(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    
    # Remove collectAsState
    text = re.sub(r'val externalLinks by viewModel\.externalLinks\.collectAsState\(\)\n\s*', '', text)
    
    # Remove externalLinks arg in ChatInputBar
    text = re.sub(r'externalLinks = .*?,\n\s*', '', text)
    
    # Remove onExternalLinkClick arg
    # This might span multiple lines, let's use a regex that matches onExternalLinkClick up to the end of its block
    pattern = r'onExternalLinkClick = \{ link ->.*?context\.startActivity\(intent\)\s*\}?\s*\},\n\s*'
    text = re.sub(pattern, '', text, flags=re.DOTALL)
    
    # Additional fallback for single line or different formats
    text = re.sub(r'onExternalLinkClick = \{.*?\},\n\s*', '', text, flags=re.DOTALL)
    
    # Also clean up imports
    text = re.sub(r'import android\.content\.Intent\n', '', text)
    text = re.sub(r'import android\.net\.Uri\n', '', text)
    
    with open(file_path, 'w') as f:
        f.write(text)

clean_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/SearchScreen.kt')
clean_screen('android_app/app/src/main/java/com/aidict/app/ui/screens/CompareScreen.kt')
