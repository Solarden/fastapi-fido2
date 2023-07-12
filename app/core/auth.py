from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from jose import JWTError
from jose import jwt
from jwt import DecodeError
from jwt import ExpiredSignatureError
from jwt import InvalidAudienceError
from jwt import InvalidIssuerError
from jwt import InvalidSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.api.errors import InvalidTokenException
from app.core import settings
from app.models.user import User


class AuthBase:
    """Base class for authentication."""

    crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])


class UserCreator(AuthBase):
    """User creator."""

    def __init__(self, db: Session, user_data: Dict[str, str]):
        self.db = db
        self.username = user_data["username"]
        self.password = user_data["password"]
        self.email = user_data["email"]
        self.first_name = user_data["first_name"]
        self.last_name = user_data["last_name"]

    def _get_password_hash(self) -> str:
        """Get password hash."""
        return self.crypt_context.hash(self.password)

    def create_user(self) -> User:
        """Create user."""
        user: User = User(
            username=self.username,
            email=self.email,
            hashed_password=self._get_password_hash(),
            first_name=self.first_name,
            last_name=self.last_name,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class TokenHandler:
    """Token handler."""

    @staticmethod
    def create_access_token(
        user: User,
        expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        state: Optional[str] = None,
    ) -> str:
        """Create access token."""
        to_encode: Dict[str, Union[str, int, Dict[str, str]]] = {
            "sub": user.username,
            "exp": int((datetime.utcnow() + expires_delta).timestamp()),
            "iss": settings.ISSUER,
            "aud": settings.AUDIENCE,
            "iat": int(datetime.utcnow().timestamp()),
            "jti": "2137",  # todo understand how jti is supposed to work
            "context": {
                "state": state,
            },
        }
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def validate_access_token(access_token: str) -> Dict[str, Any]:
        """Validate access token."""
        try:
            decoded_token = jwt.decode(
                access_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                audience=settings.AUDIENCE,
                issuer=settings.ISSUER,
                options={
                    "verify_signature": True,
                    "require": ["exp", "iss", "sub", "aud"],
                    "verify_iss": True,
                    "verify_aud": True,
                    "verify_exp": True,
                },
            )
        except (
            InvalidSignatureError,
            DecodeError,
            InvalidIssuerError,
            ExpiredSignatureError,
            InvalidAudienceError,
            JWTError,
        ) as exc:
            raise InvalidTokenException from exc

        return decoded_token

    def retrieve_user(self, db: Session, access_token: str) -> Union[User, None]:
        """Retrieve user."""
        decoded_token: Dict[str, Any] = self.validate_access_token(access_token)

        if not decoded_token["sub"]:
            raise InvalidTokenException

        user: Union[User, None] = db.query(User).filter(User.username == decoded_token["sub"]).scalar()

        if not user:
            raise InvalidTokenException

        return user

    def retrieve_token(self, access_token: str) -> str:
        """Retrieve token."""
        decoded_token: Dict[str, Any] = self.validate_access_token(access_token)

        return decoded_token["context"]["state"]


class UserAuth(AuthBase, TokenHandler):
    """User authentication."""

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password."""
        return self.crypt_context.verify(plain_password, hashed_password)

    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user."""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user


user_auth = UserAuth()
