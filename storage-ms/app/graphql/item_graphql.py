# Author: Jure
# Date created: 4.12.2024

from typing import List, Dict, Optional
from storage_utils import get_storage

async def filter_items(user_id: str, storage_name: str, filtering: Optional[dict]) -> List[dict]:
    """
    Retrieve and filter items in a user's storage.

    Args:
        user_id (str): The user ID owning the storage.
        storage_name (str): The name of the storage.
        filtering (dict): The filtering criteria.

    Returns:
        List[dict]: A list of items matching the filter criteria.
    """

    try:
        db_users = await get_collection()
        if db_users is None:
            return []

        storage = await get_storage(user_id, storage_name)
        if isinstance(await storage, Err):
            return Err(message=f"Cannot find specified storage '{storage_name}'.", code=400)

        # Apply filters if provided.
        return []

    except Exception as e:
        print(f"Error filtering items: {e}")
        return []


