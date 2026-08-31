package com.aidict.app.ui.components

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import com.halilibo.richtext.commonmark.Markdown
import com.halilibo.richtext.ui.material3.RichText

@Composable
fun MarkdownText(text: String, color: Color, modifier: Modifier = Modifier) {
    RichText(
        modifier = modifier
    ) {
        Markdown(content = text)
    }
}
