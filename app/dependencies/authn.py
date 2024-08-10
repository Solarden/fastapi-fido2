from typing import List
from typing import Union

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.errors import UserCredentialsNotFound
from app.dependencies.auth_db import get_db
from app.dependencies.auth_token import get_current_user
from app.models import User
from app.models import UserCredential


def get_current_user_credentials(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> List[Union[UserCredential, None]]:
    """Get current user credentials."""
    user_credentials: List[Union[UserCredential, None]] = (
        db.query(UserCredential).filter(UserCredential.user_id == user.id).all()
    )

    if not user_credentials:
        raise UserCredentialsNotFound

    return user_credentials
