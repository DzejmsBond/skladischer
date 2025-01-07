# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from .storage import Storage

class User(BaseModel):
    display_name: Optional[str] = None
    storages: List[Storage]