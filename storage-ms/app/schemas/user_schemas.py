# Author: Jure
# Date created: 4.12.2024
# To so DTO.

from pydantic import BaseModel
from bson import ObjectId
from typing import Optional, List

class UserCreate(BaseModel):
    ref_id: int = 0 #ref_id: ObjectId
    display_name: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

