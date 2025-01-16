package com.example.skladischer

import android.content.Context
import android.widget.Toast
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.skladischer.data.User
import com.example.skladischer.data.Storage
import com.example.skladischer.data.Item
import com.example.skladischer.data.ItemRequest
import com.example.skladischer.data.StorageRequest
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class UserViewModel : ViewModel() {
    var username = "testuser"
    var display_name = "none"

    private val _user = MutableLiveData<User?>()
    val user: LiveData<User?> get() = _user

    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> get() = _error

    private val _storages = MutableLiveData<List<Storage>>()
    val storages: LiveData<List<Storage>> get() = _storages

    private val _items = MutableLiveData<List<Item>>()
    val items: LiveData<List<Item>> get() = _items

    private val _selectedStorage = MutableLiveData<Storage?>()
    val selectedStorage: LiveData<Storage?> get() = _selectedStorage

    fun fetchUser(uUsername: String) {
        RetrofitClient.apiService.getUser(uUsername).enqueue(object : Callback<User> {
            override fun onResponse(call: Call<User>, response: Response<User>) {
                if (response.isSuccessful) {
                    val gotUser = response.body()
                    if (gotUser != null) {
                        _user.value = gotUser
                        _storages.value = gotUser.storages

                        username = _user.value!!.username
                        display_name = _user.value!!.display_name.toString()
                    }
                } else {
                    _error.value = "Error: ${response.code()}"
                }
            }

            override fun onFailure(call: Call<User>, t: Throwable) {
                _error.value = "Failed to fetch user: ${t.message}"
            }
        })
    }

    fun selectStorage(storage: Storage, context: Context) {
        _selectedStorage.value = storage
        fetchStorage(context)
        _items.value = storage.content
    }


    fun fetchStorage(context: Context) {
        val storageName = _selectedStorage.value!!.name
        RetrofitClient.apiService.getStorage(username, storageName).enqueue(object : Callback<Storage> {
            override fun onResponse(call: Call<Storage>, response: Response<Storage>) {
                if (response.isSuccessful) {
                    _selectedStorage.value = response.body() // Update LiveData with the new storage data
                } else {
                    // Handle API error response
                    Toast.makeText(context, "Failed to fetch storage: ${response.code()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Storage>, t: Throwable) {
                // Handle network errors
                Toast.makeText(context, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }

    fun addStorage(storageName: String, context: Context) {
        val newStorage = StorageRequest(name = storageName)

        RetrofitClient.apiService.createStorage(username, newStorage).enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    Toast.makeText(context, "Storage added successfully", Toast.LENGTH_SHORT).show()
                    // Fetch updated user data
                    fetchUser(username)
                } else {
                    Toast.makeText(context, "Failed to add storage: ${response.code()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Void>, t: Throwable) {
                Toast.makeText(context, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }

    fun deleteStorage(storageName: String, context: Context) {
        RetrofitClient.apiService.deleteStorage(username, storageName).enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    Toast.makeText(context, "Storage deleted successfully", Toast.LENGTH_SHORT).show()
                    // Refresh the user data after deletion
                    fetchUser(username)
                } else {
                    Toast.makeText(context, "Failed to delete storage: ${response.code()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Void>, t: Throwable) {
                Toast.makeText(context, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }



    fun addItem(newItem: ItemRequest, context: Context) {
        val storageName = _selectedStorage.value!!.name
        RetrofitClient.apiService.createItem(username, storageName, newItem).enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    Toast.makeText(context, "Item added successfully", Toast.LENGTH_SHORT).show()
                    // Need to update this storage!
                    fetchStorage(context)
                } else {
                    Toast.makeText(context, "Failed to add item: ${response.code()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Void>, t: Throwable) {
                Toast.makeText(context, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }

    fun deleteItem(itemId: String, context: Context) {
        val storageName = _selectedStorage.value!!.name
        RetrofitClient.apiService.deleteItem(username, storageName, itemId).enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    Toast.makeText(context, "Item deleted successfully", Toast.LENGTH_SHORT).show()
                    // Refresh the storage after deletion
                    fetchStorage(context)
                } else {
                    Toast.makeText(context, "Failed to delete item: ${response.code()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Void>, t: Throwable) {
                Toast.makeText(context, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }


}
