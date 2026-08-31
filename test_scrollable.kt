import androidx.compose.foundation.gestures.Orientation
import androidx.compose.foundation.gestures.scrollable
import androidx.compose.foundation.rememberScrollState
import androidx.compose.ui.Modifier

val modifier = Modifier.scrollable(rememberScrollState(), Orientation.Vertical)
