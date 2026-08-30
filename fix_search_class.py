with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    content = f.read()

# find the first "fun streamTranslation"
import re
match = re.search(r'    fun streamTranslation\(text: String.*', content, re.DOTALL)
if match:
    functions_block = match.group(0)
    # remove it from the end
    content = content.replace(functions_block, '')
    
    # insert it before the last closing brace
    # find the last closing brace
    last_brace_idx = content.rfind('}')
    if last_brace_idx != -1:
        content = content[:last_brace_idx] + functions_block + '\n' + content[last_brace_idx:]
    
    with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
        f.write(content)
