import android.graphics.Bitmap
import android.media.Image
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.skladischer.R
import com.example.skladischer.data.Item
import io.github.thibseisel.identikon.Identicon
import io.github.thibseisel.identikon.drawToBitmap

class ItemsAdapter(private var items: List<Item>, private val onItemClick: (Item) -> Unit) :
    RecyclerView.Adapter<ItemsAdapter.ItemViewHolder>() {

    class ItemViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val title: TextView = view.findViewById(R.id.itemTitle)
        val amount: TextView = view.findViewById(R.id.itemAmount)
        val date: TextView = view.findViewById(R.id.itemDate)
        val imageView: ImageView = view.findViewById(R.id.itemImage)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ItemViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_card, parent, false)
        return ItemViewHolder(view)
    }

    override fun onBindViewHolder(holder: ItemViewHolder, position: Int) {
        val item = items[position]

        // Bind only the required data to views
        holder.title.text = item.name
        holder.amount.text = "Amount: ${item.amount}"
        holder.date.text = "Date Added: ${item.date_added}"

        val icon = Identicon.fromValue(item.name, size = 64)
        val iconBitmap = Bitmap.createBitmap(64,64, Bitmap.Config.ARGB_8888)
        icon.drawToBitmap(iconBitmap)
        holder.imageView.setImageBitmap(iconBitmap)

        holder.itemView.setOnClickListener{
            onItemClick(item)
        }

    }

    override fun getItemCount() = items.size

    fun updateItems(newItems: List<Item>) {
        this.items = newItems
        notifyDataSetChanged()
    }

}
