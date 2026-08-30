sed -i 's/TopAppBar(/TopAppBar(\ncolors = TopAppBarDefaults.topAppBarColors(containerColor = androidx.compose.ui.graphics.Color.Transparent),\n/' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt
sed -i 's/NavigationBar {/NavigationBar(containerColor = androidx.compose.ui.graphics.Color.Transparent) {/' android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt
