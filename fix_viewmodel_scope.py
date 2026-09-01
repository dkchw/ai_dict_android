import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'r') as f:
    text = f.read()

lines = text.split('\n')

target_lines = [129, 222, 322, 372, 415, 458]

for i in target_lines:
    if "viewModelScope.launch {" in lines[i - 1]:
        lines[i - 1] = lines[i - 1].replace("viewModelScope.launch {", "kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {")
    else:
        print(f"Warning: line {i} does not contain viewModelScope.launch. It has: {lines[i-1]}")

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/SearchViewModel.kt', 'w') as f:
    f.write('\n'.join(lines))
print("Fixed SearchViewModel scoping")
