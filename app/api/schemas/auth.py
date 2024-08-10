from typing import Optional
from uuid import UUID

from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import ConfigDict
from pydantic import EmailStr  # pylint: disable=no-name-in-module


class NewUser(BaseModel):
    """Schema for creating a new user"""

    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLoginSchema(BaseModel):
    """Schema for user login"""

    username: str
    password: str


class PydanticUser(BaseModel):
    """Schema for user"""

    model_config = ConfigDict(title="User", from_attributes=True)

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
