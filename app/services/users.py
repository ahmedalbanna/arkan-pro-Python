import uuid
from typing import Optional
from ..db.repository import Repository
from ..schemas.users import UserCreate, UserOut, UserUpdate
from ..core.security import get_password_hash

class UserService:
    def __init__(self, repo: Repository[UserOut] | None = None) -> None:
        self.repo = repo or Repository()

    def create_user(self, data: UserCreate) -> UserOut:
        user_id = str(uuid.uuid4())
        # Store hashed password (in real DB table separate from public schema)
        hashed = get_password_hash(data.password)
        user = UserOut(id=user_id, email=data.email, full_name=data.full_name)
        # naive store; in DB you'd persist hashed password too
        self.repo.add(user_id, user)
        return user

    def get_user(self, user_id: str) -> Optional[UserOut]:
        return self.repo.get(user_id)

    def list_users(self) -> list[UserOut]:
        return self.repo.list()

    def update_user(self, user_id: str, data: UserUpdate) -> Optional[UserOut]:
        user = self.repo.get(user_id)
        if not user:
            return None
        updated = user.model_copy(update=data.model_dump(exclude_unset=True))
        self.repo.add(user_id, updated)
        return updated

    def delete_user(self, user_id: str) -> bool:
        prev = self.repo.get(user_id)
        if not prev:
            return False
        self.repo.delete(user_id)
        return True


def get_user_service() -> UserService:
    return UserService()
