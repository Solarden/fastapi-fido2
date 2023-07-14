from typing import Optional
from uuid import UUID

from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import EmailStr  # pylint: disable=no-name-in-module


class NewUser(BaseModel):
    """Schema for creating a new user"""

    username: str
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]


class UserLoginSchema(BaseModel):
    """Schema for user login"""

    username: str
    password: str


class PydanticUser(BaseModel):
    """Schema for user"""

    class Config:
        """Config for user schema"""

        title = "User"
        orm_mode = True

    id: UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool


class Token(BaseModel):
    """Schema for token"""

    access_token: str
    token_type: str


class MessageResponse(BaseModel):
    """Schema for message"""

    message: str
