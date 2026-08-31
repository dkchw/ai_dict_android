import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun PulsingDots(modifier: Modifier = Modifier) {
    val transition = rememberInfiniteTransition()
    val scales = (0..2).map { index ->
        transition.animateFloat(
            initialValue = 0.5f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 600, delayMillis = index * 200, easing = LinearEasing),
                repeatMode = RepeatMode.Reverse
            )
        )
    }

    Row(modifier = modifier.padding(16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        scales.forEach { scale ->
            Box(
                modifier = Modifier
                    .size(8.dp)
                    .background(MaterialTheme.colorScheme.primary.copy(alpha = scale.value), CircleShape)
            )
        }
    }
}
