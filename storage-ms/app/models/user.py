# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field
from typing import Optional, List
from .storage import Storage
from .objectIdWrapper import *

class User(BaseModel):
    id: Optional[str] = Field(alias='_id', default=None)
    ref_id: str # To je ID, ki ga povezuje s tabelo admin.
    display_name: Optional[str] = None
    storages: List[Storage]

    class Config:
        arbitrary_types_allowed = True

    def set_id(self, oid : ObjectId):
        self.id = oid_to_str(oid)






