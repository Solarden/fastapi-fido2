from typing import Annotated
from typing import Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.auth import user_auth
from app.dependencies.auth_db import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> Union[User, None]:
    """Get current user."""
    return user_auth.retrieve_user(db, token)
