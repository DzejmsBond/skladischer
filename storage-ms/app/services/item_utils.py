# Author: Jure
# Date created: 4.12.2024

from ..schemas import item_schemas as schema
from ..models.item import Item
from .database_helpers import get_users_collection

async def create_item(user_id : str, storage_id : str, item_create : schema.ItemCreate):
    db_users = await get_users_collection()
    if db_users is None:
        return None

    item = Item(name=item_create.name, amount=item_create.amount, description=item_create.description)
    item_dict = item.model_dump(by_alias=True)
    result = await db_users.update_one(
        {"_id": user_id, "storages._id": storage_id},
        {"$push": {"storages.$.content": item_dict}})

    if result.modified_count == 0:
        return None
    return item