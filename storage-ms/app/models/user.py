# Author: Jure
# Date created: 4.12.2024

from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List
from .storage import Storage
from ..models.py_object_id import PyObjectId

class User(BaseModel):
    id: PyObjectId = Field(alias='_id', default_factory=PyObjectId)
    ref_id: str # To je ID, ki ga povezuje s tabelo admin.
    display_name: Optional[str] = None
    storages: List[Storage]

    @field_serializer("id")
    def serialize_objectid(self, value: PyObjectId) -> str:
        return str(value)

    #set_id sem vrgel ven. id should be made enkrat, natanko ob creationu objecta, z default_factoryjem.