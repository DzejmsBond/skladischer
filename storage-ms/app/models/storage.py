# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from .item import Item

class Storage(BaseModel):
    """
    Represents a storage model.
    This model defines the attributes of a storage, including its name and the list of items it contains.
    """

    # This is the unique identifier of the item.
    name: str
    content: List[Item]