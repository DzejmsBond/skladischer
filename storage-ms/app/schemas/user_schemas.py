# Author: Jure
# Date created: 4.12.2024
# To so DTO.

from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    ref_id: str
    display_name: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


