# Author: Nina Mislej
# Date created: 15.01.2025

import jwt
from jwt import InvalidTokenError

from .error import ErrorResponse as Err
from ..config import SECRET_KEY, ALGORITHM

async def validate_token(token: str, username: str) -> None | Err:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "username" not in payload:
            return Err(message="Username not found in token.", code=401)
        if payload.get("username") != username:
            return Err(message="Token username does not match.", code=401)
    except InvalidTokenError:
        return Err(message="Could not validate credentials.", code=401)
    except Exception as e:
        return Err(message=f"Unknown  exception: {e}", code=500)