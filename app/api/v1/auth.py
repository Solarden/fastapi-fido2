from typing import Dict

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.api.schemas.auth import MessageResponse
from app.api.schemas.auth import NewUser
from app.api.schemas.auth import PydanticUser
from app.api.schemas.auth import Token
from app.core.auth import UserCreator
from app.core.auth import user_auth
from app.dependencies.auth_db import get_db
from app.dependencies.auth_token import get_current_user
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=MessageResponse, status_code=status.HTTP_201_CREATED, summary="Sign up")
async def sign_up(new_user: NewUser, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Sign up a new user."""
    user_creator = UserCreator(db=db, user_data=new_user.dict())
    user_creator.create_user()
    return {"message": "Created user successfully!"}


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Incorrect username or password"},
    },
)
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user."""
    username = form_data.username
    password = form_data.password
    user: User = user_auth.authenticate_user(db, username, password)
    if user:
        access_token = user_auth.create_access_token(user=user)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")


@router.get("/me", response_model=PydanticUser, status_code=status.HTTP_200_OK, summary="User information.")
async def sup(
    current_user: User = Depends(get_current_user),
) -> User:
    """Sup."""
    return current_user
