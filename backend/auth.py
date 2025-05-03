# backend/auth.py
# FastAPI UsersのJWT認証をインポート
from fastapi_users.authentication import JWTAuthentication

# 秘密鍵（変更が必要です）
SECRET = "SECRET_KEY_YOU_SHOULD_CHANGE"

# JWT認証バックエンドの設定
# トークンの有効期間は3600秒（1時間）
# トークンURLは"auth/jwt/login"
auth_backend = JWTAuthentication(
    secret=SECRET,
    lifetime_seconds=3600,
    tokenUrl="auth/jwt/login",
)
