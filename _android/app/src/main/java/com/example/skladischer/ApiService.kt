package com.example.skladischer

import com.example.skladischer.data.ItemRequest
import com.example.skladischer.data.LoginRequest
import com.example.skladischer.data.LoginResponse
import com.example.skladischer.data.RegistrationRequest
import com.example.skladischer.data.Storage
import com.example.skladischer.data.StorageRequest
import com.example.skladischer.data.User
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.Path

interface ApiService {
    @FormUrlEncoded
    @POST("credentials/create-credentials")
    fun register(
        @Field("grant_type") grant_type: String = "password",
        @Field("username") username: String,
        @Field("password") password: String,
        @Field("scope") scope: String = "",
        @Field("client_id") clientId: String = "",
        @Field("client_secret") clientSecret: String = ""
    ): Call<Void>

//    @POST("credentials/login")
//    fun login(@Body loginData: LoginRequest): Call<LoginResponse>
    @FormUrlEncoded
    @POST("credentials/login")
    fun login(
        @Field("grant_type") grant_type: String = "password",
        @Field("username") username: String,
        @Field("password") password: String,
        @Field("scope") scope: String = "",
        @Field("client_id") clientId: String = "",
        @Field("client_secret") clientSecret: String = ""
    ): Call<LoginResponse>


    @GET("users/{username}")
    fun getUser(@Header("Authorization") token: String, @Path("username") username: String): Call<User>

    @GET("users/{username}/{storage_name}")
    fun getStorage(
        @Header("Authorization") token: String,
        @Path("username") username: String,
        @Path("storage_name") storageName: String
    ): Call<Storage>

    @POST("users/{username}/create-storage")
    fun createStorage(
        @Header("Authorization") token: String,
        @Path("username") username: String,
        @Body newStorage: StorageRequest
    ): Call<Void>

    @DELETE("users/{username}/{storage_name}")
    fun deleteStorage(
        @Header("Authorization") token: String,
        @Path("username") username: String,
        @Path("storage_name") storageName: String
    ): Call<Void>

    @POST("users/{username}/{storage_name}/create-item")
    fun createItem(
        @Header("Authorization") token: String,
        @Path("username") username: String,
        @Path("storage_name") storageName: String,
        @Body newItem: ItemRequest
    ): Call<Void>

    @DELETE("users/{username}/{storage_name}/{item_id}")
    fun deleteItem(
        @Header("Authorization") token: String,
        @Path("username") username: String,
        @Path("storage_name") storageName: String,
        @Path("item_id") itemId: String
    ): Call<Void>



}
