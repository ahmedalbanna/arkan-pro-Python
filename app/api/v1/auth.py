from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.auth import Token, LoginRequest, RefreshRequest
from ...core.security import create_token, verify_password, get_password_hash, get_current_user
from ...core.config import settings

router = APIRouter()

# In-memory demo users store; replace with DB lookup
_USERS = {
    "demo@example.com": get_password_hash("password123")
}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    hashed = _USERS.get(username)
    if not hashed or not verify_password(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access = create_token(
        subject=username,
        token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        scopes=form_data.scopes,
    )
    refresh = create_token(
        subject=username,
        token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return Token(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=Token)
async def refresh(payload: RefreshRequest):
    # For simplicity, do not store refresh tokens. In prod, consider rotation & blacklist.
    from ...core.security import verify_token

    data = verify_token(payload.refresh_token)
    if data.type != "refresh":
        raise HTTPException(status_code=400, detail="Invalid refresh token type")

    access = create_token(
        subject=data.sub,
        token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_token(
        subject=data.sub,
        token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return Token(access_token=access, refresh_token=refresh_token)

@router.get("/me")
async def me(user=Depends(get_current_user)):
    return {"subject": user.sub, "scopes": user.scopes}
