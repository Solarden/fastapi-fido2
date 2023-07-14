from typing import Dict

from sqlalchemy.orm import Session

from app.core.auth import AuthBase
from app.models import User


class UserService(AuthBase):
    """User service."""

    def _get_password_hash(self, password: str) -> str:
        """Get password hash."""
        return self.crypt_context.hash(password)

    def create_user(self, db: Session, user_data: Dict[str, str]) -> User:
        """Create user."""
        user: User = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=self._get_password_hash(user_data["password"]),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


user_service = UserService()
