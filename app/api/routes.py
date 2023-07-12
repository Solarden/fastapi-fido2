from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer

from app.api.v1 import auth
from app.api.v1 import authn
from app.api.v1 import health

api_router = APIRouter()

bearer = HTTPBearer(auto_error=False)

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, tags=["auth"], dependencies=[Depends(bearer)])
api_router.include_router(authn.router, tags=["authn"], dependencies=[Depends(bearer)])
