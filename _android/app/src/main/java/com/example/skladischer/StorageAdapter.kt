import android.graphics.Bitmap
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.PopupMenu
import android.widget.TextView
import android.widget.Toast
import androidx.recyclerview.widget.RecyclerView
import com.example.skladischer.R
import com.example.skladischer.data.Item
import com.example.skladischer.data.Storage
import io.github.thibseisel.identikon.Identicon
import io.github.thibseisel.identikon.drawToBitmap

class StorageAdapter(
    private var storages: List<Storage>,
    private val onEditStorage: (Storage) -> Unit,
    private val onDeleteStorage: (Storage) -> Unit,
    private val onStorageClick: (Storage) -> Unit) :
    RecyclerView.Adapter<StorageAdapter.StorageViewHolder>() {
    class StorageViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val imageView: ImageView = view.findViewById(R.id.storageImageView)
        val nameTextView: TextView = view.findViewById(R.id.storageTextView)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): StorageViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.storage_card, parent, false)
        return StorageViewHolder(view)
    }

    override fun onBindViewHolder(holder: StorageViewHolder, position: Int) {
        val storage = storages[position]
        val icon = Identicon.fromValue(storage.name, size = 128)
        val iconBitmap = Bitmap.createBitmap(128,128, Bitmap.Config.ARGB_8888)
        icon.drawToBitmap(iconBitmap)
        holder.imageView.setImageBitmap(iconBitmap)
        holder.nameTextView.text = storage.name              // Set the storage name

        holder.itemView.setOnClickListener {
            onStorageClick(storage)
        }
        holder.itemView.setOnLongClickListener {
            showPopupMenu(it, storage)
            true
        }
    }


    override fun getItemCount() = storages.size

    fun updateStorages(newStorages: List<Storage>) {
        storages = newStorages
        notifyDataSetChanged()
    }

    fun showPopupMenu(view: View, storage: Storage) {
        val popupMenu = PopupMenu(view.context, view)
        popupMenu.inflate(R.menu.storage_popup_menu)
        popupMenu.setOnMenuItemClickListener { menuItem ->
            when (menuItem.itemId) {
                R.id.edit_storage -> {
                    onEditStorage(storage)
                    true
                }
                R.id.delete_storage -> {
                    onDeleteStorage(storage)
                    true
                }
                else -> false
            }
        }
        popupMenu.show()
    }
}
