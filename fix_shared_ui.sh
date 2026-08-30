sed -i '/import androidx.compose.material.icons.filled.ArrowDropDown/a import androidx.compose.material.icons.filled.Add' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt

sed -i 's/onTargetLangChange: ((String) -> Unit)? = null/onTargetLangChange: ((String) -> Unit)? = null,\n    onClear: (() -> Unit)? = null/' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt

sed -i '/OutlinedTextField(/i \
                if (onClear != null) {\n\
                    IconButton(onClick = onClear, modifier = Modifier.padding(bottom = 8.dp)) {\n\
                        Icon(Icons.Default.Add, contentDescription = "New Search", tint = MaterialTheme.colorScheme.primary)\n\
                    }\n\
                }' android_app/app/src/main/java/com/aidict/app/ui/components/SharedUI.kt
