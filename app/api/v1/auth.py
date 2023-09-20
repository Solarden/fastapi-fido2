from typing import Dict

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from app.api.errors import UserAlreadyExistsException
from app.api.schemas.auth import MessageResponse
from app.api.schemas.auth import NewUser
from app.api.schemas.auth import PydanticUser
from app.api.schemas.auth import Token
from app.api.schemas.auth import UserLoginSchema
from app.api.services.user_service import user_service
from app.core.auth import user_auth
from app.dependencies.auth_db import get_db
from app.dependencies.auth_token import get_current_user
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=MessageResponse, status_code=status.HTTP_201_CREATED, summary="Sign up")
async def sign_up(new_user: NewUser, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Sign up a new user."""
    try:
        user_service.create_user(db, new_user.dict())
    except IntegrityError as e:
        raise UserAlreadyExistsException from e
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
async def login(form_data: UserLoginSchema, db: Session = Depends(get_db)):
    """Login user."""
    user: User = user_auth.authenticate_user(db, form_data.username, form_data.password)
    if user:
        access_token = user_auth.create_access_token(user=user)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")


@router.get("/me", response_model=PydanticUser, status_code=status.HTTP_200_OK, summary="User information.")
async def get_current_user_information(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current user information."""
    return current_user
