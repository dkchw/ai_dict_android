with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    content = f.read()

# count total '{' and '}'
open_count = content.count('{')
close_count = content.count('}')

# remove from end if close_count > open_count
while close_count > open_count:
    last_brace_idx = content.rfind('}')
    content = content[:last_brace_idx] + content[last_brace_idx+1:]
    close_count -= 1

# add to end if open_count > close_count
while open_count > close_count:
    content += '\n}'
    close_count += 1

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write(content)
