import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    content = f.read()

# Extract the block from `fun streamTranslation` to the end
match = re.search(r'        fun streamTranslation\(text: String.*', content, re.DOTALL)
if match:
    functions_block = match.group(0)
    # Remove it
    content = content.replace(functions_block, '')
    
    # ensure content ends with exactly ONE closing brace for the class
    content = content.rstrip()
    while content.endswith('}'):
        content = content[:-1].rstrip()
    content += '\n}\n'
    
    # insert functions before the last brace
    content = content[:-2] + '\n' + functions_block.replace('        fun streamTranslation', '    fun streamTranslation') + '\n}'
    
    with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
        f.write(content)
