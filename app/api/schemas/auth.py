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


class Fido2RegistrationResponse(BaseModel):
    """Schema for FIDO2 registration response"""

    client_data: str
    attestation_object: str
    state: str


class Fido2AuthenticatorResponse(BaseModel):
    """Schema for FIDO2 authenticator response"""

    credential_id: str
    client_data: str
    authenticator_data: str
    signature: str
    user_handle: str


class Fido2State(BaseModel):
    """Schema for FIDO2 state"""

    challenge: str
    user_verification: str
    authenticator_attachment: str


class Fido2RegistrationStartedResponse(BaseModel):
    """Schema for FIDO2 registration started response"""

    public_key: str
    state: Fido2State
