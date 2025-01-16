package com.example.skladischer.ui.login

/**
 * User details post authentication that is exposed to the UI
 */
data class LoggedInUserView(
    val username: String,
    val token: String
    //... other data fields that may be accessible to the UI
)