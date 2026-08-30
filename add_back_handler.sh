sed -i '/var currentMode by remember { mutableStateOf(0) }/a \
    androidx.activity.compose.BackHandler(enabled = currentScreen != Screen.MAIN || currentMode != 0) {\n\
        if (currentScreen != Screen.MAIN) {\n\
            currentScreen = Screen.MAIN\n\
        } else if (currentMode != 0) {\n\
            currentMode = 0\n\
        }\n\
    }' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt
