from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

class TokenData(BaseModel):
    sub: str
    exp: int
    type: str
    scopes: list[str] = []
    aud: str | None = None
    iss: str | None = None


def create_token(subject: str, token_type: str, expires_delta: timedelta, scopes: list[str] | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "type": token_type,
        "scopes": scopes or [],
    }
    if settings.TOKEN_AUDIENCE:
        payload["aud"] = settings.TOKEN_AUDIENCE
    if settings.TOKEN_ISSUER:
        payload["iss"] = settings.TOKEN_ISSUER
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], audience=settings.TOKEN_AUDIENCE if settings.TOKEN_AUDIENCE else None, issuer=settings.TOKEN_ISSUER if settings.TOKEN_ISSUER else None)
        return TokenData(**payload)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    data = verify_token(token)
    return data
