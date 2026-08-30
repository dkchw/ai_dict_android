sed -i 's/androidx.activity.compose.BackHandler(enabled = currentScreen != Screen.MAIN || currentMode != 0) {/androidx.activity.compose.BackHandler(enabled = currentScreen != Screen.MAIN || currentMode != 0 || searchViewModel.uiState.value.word != null) {/' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt

sed -i 's/        } else if (currentMode != 0) {/        } else if (currentMode != 0) {\n            currentMode = 0\n        } else if (searchViewModel.uiState.value.word != null) {\n            searchViewModel.clearCurrentSearch()\n        }/' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt
# Actually, the original was:
#        } else if (currentMode != 0) {
#            currentMode = 0
#        }
