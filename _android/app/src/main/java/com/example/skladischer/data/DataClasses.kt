package com.example.skladischer.data

data class User(
    val username: String,
    val display_name: String?,
    val storages: List<Storage>
)

data class Storage(
    val name: String,
    val content: List<Item>
)

data class Item(
    val code_id: String,
    val image_base64: String,
    val name: String,
    val amount: Int,
    val description: String?,
    val date_added: String
)

data class ItemRequest(
    val name: String,
    val amount: Int,
    val description: String?
)

data class StorageRequest(val name: String)
