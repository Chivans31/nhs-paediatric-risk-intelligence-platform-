# AUTHENTICATION SYSTEM

from fastapi.security import HTTPBearer
from fastapi import HTTPException
from jose import jwt

import os

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "nhs_secret_key"
)

ALGORITHM = "HS256"

security = HTTPBearer()


def create_token(username: str):

    payload = {
        "sub": username
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

