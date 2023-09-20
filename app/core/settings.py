from decouple import config

# App general settings
API_PREFIX = "/api/v1"
PROJECT_NAME = config("PROJECT_NAME", default="FIDO2 FastAPI")
DEBUG = config("DEBUG", cast=bool, default=False)

# Database settings
DATABASE_URL = config("DATABASE_URL")
TEST_DATABASE_URL = config("TEST_DATABASE_URL")
SQLALCHEMY_POOL_SIZE = config("SQLALCHEMY_POOL_SIZE", cast=int, default=20)
SQLALCHEMY_MAX_OVERFLOW = config("SQLALCHEMY_MAX_OVERFLOW", cast=int, default=80)
SQLALCHEMY_POOL_TIMEOUT = config("SQLALCHEMY_POOL_TIMEOUT", cast=int, default=10)

# OAuth2 settings
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30)
ISSUER = config("ISSUER", default="FIDO2 FastAPI")
AUDIENCE = config("AUDIENCE", default="FIDO2 FastAPI")

# FIDO2 settings
RP_ID = config("RP_ID", default="localhost")
RP_NAME = config("RP_NAME", default="FIDO2 FastAPI")
USER_VERIFICATION = "preferred"
AUTHENTICATOR_ATTACHMENT = "platform"
EXPECTED_ORIGIN = config("EXPECTED_ORIGIN", default="http://localhost:8000")
