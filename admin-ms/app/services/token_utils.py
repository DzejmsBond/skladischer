# Author: Nina Mislej
# Date created: 15.01.2025

from datetime import datetime, timedelta, timezone
import jwt

from ..config import SECRET_KEY, ALGORITHM

async def create_access_token(data: dict, expires: timedelta = timedelta(minutes=60)):
    content = data.copy()
    expire = datetime.now(timezone.utc) + expires
    content.update({"exp": expire})
    token = jwt.encode(content, SECRET_KEY, algorithm=ALGORITHM)
    return token