import re

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'r') as f:
    text = f.read()

# I will fix the dangling `.stateIn` by moving the new block to AFTER it.
# First, remove the dangling line:
text = text.replace('    }\n        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())', '    }')

# Now, we need to append `.stateIn(viewModelScope, SharingStarted.Lazily, emptyList())` to `val sessions = ...` line.
# Wait, let's just find the `val sessions` line and append it.
pattern = r'val sessions = activeProfileId\.flatMapLatest \{ pid -> database\.appDao\(\)\.getSessions\(pid\.toLong\(\)\) \}'
text = re.sub(pattern, r'\g<0>\n        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())', text)

with open('android_app/app/src/main/java/com/aidict/app/ui/viewmodels/HistoryViewModel.kt', 'w') as f:
    f.write(text)
