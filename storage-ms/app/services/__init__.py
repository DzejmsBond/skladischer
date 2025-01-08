"""
The `services` module provides utility functions for managing items in storage.
It serves as communication between models and the database.
"""

from .item_utils import (
    create_item,
    delete_item,
    update_item,
    get_item)

from .user_utils import (
    create_user,
    update_display_name,
    delete_user, get_user,
    empty_storages)

from .storage_utils import (
    create_storage,
    get_storage,
    empty_storage,
    update_storage_name,
    delete_storage)
