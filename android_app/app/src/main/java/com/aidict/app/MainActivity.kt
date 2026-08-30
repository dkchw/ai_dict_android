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
import com.aidict.app.ui.viewmodels.CompareViewModel
import com.aidict.app.ui.viewmodels.ExplainViewModel
import com.aidict.app.ui.viewmodels.HistoryViewModel
import com.aidict.app.ui.viewmodels.SearchViewModel
import com.aidict.app.ui.viewmodels.SettingsViewModel
import com.aidict.app.ui.viewmodels.TranslateViewModel
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
                    modelClass.isAssignableFrom(ExplainViewModel::class.java) -> ExplainViewModel(repository, database) as T
                    modelClass.isAssignableFrom(TranslateViewModel::class.java) -> TranslateViewModel(repository, database) as T
                    modelClass.isAssignableFrom(CompareViewModel::class.java) -> CompareViewModel(repository, database) as T
                    modelClass.isAssignableFrom(HistoryViewModel::class.java) -> HistoryViewModel(database) as T
                                        modelClass.isAssignableFrom(SettingsViewModel::class.java) -> SettingsViewModel(database, repository) as T
                    modelClass.isAssignableFrom(NotesViewModel::class.java) -> NotesViewModel(database) as T
                    else -> throw IllegalArgumentException("Unknown ViewModel class")
                }
            }
        }

        setContent {
            val windowSizeClass = calculateWindowSizeClass(this)
            
            val searchViewModel: SearchViewModel = viewModel(factory = factory)
            val explainViewModel: ExplainViewModel = viewModel(factory = factory)
            val translateViewModel: TranslateViewModel = viewModel(factory = factory)
            val compareViewModel: CompareViewModel = viewModel(factory = factory)
            val historyViewModel: HistoryViewModel = viewModel(factory = factory)
                        val settingsViewModel: SettingsViewModel = viewModel(factory = factory)
            val notesViewModel: NotesViewModel = viewModel(factory = factory)
            val appViewModel: com.aidict.app.ui.viewmodels.AppViewModel = viewModel(factory = object : ViewModelProvider.Factory {
                override fun <T : ViewModel> create(modelClass: Class<T>): T {
                    return com.aidict.app.ui.viewmodels.AppViewModel(database) as T
                }
            })
            
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

            MaterialTheme(colorScheme = modifiedColorScheme) {
                Surface(color = MaterialTheme.colorScheme.background) {
                    AppNavigation(
                        windowSizeClass = windowSizeClass,
                        appViewModel = appViewModel,
                        searchViewModel = searchViewModel,
                        explainViewModel = explainViewModel,
                        translateViewModel = translateViewModel,
                        compareViewModel = compareViewModel,
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



