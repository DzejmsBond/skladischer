# Author: Jure
# Date created: 4.12.2024
# To so DTO.

from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    display_name: Optional[str] = None


