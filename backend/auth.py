# backend/auth.py
from fastapi_users.authentication import JWTAuthentication

SECRET = "SECRET_KEY_YOU_SHOULD_CHANGE"

auth_backend = JWTAuthentication(
    secret=SECRET,
    lifetime_seconds=3600,
    tokenUrl="auth/jwt/login",
)
