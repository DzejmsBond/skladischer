# Author: Nina Mislej
# Date created: 15.01.2025

from datetime import datetime, timedelta, timezone
import jwt

from .config import SECRET_KEY, ALGORITHM

async def create_access_token(data: dict, expires: timedelta = timedelta(minutes=60)):
    content = data.copy()
    expire = datetime.now(timezone.utc) + expires
    content.update({"exp": expire})
    token = jwt.encode(content, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def validate_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "username" not in payload:
            return False
        return True
    except InvalidTokenError as e:
        print(e)
        return False
    except Exception:
        return False

async def validate_token_with_username(username, token) -> bool:
    if not validate_token(token):
        return False

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if payload.get("username") != username:
        return False
    return True