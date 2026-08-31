package com.aidict.app.ui

import androidx.compose.material3.windowsizeclass.WindowSizeClass
import androidx.compose.foundation.background
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.windowsizeclass.WindowWidthSizeClass
import androidx.compose.runtime.*
import kotlinx.coroutines.launch
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.foundation.ExperimentalFoundationApi

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.clickable
import androidx.compose.material3.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.blur
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Alignment
import com.aidict.app.ui.screens.CompareScreen
import com.aidict.app.ui.screens.ExplainScreen
import com.aidict.app.ui.screens.HistoryScreen
import com.aidict.app.ui.screens.SearchScreen
import com.aidict.app.ui.screens.SettingsScreen
import com.aidict.app.ui.screens.TranslateScreen
import com.aidict.app.ui.screens.NotesScreen
import com.aidict.app.ui.viewmodels.HistoryViewModel
import com.aidict.app.ui.viewmodels.SearchViewModel
import com.aidict.app.ui.viewmodels.SettingsViewModel
import com.aidict.app.ui.viewmodels.NotesViewModel

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Translate
import androidx.compose.material.icons.filled.EditNote
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.automirrored.filled.CompareArrows
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.ui.graphics.vector.ImageVector

data class TabItem(val title: String, val icon: ImageVector)

enum class Screen { MAIN, HISTORY, SETTINGS, NOTES }

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.foundation.layout.ExperimentalLayoutApi::class, ExperimentalFoundationApi::class)
@Composable
fun AppNavigation(
    windowSizeClass: WindowSizeClass,
    appViewModel: com.aidict.app.ui.viewmodels.AppViewModel,
    searchViewModel: SearchViewModel,
    historyViewModel: HistoryViewModel,
    settingsViewModel: SettingsViewModel,
    notesViewModel: NotesViewModel,
    onColorExtracted: (androidx.compose.ui.graphics.Color?) -> Unit
) {
    val isExpanded = windowSizeClass.widthSizeClass == WindowWidthSizeClass.Expanded
    
    var currentScreen by remember { mutableStateOf(Screen.MAIN) }
    val coroutineScope = rememberCoroutineScope()
    val pagerState = androidx.compose.foundation.pager.rememberPagerState(initialPage = 0, pageCount = { 4 })
    val currentMode = pagerState.targetPage


    val currentSearchState = when (currentMode) {
        0 -> searchViewModel.dictState.collectAsState().value
        1 -> searchViewModel.compareState.collectAsState().value
        2 -> searchViewModel.translateState.collectAsState().value
        3 -> searchViewModel.explainState.collectAsState().value
        else -> searchViewModel.dictState.collectAsState().value
    }

    androidx.activity.compose.BackHandler(enabled = currentScreen != Screen.MAIN || currentMode != 0 || currentSearchState.word != null) {

        if (currentScreen != Screen.MAIN) {

            currentScreen = Screen.MAIN

        } else if (currentMode != 0) {
            coroutineScope.launch { pagerState.animateScrollToPage(0) }
        } else if (currentSearchState.word != null) {
            searchViewModel.clearCurrentSearch()
        }
    }
    
    val appState by appViewModel.uiState.collectAsState()

    val bgDict by settingsViewModel.bgDict.collectAsState()
    val bgCompare by settingsViewModel.bgCompare.collectAsState()
    val bgTranslate by settingsViewModel.bgTranslate.collectAsState()
    val bgExplain by settingsViewModel.bgExplain.collectAsState()
    val bgBlur by settingsViewModel.bgBlurRadius.collectAsState()
        val bgUniversal by settingsViewModel.bgUniversal.collectAsState()
    val bgOpacity by settingsViewModel.bgOpacity.collectAsState()

    val activeBg = when {
        currentScreen != Screen.MAIN -> null
        currentMode == 0 -> bgDict ?: bgUniversal
        currentMode == 1 -> bgCompare ?: bgUniversal
        currentMode == 2 -> bgTranslate ?: bgUniversal
        currentMode == 3 -> bgExplain ?: bgUniversal
        else -> null
    }

    LaunchedEffect(activeBg) { if (activeBg == null) onColorExtracted(null) }

    Box(modifier = Modifier.fillMaxSize()) {

        if (activeBg != null) {
            coil.compose.AsyncImage(
                model = activeBg,
                contentDescription = null,
                contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                modifier = Modifier.fillMaxSize().blur(bgBlur.dp).alpha(bgOpacity),
                onSuccess = { state ->
                    val bitmap = (state.result.drawable as? android.graphics.drawable.BitmapDrawable)?.bitmap
                    if (bitmap != null) {
                        androidx.palette.graphics.Palette.from(bitmap).generate { palette ->
                            val swatch = palette?.vibrantSwatch ?: palette?.mutedSwatch ?: palette?.dominantSwatch
                            if (swatch != null) {
                                onColorExtracted(androidx.compose.ui.graphics.Color(swatch.rgb))
                            }
                        }
                    }
                }
            )
        }
    val modes = listOf(
        TabItem("Dict", Icons.Default.Search),
        TabItem("Compare", Icons.AutoMirrored.Filled.CompareArrows),
        TabItem("Translate", Icons.Default.Translate),
        TabItem("Explain", Icons.Default.Description)
    )

        val quoteMode by settingsViewModel.quoteMode.collectAsState()
        val quoteStyleStr by settingsViewModel.quoteStyle.collectAsState()
        val fontFamily = when(quoteStyleStr) { "Serif" -> androidx.compose.ui.text.font.FontFamily.Serif; "Sans Serif" -> androidx.compose.ui.text.font.FontFamily.SansSerif; "Monospace" -> androidx.compose.ui.text.font.FontFamily.Monospace; "Cursive" -> androidx.compose.ui.text.font.FontFamily.Cursive; else -> androidx.compose.ui.text.font.FontFamily.Default }

        val quotesList by settingsViewModel.allQuotes.collectAsState()
        val shuffleEnabledQuotes by settingsViewModel.shuffleEnabledQuotes.collectAsState()
        
        val activeShuffleList = shuffleEnabledQuotes?.filter { it in quotesList }?.takeIf { it.isNotEmpty() } ?: quotesList

        var shuffledQuote by remember { mutableStateOf(activeShuffleList.randomOrNull() ?: "") }

        LaunchedEffect(currentMode, activeShuffleList) { if (quoteMode == "Shuffle") shuffledQuote = activeShuffleList.randomOrNull() ?: "" }

        val displayQuote = when (quoteMode) { "None" -> null; "Shuffle" -> shuffledQuote; else -> quoteMode }



        if (displayQuote != null && currentScreen == Screen.MAIN) {

            Box(modifier = Modifier.fillMaxSize().padding(bottom = 120.dp), contentAlignment = Alignment.Center) {

                Text(

                    text = displayQuote,

                    style = MaterialTheme.typography.headlineMedium.copy(fontFamily = fontFamily, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic),

                    color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.3f),

                    textAlign = androidx.compose.ui.text.style.TextAlign.Center,

                    modifier = Modifier.padding(32.dp)

                )

            }

        }
    Scaffold(containerColor = androidx.compose.ui.graphics.Color.Transparent,
        topBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp)
                    .background(androidx.compose.ui.graphics.Color.Transparent)
                    .padding(horizontal = 4.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (currentScreen == Screen.MAIN) {
                        IconButton(onClick = { 
                            appViewModel.clearHistoryUnseen()
                            currentScreen = Screen.HISTORY 
                        }) {
                            if (appState.unseenHistoryItems > 0) {
                                BadgedBox(badge = { Badge { Text(appState.unseenHistoryItems.toString()) } }) {
                                    Icon(Icons.Default.History, contentDescription = "History")
                                }
                            } else {
                                Icon(Icons.Default.History, contentDescription = "History")
                            }
                        }
                    } else {
                        IconButton(onClick = { currentScreen = Screen.MAIN }) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    }
                    
                    Column(modifier = Modifier.padding(start = 4.dp), horizontalAlignment = Alignment.Start) {
                        Text("AI Dict", style = MaterialTheme.typography.titleMedium)
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            Row(
                                verticalAlignment = Alignment.CenterVertically, 
                                modifier = Modifier.clickable { expanded = true }.padding(vertical = 2.dp),
                                horizontalArrangement = Arrangement.Start
                            ) {
                                Text(appState.activeProfile?.name ?: "Default", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                                Icon(Icons.Default.ArrowDropDown, contentDescription = "Select", modifier = Modifier.size(14.dp), tint = MaterialTheme.colorScheme.primary)
                            }
                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                appState.profiles.forEach { profile ->
                                    DropdownMenuItem(
                                        text = { Text(profile.name) },
                                        onClick = { 
                                            appViewModel.setActiveProfile(profile)
                                            searchViewModel.clearCurrentSearch()
                                            historyViewModel.setActiveSession(null)
                                            expanded = false 
                                        }
                                    )
                                }
                            }
                        }
                    }
                }
                
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (currentScreen == Screen.MAIN) {
                        androidx.compose.material3.Text(
                            text = modes[currentMode].title,
                            style = androidx.compose.material3.MaterialTheme.typography.titleSmall,
                            modifier = androidx.compose.ui.Modifier.padding(end = 8.dp),
                            color = androidx.compose.material3.MaterialTheme.colorScheme.primary.copy(alpha = 0.7f)
                        )
                        IconButton(onClick = { currentScreen = Screen.NOTES }) {
                            Icon(Icons.Default.EditNote, contentDescription = "Notes")
                        }
                        IconButton(onClick = { currentScreen = Screen.SETTINGS }) {
                            Icon(Icons.Default.Settings, contentDescription = "Settings")
                        }
                    } else {
                        Spacer(modifier = Modifier.width(48.dp))
                    }
                }
            }
        },
        bottomBar = {
            if (currentScreen == Screen.MAIN) {
                Row(
                    modifier = Modifier.fillMaxWidth().height(48.dp).background(androidx.compose.ui.graphics.Color.Transparent),
                    horizontalArrangement = Arrangement.SpaceEvenly,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    modes.forEachIndexed { index, tab ->
                        val isSelected = currentMode == index
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier
                                .clickable {
                                    if (currentMode != index) {
                                        coroutineScope.launch { pagerState.animateScrollToPage(index) }
                                        searchViewModel.clearCurrentSearch()
                                    }
                                }
                                .padding(horizontal = 16.dp, vertical = 4.dp)
                        ) {
                            Icon(
                                tab.icon, 
                                contentDescription = tab.title, 
                                tint = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.size(24.dp)
                            )
                            Text(
                                tab.title, 
                                style = MaterialTheme.typography.labelSmall,
                                color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    ) { paddingValues ->
        Surface(modifier = Modifier.padding(paddingValues).fillMaxSize(), color = androidx.compose.ui.graphics.Color.Transparent) {
            when (currentScreen) {
                                Screen.SETTINGS -> SettingsScreen(settingsViewModel)
                Screen.NOTES -> NotesScreen(notesViewModel)
                Screen.HISTORY -> {
                    val modeStr = when (currentMode) {
                        0 -> "dict"
                        1 -> "compare"
                        2 -> "translate"
                        3 -> "explain"
                        else -> "dict"
                    }
                    LaunchedEffect(currentMode) {
                        historyViewModel.setMode(modeStr)
                    }
                    LaunchedEffect(appState.activeProfile?.id) {
                        historyViewModel.setActiveProfileId(appState.activeProfile?.id ?: 1)
                    }
                                        HistoryScreen(
                        appViewModel = appViewModel,
                        onNavigateToChat = { word ->
                            searchViewModel.loadWord(word)
                            val modeInt = when (word.mode) {
                                "dict" -> 0
                                "compare" -> 1
                                "translate" -> 2
                                "explain" -> 3
                                else -> 0
                            }
                            coroutineScope.launch { pagerState.scrollToPage(modeInt) }
                            currentScreen = Screen.MAIN
                        },
                        viewModel = historyViewModel,
                        windowSizeClass = windowSizeClass
                    )
                }
                Screen.MAIN -> {
                    val pid = appState.activeProfile?.id ?: 1
                    
                    val pullRefreshState = androidx.compose.material3.pulltorefresh.rememberPullToRefreshState()
                    var maxProgress by remember { mutableStateOf(0f) }
                    
                    if (pullRefreshState.progress > maxProgress) {
                        maxProgress = pullRefreshState.progress
                    }
                    if (pullRefreshState.progress == 0f && !pullRefreshState.isRefreshing) {
                        maxProgress = 0f
                    }
                    
                    if (pullRefreshState.isRefreshing) {
                        LaunchedEffect(Unit) {
                            if (maxProgress > 1.3f) {
                                currentScreen = Screen.SETTINGS
                            } else {
                                appViewModel.clearHistoryUnseen()
                                currentScreen = Screen.HISTORY
                            }
                            pullRefreshState.endRefresh()
                            maxProgress = 0f
                        }
                    }
                    
                    Box(modifier = Modifier.fillMaxSize().nestedScroll(pullRefreshState.nestedScrollConnection)) {
                        androidx.compose.foundation.pager.HorizontalPager(
                            state = pagerState,
                            modifier = Modifier.fillMaxSize(),
                            beyondBoundsPageCount = 1
                        ) { page ->
                            when (page) {
                                0 -> SearchScreen(searchViewModel, pid)
                                1 -> CompareScreen(searchViewModel, pid)
                                2 -> TranslateScreen(searchViewModel, pid)
                                3 -> ExplainScreen(searchViewModel, pid)
                            }
                        }
                        
                        androidx.compose.material3.pulltorefresh.PullToRefreshContainer(
                            state = pullRefreshState,
                            modifier = Modifier.align(Alignment.TopCenter)
                        )
                        
                        if (pullRefreshState.progress > 0f) {
                            val isHardPull = pullRefreshState.progress > 1.3f
                            Box(modifier = Modifier
                                .align(Alignment.TopCenter)
                                .padding(top = 90.dp)
                                .background(
                                    color = if (isHardPull) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant, 
                                    shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp)
                                )
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                            ) {
                                Text(
                                    text = if (isHardPull) "Release for Settings" else "Release for History",
                                    color = if (isHardPull) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant,
                                    style = MaterialTheme.typography.labelMedium
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}
}
