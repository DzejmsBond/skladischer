package com.example.skladischer

import com.example.skladischer.data.ItemRequest
import com.example.skladischer.data.Storage
import com.example.skladischer.data.StorageRequest
import com.example.skladischer.data.User
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path

interface ApiService {
    @GET("users/{username}")
    fun getUser(@Path("username") username: String): Call<User>

    @GET("users/{username}/{storage_name}")
    fun getStorage(
        @Path("username") username: String,
        @Path("storage_name") storageName: String
    ): Call<Storage>

    @POST("users/{username}/create-storage")
    fun createStorage(
        @Path("username") username: String,
        @Body newStorage: StorageRequest
    ): Call<Void>

    @DELETE("users/{username}/{storage_name}")
    fun deleteStorage(
        @Path("username") username: String,
        @Path("storage_name") storageName: String
    ): Call<Void>

    @POST("users/{username}/{storage_name}/create-item")
    fun createItem(
        @Path("username") username: String,
        @Path("storage_name") storageName: String,
        @Body newItem: ItemRequest
    ): Call<Void>

    @DELETE("users/{username}/{storage_name}/{item_id}")
    fun deleteItem(
        @Path("username") username: String,
        @Path("storage_name") storageName: String,
        @Path("item_id") itemId: String
    ): Call<Void>



}
