from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.users import UserCreate, UserOut, UserUpdate
from ..schemas.common import Message
from ..services.users import UserService, get_user_service
from ...core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, svc: UserService = Depends(get_user_service)):
    return svc.create_user(payload)

@router.get("/", response_model=list[UserOut])
async def list_users(svc: UserService = Depends(get_user_service), _=Depends(get_current_user)):
    return svc.list_users()

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, svc: UserService = Depends(get_user_service), _=Depends(get_current_user)):
    user = svc.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, payload: UserUpdate, svc: UserService = Depends(get_user_service), _=Depends(get_current_user)):
    user = svc.update_user(user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", response_model=Message)
async def delete_user(user_id: str, svc: UserService = Depends(get_user_service), _=Depends(get_current_user)):
    ok = svc.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return Message(message="deleted")
