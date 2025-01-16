package com.example.skladischer

import ItemsAdapter
import StorageAdapter
import android.graphics.BitmapFactory
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.viewModels
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.Observer
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.skladischer.data.Item
import com.example.skladischer.data.ItemRequest
import com.example.skladischer.data.User
import com.example.skladischer.ui.theme.SkladischerTheme
import com.google.gson.Gson
import java.io.BufferedReader
import java.io.InputStreamReader
import kotlin.io.encoding.Base64
import kotlin.io.encoding.ExperimentalEncodingApi

@OptIn(ExperimentalEncodingApi::class)
class MainActivity : ComponentActivity() {

    private val userViewModel: UserViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val authToken = intent.getStringExtra("AUTH_TOKEN")!!

        userViewModel.fetchUser("testuser")

        val welcomeText = findViewById<TextView>(R.id.welcomeDisplayName)
        welcomeText.text = userViewModel.display_name
        /*
        val userJson = queryUserData(authToken)
        //Log.d("MACKA", userJson.getString("display_name"))
        val gson = Gson()
        val user = gson.fromJson(userJson, User::class.java) // If gotted by api, this will have automatically been GSON'd already.
        Log.d("MACKA", user.toString())
        for (storage in user.storages) {
            Log.d("MACKA", storage.toString())
            for (item in storage.content) {
                Log.d("MACKA", item.toString())
            }
        }
        */
        val storageRecView = findViewById<RecyclerView>(R.id.storageRecView)
        val itemsRecView = findViewById<RecyclerView>(R.id.itemsRecView)
        val itemsInStorage = findViewById<TextView>(R.id.tvItemsInStorage)

        val detailItemFrame = findViewById<View>(R.id.detailedItemCard)
        val backButton = findViewById<ImageButton>(R.id.backButtonDets)
        val detailItemName = findViewById<TextView>(R.id.detailItemName)
        val detailItemAmount = findViewById<TextView>(R.id.detailItemAmount)
        val detailItemDate = findViewById<TextView>(R.id.detailItemDate)
        val detailItemDescription = findViewById<TextView>(R.id.detailItemDescription)
        val qrCodeImageView = findViewById<ImageView>(R.id.qrCodeImageView)
        val deleteButton: TextView = findViewById(R.id.tvDelItem)

        var currItem : Item? = null

        val itemsLayoutManager = LinearLayoutManager(applicationContext, LinearLayoutManager.VERTICAL, false)
        itemsRecView.layoutManager = itemsLayoutManager
        val itemsAdapter = ItemsAdapter(emptyList()) {selectedItem ->
            currItem = selectedItem
            detailItemName.text = selectedItem.name
            detailItemAmount.text = "Amount: ${selectedItem.amount}"
            detailItemDate.text = "Date Added: ${selectedItem.date_added}"
            detailItemDescription.text = selectedItem.description ?: "No description"

            // Generate QR code from base64 string
            val decodedBytes = Base64.decode(selectedItem.image_base64)
            val bitmap = BitmapFactory.decodeByteArray(decodedBytes, 0, decodedBytes.size)

            qrCodeImageView.setImageBitmap(bitmap)

            itemsRecView.visibility = View.GONE
            detailItemFrame.visibility = View.VISIBLE

        }
        itemsRecView.adapter = itemsAdapter

        qrCodeImageView.setOnClickListener {
            Toast.makeText(this, "Printing...", Toast.LENGTH_SHORT).show()
        }

        backButton.setOnClickListener {
            detailItemFrame.visibility = View.GONE
            itemsRecView.visibility = View.VISIBLE
        }

        deleteButton.setOnClickListener {
            detailItemFrame.visibility = View.GONE
            itemsRecView.visibility = View.VISIBLE
            userViewModel.deleteItem(currItem!!.code_id, this)
        }

        val storageLayoutManager = LinearLayoutManager(applicationContext, LinearLayoutManager.HORIZONTAL, false)
        storageRecView.layoutManager = storageLayoutManager

        //set inital adapter
        storageRecView.adapter = StorageAdapter(emptyList(), {}, { storage -> userViewModel.deleteStorage(storage.name, this)}) { selectedStorage ->
            itemsAdapter.updateItems(selectedStorage.content)
        }

        addStorageConfig()
        addItemConfig()

        // Observe data changes
        /*
        userViewModel.user.observe(this, Observer { user ->
            if (user != null) {
                println("User: ${user.display_name}")
                // Update UI with user data
            }
        })
        */
        // Observe storages
        userViewModel.storages.observe(this) { storages ->
            if (storages != null) {
                storageRecView.adapter = StorageAdapter(storages, {}, { storage -> userViewModel.deleteStorage(storage.name, this)}) { selectedStorage ->
                    userViewModel.selectStorage(selectedStorage, this)
                    itemsInStorage.text = "Items in ${selectedStorage.name}:"

                }
            }
        }

        // Observe storage
        userViewModel.selectedStorage.observe(this) { updatedStorage ->
            if (updatedStorage != null) {
                // Update the items in the RecyclerView
                itemsAdapter.updateItems(updatedStorage.content)
            }
        }

        // Observe items
        userViewModel.items.observe(this) { items ->
            itemsAdapter.updateItems(items)
        }

        userViewModel.error.observe(this, Observer { error ->
            if (error != null) {
                println("Error: $error")
            }
        })

        userViewModel.fetchUser("testuser")
        welcomeText.text = userViewModel.display_name
        //not working
        welcomeText.text = "skladischer"
    }

    fun addStorageConfig() {
        // btnShowAddStorage is tvAddStorage
        val addStorageLayout = findViewById<LinearLayout>(R.id.addStorageLayout)
        val etStorageName = findViewById<EditText>(R.id.etStorageName)
        val btnAddStorage = findViewById<Button>(R.id.btnAddStorage)
        val btnShowAddStorage = findViewById<TextView>(R.id.tvAddStorage)
        btnShowAddStorage.setOnClickListener {
            addStorageLayout.visibility = View.VISIBLE
        }

        btnAddStorage.setOnClickListener {
            val storageName = etStorageName.text.toString().trim()
            if (storageName.isEmpty()) {
                Toast.makeText(this, "Storage name cannot be empty", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // Call ViewModel to add storage
            userViewModel.addStorage(storageName, this)

            // Reset form and hide the layout
            etStorageName.text.clear()
            addStorageLayout.visibility = View.GONE
        }
    }

    fun addItemConfig() {
        val addItemLayout = findViewById<View>(R.id.addItemLayout)
        val itemsRecView = findViewById<RecyclerView>(R.id.itemsRecView)
        val tvAddItem = findViewById<TextView>(R.id.tvAddItem)
        val etItemName = findViewById<EditText>(R.id.etItemName)
        val etItemAmount = findViewById<EditText>(R.id.etItemAmount)
        val etItemDescription = findViewById<EditText>(R.id.etItemDescription)
        val btnSubmitItem = findViewById<Button>(R.id.btnSubmitItem)

        // Show Add Item Layout
        tvAddItem.setOnClickListener {
            itemsRecView.visibility = View.GONE
            addItemLayout.visibility = View.VISIBLE
        }

        // Submit New Item
        btnSubmitItem.setOnClickListener {
            val itemName = etItemName.text.toString()
            val itemAmount = etItemAmount.text.toString().toIntOrNull() ?: 0
            val itemDescription = etItemDescription.text.toString()

            // Validate inputs
            if (itemName.isEmpty() || itemAmount <= 0) {
                Toast.makeText(this, "Please enter valid item details", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val newItem = ItemRequest(name = itemName, amount = itemAmount, description = itemDescription)

            // Use ViewModel to send POST request
            userViewModel.addItem( newItem, this)

            // Reset form and toggle visibility
            etItemName.text.clear()
            etItemAmount.text.clear()
            etItemDescription.text.clear()
            addItemLayout.visibility = View.GONE
            itemsRecView.visibility = View.VISIBLE
        }
    }

    fun queryUserData(authToken: String) : String {
        // Dummy function.
        if (authToken == "SuperSecretToken") {
            val inputStream = this.applicationContext.resources.openRawResource(R.raw.testuser)
            val bufferedReader = BufferedReader(InputStreamReader(inputStream))
            return (bufferedReader.use { it.readText() })
        } else return ""
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    SkladischerTheme {
        Greeting("Android")
    }
}