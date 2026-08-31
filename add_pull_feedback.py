import re

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'r') as f:
    text = f.read()

old_pull = """                        androidx.compose.material3.pulltorefresh.PullToRefreshContainer(
                            state = pullRefreshState,
                            modifier = Modifier.align(Alignment.TopCenter)
                        )
                    }
                }
            }
        }
    }
}"""

new_pull = """                        androidx.compose.material3.pulltorefresh.PullToRefreshContainer(
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
                                    text = if (isHardPull) "Release for Settings" else "Pull further for Settings",
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
}"""

text = text.replace(old_pull, new_pull)

with open('android_app/app/src/main/java/com/aidict/app/ui/AppNavigation.kt', 'w') as f:
    f.write(text)

