package com.aidict.app.models

import kotlinx.serialization.Serializable

@Serializable
data class ExternalLink(
    val name: String,
    val url: String,
    val iconUrl: String = ""
)
