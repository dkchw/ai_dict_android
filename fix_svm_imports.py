with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    lines = f.readlines()

unique_lines = []
imports = set()

for line in lines:
    if line.startswith('import '):
        if line not in imports:
            imports.add(line)
            unique_lines.append(line)
    else:
        unique_lines.append(line)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.writelines(unique_lines)
