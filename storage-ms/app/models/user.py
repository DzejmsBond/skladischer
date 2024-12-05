# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List
from .storage import Storage

class User(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId)
    ref_id: ObjectId # To je ID, ki ga povezuje s tabelo admin.
    display_name: Optional[str] = None
    storages: List[Storage]

    class Config:
        arbitrary_types_allowed = True





