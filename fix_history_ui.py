import re

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'r') as f:
    hs = f.read()

imports = """import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalDensity
"""
hs = hs.replace('import androidx.compose.ui.Alignment', imports + 'import androidx.compose.ui.Alignment')

layout_block = """    val splitFraction by viewModel.splitFraction.collectAsState()
    val configuration = LocalConfiguration.current
    val density = LocalDensity.current

    if (isTablet) {
        val totalWidthDp = configuration.screenWidthDp.dp
        Row(modifier = modifier.fillMaxSize()) {
            Box(modifier = Modifier.weight(if (selectedWord != null) splitFraction else 1f)) { listContent() }
            if (selectedWord != null) {
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .width(8.dp)
                        .background(MaterialTheme.colorScheme.outlineVariant)
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                val dragAmountFraction = dragAmount.x / (totalWidthDp.toPx())
                                val newFraction = (splitFraction + dragAmountFraction).coerceIn(0.2f, 0.8f)
                                viewModel.updateSplitFraction(newFraction)
                            }
                        }
                ) {
                    VerticalDivider(modifier = Modifier.align(Alignment.Center))
                }
                Box(modifier = Modifier.weight(1f - splitFraction)) { detailContent() }
            }
        }
    } else {
        val totalHeightDp = configuration.screenHeightDp.dp
        Column(modifier = modifier.fillMaxSize()) {
            Box(modifier = Modifier.weight(if (selectedWord != null) splitFraction else 1f)) { listContent() }
            if (selectedWord != null) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(8.dp)
                        .background(MaterialTheme.colorScheme.outlineVariant)
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                val dragAmountFraction = dragAmount.y / (totalHeightDp.toPx())
                                val newFraction = (splitFraction + dragAmountFraction).coerceIn(0.2f, 0.8f)
                                viewModel.updateSplitFraction(newFraction)
                            }
                        }
                ) {
                    HorizontalDivider(modifier = Modifier.align(Alignment.Center))
                }
                Box(modifier = Modifier.weight(1f - splitFraction)) { detailContent() }
            }
        }
    }"""

pattern = r'    if \(isTablet\) \{\n        Row\(modifier = modifier\.fillMaxSize\(\)\) \{\n            Box\(modifier = Modifier\.weight\(1f\)\) \{ listContent\(\) \}\n            if \(selectedWord != null\) \{\n                VerticalDivider\(\)\n                Box\(modifier = Modifier\.weight\(1f\)\) \{ detailContent\(\) \}\n            \}\n        \}\n    \} else \{\n        Column\(modifier = modifier\.fillMaxSize\(\)\) \{\n            Box\(modifier = Modifier\.weight\(if \(selectedWord != null\) 1f else 2f\)\) \{ listContent\(\) \}\n            if \(selectedWord != null\) \{\n                HorizontalDivider\(\)\n                Box\(modifier = Modifier\.weight\(1f\)\) \{ detailContent\(\) \}\n            \}\n        \}\n    \}'

hs = re.sub(pattern, layout_block, hs, flags=re.DOTALL)

with open('android_app/app/src/main/java/com/aidict/app/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(hs)
