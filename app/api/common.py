import base64
from typing import Annotated
from typing import List
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic.alias_generators import to_camel
from starlette.responses import HTMLResponse
from webauthn.helpers.structs import AttestationConveyancePreference
from webauthn.helpers.structs import AuthenticatorAttachment
from webauthn.helpers.structs import AuthenticatorSelectionCriteria
from webauthn.helpers.structs import AuthenticatorTransport
from webauthn.helpers.structs import PublicKeyCredentialDescriptor
from webauthn.helpers.structs import PublicKeyCredentialParameters
from webauthn.helpers.structs import PublicKeyCredentialRpEntity
from webauthn.helpers.structs import PublicKeyCredentialType
from webauthn.helpers.structs import PublicKeyCredentialUserEntity
from webauthn.helpers.structs import UserVerificationRequirement


class JavascriptResponse(HTMLResponse):
    """Javascript response."""

    media_type = "application/javascript"


def b64decode(string: str) -> bytes:
    """Decode a base64 string to bytes."""
    return base64.urlsafe_b64decode(string.encode())


class CustomPublicKeyCredentialCreationOptions(BaseModel):
    """Custom public key credential creation options that decodes the raw_id."""

    model_config = ConfigDict(title="PublicKeyCredentialCreationOptions", alias_generator=to_camel)

    rp: PublicKeyCredentialRpEntity
    user: PublicKeyCredentialUserEntity
    challenge: bytes
    pub_key_cred_params: List[PublicKeyCredentialParameters]
    timeout: Optional[int] = None
    excludeCredentials: Optional[List[PublicKeyCredentialDescriptor]] = None
    authenticatorSelection: Optional[AuthenticatorSelectionCriteria] = None
    attestation: AttestationConveyancePreference = AttestationConveyancePreference.NONE


class CustomAuthenticatorAttestationResponse(BaseModel):
    """Custom attestation response that decodes the client_data_json and attestation_object."""

    model_config = ConfigDict(title="AuthenticatorAttestationResponse")

    client_data_json: Annotated[bytes, Field(alias="clientDataJSON")]
    attestation_object: Annotated[bytes, Field(alias="attestationObject")]
    transports: Optional[List[AuthenticatorTransport]] = None


class CustomRegistrationCredential(BaseModel):
    """Custom registration credential that decodes the raw_id and response."""

    model_config = ConfigDict(title="RegistrationCredential", alias_generator=to_camel)

    id: str
    raw_id: bytes
    response: CustomAuthenticatorAttestationResponse
    authenticator_attachment: Optional[AuthenticatorAttachment] = None
    type: Literal[PublicKeyCredentialType.PUBLIC_KEY] = PublicKeyCredentialType.PUBLIC_KEY


class CustomPublicKeyCredentialRequestOptions(BaseModel):
    """Custom public key credential request options that decodes the allow_credentials."""

    model_config = ConfigDict(title="PublicKeyCredentialRequestOptions", alias_generator=to_camel)

    challenge: bytes
    timeout: Optional[int] = None
    rp_id: Optional[str] = None
    allow_credentials: Optional[List[PublicKeyCredentialDescriptor]] = None
    user_verification: Optional[UserVerificationRequirement] = None
