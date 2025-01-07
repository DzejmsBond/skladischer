# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from .item import Item

class Storage(BaseModel):
    name: str
    content: List[Item]