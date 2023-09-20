import base64

from pydantic import validator
from starlette.responses import HTMLResponse
from webauthn.helpers.structs import AuthenticationCredential
from webauthn.helpers.structs import RegistrationCredential


class JavascriptResponse(HTMLResponse):
    """Javascript response."""

    media_type = "application/javascript"


def b64decode(string: str) -> bytes:
    """Decode a base64 string to bytes."""
    return base64.urlsafe_b64decode(string.encode())


class CustomRegistrationCredential(RegistrationCredential):
    """Custom registration credential that decodes the raw_id and response."""

    @validator("raw_id", pre=True)
    def convert_raw_id(cls, v: str):  # pylint: disable=no-self-argument
        """Convert raw_id to bytes."""
        assert isinstance(v, str), "raw_id is not a string"
        return b64decode(v)

    @validator("response", pre=True)
    def convert_response(cls, data: dict):  # pylint: disable=no-self-argument
        """Convert response to bytes."""
        assert isinstance(data, dict), "response is not a dictionary"
        return {k: b64decode(v) for k, v in data.items()}


class CustomAuthenticationCredential(AuthenticationCredential):
    """Custom authentication credential that decodes the raw_id and response."""

    @validator("raw_id", pre=True)
    def convert_raw_id(cls, v: str):  # pylint: disable=no-self-argument
        """Convert raw_id to bytes."""
        assert isinstance(v, str), "raw_id is not a string"
        return b64decode(v)

    @validator("response", pre=True)
    def convert_response(cls, data: dict):  # pylint: disable=no-self-argument
        """Convert response to bytes."""
        assert isinstance(data, dict), "response is not a dictionary"
        return {k: b64decode(v) for k, v in data.items()}
