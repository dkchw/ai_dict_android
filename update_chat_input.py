import re

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'r') as f:
    text = f.read()

sig_old = """    onClear: (() -> Unit)? = null,
    modifier: Modifier = Modifier
) {"""

sig_new = """    onClear: (() -> Unit)? = null,
    autoNewSearch: Boolean = false,
    onToggleAutoNewSearch: (() -> Unit)? = null,
    enterToSend: Boolean = false,
    modifier: Modifier = Modifier
) {"""

text = text.replace(sig_old, sig_new)

clear_old = """                if (onClear != null) {
                    IconButton(
                        onClick = onClear, 
                        modifier = Modifier
                            .padding(bottom = 8.dp, start = 8.dp, end = 8.dp)
                            .background(MaterialTheme.colorScheme.secondaryContainer, CircleShape)
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "New Search", tint = MaterialTheme.colorScheme.onSecondaryContainer)
                    }
                }"""

clear_new = """                if (onClear != null) {
                    androidx.compose.foundation.layout.Box(
                        contentAlignment = Alignment.Center,
                        modifier = Modifier
                            .padding(bottom = 8.dp, start = 8.dp, end = 8.dp)
                            .size(40.dp)
                            .background(if (autoNewSearch) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.secondaryContainer, CircleShape)
                            .androidx.compose.ui.draw.clip(CircleShape)
                            .androidx.compose.foundation.ExperimentalFoundationApi::class.let {
                                @OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
                                Modifier.androidx.compose.foundation.combinedClickable(
                                    onClick = onClear,
                                    onLongClick = onToggleAutoNewSearch
                                )
                            }
                    ) {
                        Icon(
                            if (autoNewSearch) Icons.Default.Bolt else Icons.Default.Add, 
                            contentDescription = "New Search", 
                            tint = if (autoNewSearch) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSecondaryContainer,
                            modifier = Modifier.size(24.dp)
                        )
                    }
                }"""

text = text.replace(clear_old, clear_new)

field_old = """                OutlinedTextField(
                    value = inputTerm,
                    onValueChange = onValueChange,
                    placeholder = { Text(placeholder) },
                    modifier = Modifier.weight(1f),
                    minLines = 1,
                    maxLines = 4,
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Color.Transparent,
                        unfocusedBorderColor = Color.Transparent,
                        focusedContainerColor = Color.Transparent,
                        unfocusedContainerColor = Color.Transparent
                    )
                )"""

field_new = """                OutlinedTextField(
                    value = inputTerm,
                    onValueChange = onValueChange,
                    placeholder = { Text(placeholder) },
                    modifier = Modifier.weight(1f),
                    minLines = 1,
                    maxLines = 4,
                    keyboardOptions = androidx.compose.foundation.text.KeyboardOptions.Default.copy(
                        imeAction = if (enterToSend) androidx.compose.ui.text.input.ImeAction.Send else androidx.compose.ui.text.input.ImeAction.Default
                    ),
                    keyboardActions = androidx.compose.foundation.text.KeyboardActions(
                        onSend = { if (inputTerm.isNotBlank() && !isLoading) onSend() }
                    ),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Color.Transparent,
                        unfocusedBorderColor = Color.Transparent,
                        focusedContainerColor = Color.Transparent,
                        unfocusedContainerColor = Color.Transparent
                    )
                )"""

text = text.replace(field_old, field_new)

with open('android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt', 'w') as f:
    f.write(text)

