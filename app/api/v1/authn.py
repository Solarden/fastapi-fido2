import base64
from pathlib import Path
from typing import List

import webauthn
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette import status
from webauthn.helpers.structs import AuthenticatorAttachment
from webauthn.helpers.structs import AuthenticatorSelectionCriteria
from webauthn.helpers.structs import AuthenticatorTransport
from webauthn.helpers.structs import PublicKeyCredentialCreationOptions
from webauthn.helpers.structs import PublicKeyCredentialDescriptor
from webauthn.helpers.structs import PublicKeyCredentialRequestOptions
from webauthn.helpers.structs import ResidentKeyRequirement
from webauthn.helpers.structs import UserVerificationRequirement
from webauthn.registration.verify_registration_response import VerifiedRegistration

from app.api.common import CustomAuthenticationCredential
from app.api.common import CustomRegistrationCredential
from app.api.common import JavascriptResponse
from app.api.schemas.auth import MessageResponse
from app.core import settings
from app.dependencies.auth_db import get_db
from app.dependencies.auth_token import get_current_user
from app.dependencies.authn import get_current_user_credential
from app.dependencies.authn import get_current_user_credentials
from app.models import User
from app.models import UserCredential

router = APIRouter(prefix="/authn", tags=["authn"])


@router.get("/", response_class=HTMLResponse)
async def index():
    """Index."""
    with open("app/api/v1/resources/authn_html.html", "r", encoding="utf8") as f:
        html_string = f.read()
        return html_string


@router.get("/webauthn_client.js", response_class=JavascriptResponse)
async def client_js():
    """Client JS."""
    return Path("app/api/v1/resources/webauthn_client.js").read_bytes()


@router.get("/register/public_key", response_model=PublicKeyCredentialCreationOptions, status_code=status.HTTP_200_OK)
async def get_user_register_public_key(
    request: Request,
    user: User = Depends(get_current_user),
):
    """Get user public key."""
    public_key = webauthn.generate_registration_options(
        rp_id=settings.RP_ID,
        rp_name=settings.RP_NAME,
        user_id=str(user.id),
        user_name=user.email,
        user_display_name=user.username,
        authenticator_selection=AuthenticatorSelectionCriteria(
            authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
            resident_key=ResidentKeyRequirement.DISCOURAGED,
            user_verification=UserVerificationRequirement.DISCOURAGED,
        ),
    )
    request.session["webauthn_register_challenge"] = base64.b64encode(public_key.challenge).decode()
    return public_key


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_user_credential(
    request: Request,
    credential: CustomRegistrationCredential,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create user credential."""
    expected_challenge = base64.b64decode(request.session["webauthn_register_challenge"].encode())
    registration: VerifiedRegistration = webauthn.verify_registration_response(
        credential=credential,
        expected_challenge=expected_challenge,
        expected_rp_id=settings.RP_ID,
        expected_origin=settings.EXPECTED_ORIGIN,
    )
    UserCredential.create_credential(db, user, registration)
    return {"message": "User credential created"}


@router.get("/auth/public_key", response_model=PublicKeyCredentialRequestOptions, status_code=status.HTTP_200_OK)
async def get_user_auth_credential(
    request: Request,
    user: User = Depends(get_current_user),  # pylint: disable=unused-argument
    user_credentials: List[UserCredential] = Depends(get_current_user_credentials),
):
    """Get user auth credential."""
    public_key = webauthn.generate_authentication_options(
        rp_id=settings.RP_ID,
        allow_credentials=[
            PublicKeyCredentialDescriptor(
                id=credential.credential_id, transports=[AuthenticatorTransport.USB, AuthenticatorTransport.HYBRID]
            )
            for credential in user_credentials
        ],
        user_verification=UserVerificationRequirement.DISCOURAGED,
    )
    request.session["webauthn_auth_challenge"] = base64.b64encode(public_key.challenge).decode()
    return public_key


@router.post("/auth", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def auth_post(
    request: Request,
    credential: CustomAuthenticationCredential,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),  # pylint: disable=unused-argument
    user_credential: UserCredential = Depends(get_current_user_credential),
):
    """Auth post."""
    expected_challenge = base64.b64decode(request.session["webauthn_auth_challenge"].encode())
    auth = webauthn.verify_authentication_response(
        credential=credential,
        expected_challenge=expected_challenge,
        expected_rp_id=settings.RP_ID,
        expected_origin=settings.EXPECTED_ORIGIN,
        credential_public_key=user_credential.public_key,
        credential_current_sign_count=user_credential.sign_count,
    )
    user_credential.update_sign_count(db, auth.new_sign_count)
    return {"message": "OK"}
