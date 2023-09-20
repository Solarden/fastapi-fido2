from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.routes import api_router
from app.core import settings


def get_application() -> FastAPI:
    """Create FastAPI application."""
    middleware = [
        Middleware(
            SessionMiddleware,
            secret_key=settings.SECRET_KEY,
            session_cookie=settings.PROJECT_NAME,
            same_site="strict",
            https_only=True,
        )
    ]
    application = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG, middleware=middleware)
    application.include_router(api_router, prefix=settings.API_PREFIX)

    return application


app = get_application()
