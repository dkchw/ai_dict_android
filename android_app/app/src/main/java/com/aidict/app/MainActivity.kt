package com.aidict.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.material3.windowsizeclass.ExperimentalMaterial3WindowSizeClassApi
import androidx.compose.material3.windowsizeclass.calculateWindowSizeClass
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import com.aidict.app.data.AppDatabase
import com.aidict.app.data.LlmRepository
import com.aidict.app.ui.AppNavigation
import com.aidict.app.ui.viewmodels.HistoryViewModel
import com.aidict.app.ui.viewmodels.SearchViewModel
import com.aidict.app.ui.viewmodels.SettingsViewModel
import com.aidict.app.ui.viewmodels.AppViewModel
import com.aidict.app.ui.viewmodels.NotesViewModel

class MainActivity : ComponentActivity() {
    @OptIn(ExperimentalMaterial3WindowSizeClassApi::class)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val database = AppDatabase.getDatabase(this)
        val repository = LlmRepository(database)
        
        val factory = object : ViewModelProvider.Factory {
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                return when {
                    modelClass.isAssignableFrom(SearchViewModel::class.java) -> SearchViewModel(repository, database) as T
                    modelClass.isAssignableFrom(AppViewModel::class.java) -> AppViewModel(database) as T
                    modelClass.isAssignableFrom(HistoryViewModel::class.java) -> HistoryViewModel(database) as T
                    modelClass.isAssignableFrom(SettingsViewModel::class.java) -> SettingsViewModel(database, repository) as T
                    modelClass.isAssignableFrom(NotesViewModel::class.java) -> NotesViewModel(database) as T
                    else -> throw IllegalArgumentException("Unknown ViewModel class")
                }
            }
        }

        setContent {
            val windowSizeClass = calculateWindowSizeClass(this)
            
            val appViewModel: AppViewModel = viewModel(factory = factory)
            val searchViewModel: SearchViewModel = viewModel(factory = factory)
            val historyViewModel: HistoryViewModel = viewModel(factory = factory)
            val settingsViewModel: SettingsViewModel = viewModel(factory = factory)
            val notesViewModel: NotesViewModel = viewModel(factory = factory)
            
            val isDarkMode by settingsViewModel.isDarkMode.collectAsState()
            val appTheme by settingsViewModel.appTheme.collectAsState()
            
            val colorScheme = when (appTheme) {
                "light" -> androidx.compose.material3.lightColorScheme()
                "dark" -> androidx.compose.material3.darkColorScheme()
                "nord" -> com.aidict.app.ui.theme.NordColors
                "dracula" -> com.aidict.app.ui.theme.DraculaColors
                "tokyonight" -> com.aidict.app.ui.theme.TokyoNightColors
                else -> com.aidict.app.ui.theme.TokyoNightColors // default
            }

            val dynamicColorState = androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf<androidx.compose.ui.graphics.Color?>(null) }
            val dynamicColor = dynamicColorState.value
            val modifiedColorScheme = if (dynamicColor != null) {
                colorScheme.copy(
                    primary = dynamicColor!!,
                    onPrimary = androidx.compose.ui.graphics.Color.White,
                    primaryContainer = dynamicColor!!.copy(alpha = 0.3f),
                    surfaceTint = dynamicColor!!
                )
            } else colorScheme

            val uiScaleStr by settingsViewModel.getSettingFlow("UI_SCALE", "1.0").collectAsState()
            val textScaleStr by settingsViewModel.getSettingFlow("TEXT_SIZE_SCALE", "1.0").collectAsState()
            val uiScale = uiScaleStr.toFloatOrNull() ?: 1.0f
            val textScale = textScaleStr.toFloatOrNull() ?: 1.0f
            
            val currentDensity = androidx.compose.ui.platform.LocalDensity.current
            val newDensity = androidx.compose.ui.unit.Density(
                density = currentDensity.density * uiScale,
                fontScale = currentDensity.fontScale * textScale
            )

            MaterialTheme(colorScheme = modifiedColorScheme) {
                androidx.compose.runtime.CompositionLocalProvider(
                    androidx.compose.ui.platform.LocalDensity provides newDensity
                ) {
                    Surface(color = MaterialTheme.colorScheme.background) {
                    AppNavigation(
                        appViewModel = appViewModel,
                        windowSizeClass = windowSizeClass,
                        searchViewModel = searchViewModel,
                        historyViewModel = historyViewModel,
                        settingsViewModel = settingsViewModel,
                        notesViewModel = notesViewModel,
                        onColorExtracted = { dynamicColorState.value = it }
                    )
                    }
                }
            }
        }
    }
}
