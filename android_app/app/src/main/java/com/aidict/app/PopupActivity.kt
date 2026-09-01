package com.aidict.app

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.material3.windowsizeclass.ExperimentalMaterial3WindowSizeClassApi
import androidx.compose.material3.windowsizeclass.calculateWindowSizeClass
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
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

class PopupActivity : ComponentActivity() {
    @OptIn(ExperimentalMaterial3WindowSizeClassApi::class)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val textExtra = intent.getCharSequenceExtra(Intent.EXTRA_PROCESS_TEXT)?.toString() ?: ""
        
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
            
            LaunchedEffect(Unit) {
                if (textExtra.isNotBlank() && searchViewModel.searchInput.isBlank()) {
                    searchViewModel.searchInput = textExtra
                }
            }
            
            val isDarkMode by settingsViewModel.isDarkMode.collectAsState()
            val appTheme by settingsViewModel.appTheme.collectAsState()
            
            val colorScheme = when (appTheme) {
                "light" -> lightColorScheme()
                "dark" -> darkColorScheme()
                "nord" -> com.aidict.app.ui.theme.NordColors
                "dracula" -> com.aidict.app.ui.theme.DraculaColors
                "tokyonight" -> com.aidict.app.ui.theme.TokyoNightColors
                else -> com.aidict.app.ui.theme.TokyoNightColors
            }

            val dynamicColorState = remember { androidx.compose.runtime.mutableStateOf<Color?>(null) }
            val dynamicColor = dynamicColorState.value
            val modifiedColorScheme = if (dynamicColor != null) {
                colorScheme.copy(
                    primary = dynamicColor!!,
                    onPrimary = Color.White,
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
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(Color.Black.copy(alpha = 0.5f))
                            .clickable(
                                interactionSource = remember { MutableInteractionSource() },
                                indication = null
                            ) {
                                finish()
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = MaterialTheme.colorScheme.background,
                            modifier = Modifier
                                .fillMaxWidth(0.95f)
                                .fillMaxHeight(0.9f)
                                .clickable(
                                    interactionSource = remember { MutableInteractionSource() },
                                    indication = null
                                ) {
                                    // Do nothing on internal clicks
                                }
                                .clip(RoundedCornerShape(16.dp))
                        ) {
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
}
