package com.example.skladischer.data

import android.content.Context
import android.util.Log
import android.widget.Toast
import com.example.skladischer.RetrofitClient
import com.example.skladischer.data.model.LoggedInUser
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.io.IOException

/**
 * Class that handles authentication w/ login credentials and retrieves user information.
 */
class LoginDataSource {

    fun fakelogin(username: String, password: String): Result<LoggedInUser> {
        try {
            val fakeUser = LoggedInUser(java.util.UUID.randomUUID().toString(), "Jane Doe")
            return Result.Success(fakeUser)
        } catch (e: Throwable) {
            return Result.Error(IOException("Error logging in", e))
        }
    }

    fun register(username: String, password: String, callback: (Result<Unit>) -> Unit) {
        RetrofitClient.apiService.register(username=username, password=password).enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    callback(Result.Success(Unit)) // Success callback
                } else {
                    callback(Result.Error(IOException("Registration failed: ${response.code()}")))
                }
            }
            override fun onFailure(call: Call<Void>, t: Throwable) {
                callback(Result.Error(IOException("Error registering", t)))
            }
        })
    }



    fun login(username: String, password: String, callback: (Result<LoggedInUser>) -> Unit) {
        RetrofitClient.apiService.login(username=username, password=password).enqueue(object : Callback<LoginResponse> {
            override fun onResponse(call: Call<LoginResponse>, response: Response<LoginResponse>) {
                if (response.isSuccessful && response.body() != null) {
                    val token = response.body()!!.access_token
                    val loggedInUser = LoggedInUser(username, token)
                    callback(Result.Success(loggedInUser)) // Success callback
                } else {
                    callback(Result.Error(IOException("Login failed: ${response.code()}")))
                }
            }
            override fun onFailure(call: Call<LoginResponse>, t: Throwable) {
                callback(Result.Error(IOException("Error logging in", t)))
            }
        })
    }



    fun logout() {
    }
}