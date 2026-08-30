package com.aidict.app.ui.components

import androidx.compose.material3.Text
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.withStyle

fun parseMarkdown(text: String, codeColor: Color): AnnotatedString {
    return buildAnnotatedString {
        var i = 0
        while (i < text.length) {
            when {
                // Code blocks (simplified)
                text.startsWith("```", i) -> {
                    val endIdx = text.indexOf("```", i + 3)
                    if (endIdx != -1) {
                        withStyle(SpanStyle(fontFamily = FontFamily.Monospace, background = codeColor.copy(alpha = 0.3f))) {
                            append(text.substring(i + 3, endIdx).trim('\n'))
                        }
                        i = endIdx + 3
                    } else {
                        append("```")
                        i += 3
                    }
                }
                // Inline code
                text.startsWith("`", i) -> {
                    val endIdx = text.indexOf("`", i + 1)
                    if (endIdx != -1) {
                        withStyle(SpanStyle(fontFamily = FontFamily.Monospace, background = codeColor.copy(alpha = 0.3f))) {
                            append(text.substring(i + 1, endIdx))
                        }
                        i = endIdx + 1
                    } else {
                        append("`")
                        i += 1
                    }
                }
                // Bold
                text.startsWith("**", i) -> {
                    val endIdx = text.indexOf("**", i + 2)
                    if (endIdx != -1) {
                        withStyle(SpanStyle(fontWeight = FontWeight.Bold)) {
                            append(text.substring(i + 2, endIdx))
                        }
                        i = endIdx + 2
                    } else {
                        append("**")
                        i += 2
                    }
                }
                // Italic
                text.startsWith("*", i) -> {
                    val endIdx = text.indexOf("*", i + 1)
                    if (endIdx != -1 && text.getOrNull(i+1) != ' ' && text.getOrNull(endIdx-1) != ' ') {
                        withStyle(SpanStyle(fontStyle = FontStyle.Italic)) {
                            append(text.substring(i + 1, endIdx))
                        }
                        i = endIdx + 1
                    } else {
                        append("*")
                        i += 1
                    }
                }
                else -> {
                    append(text[i])
                    i++
                }
            }
        }
    }
}

@Composable
fun MarkdownText(text: String, color: Color, modifier: Modifier = Modifier) {
    Text(
        text = parseMarkdown(text, MaterialTheme.colorScheme.primary),
        color = color,
        modifier = modifier
    )
}
