from typing import Optional

from fastapi import HTTPException
from fastapi import status


class BasicException(HTTPException):
    """Basic Exception with self message, and status code"""

    status_code: status = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Something went wrong"

    def __init__(self, detail: Optional[str] = None, status_code: Optional[status] = None):
        self.status_code = status_code or self.status_code
        self.detail = detail or self.detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidTokenException(BasicException):
    """Invalid Token Exception"""

    status_code: status = status.HTTP_401_UNAUTHORIZED
    detail: str = "Invalid token - signature verification failed"


class InvalidCredentialException(BasicException):
    """Invalid Credential Exception"""

    status_code: status = status.HTTP_404_NOT_FOUND
    detail: str = "Invalid or not found credential"


class UserAlreadyExistsException(BasicException):
    """User Already Exists Exception"""

    status_code: status = status.HTTP_409_CONFLICT
    detail: str = "User already exists"


class UserCredentialsNotFound(BasicException):
    """User Credentials Not Found Exception"""

    status_code: status = status.HTTP_404_NOT_FOUND
    detail: str = "User credentials not configured or not found"
