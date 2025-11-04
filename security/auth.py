from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from core.config import settings
from models.user import User
from schemas.token import TokenData
from beanie.exceptions import DocumentNotFound


# Use Argon2 for password hashing. Argon2 is a modern, memory-hard KDF
# that doesn't have bcrypt's 72-byte limitation and is recommended for
# new applications. Requires `argon2-cffi` (or passlib[argon2]) in
# requirements.
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# OAuth2 scheme, trỏ đến endpoint /api/v1/auth/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if isinstance(plain_password, bytes):
        plain_password = plain_password.decode("utf-8", errors="ignore")
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    if isinstance(password, bytes):
        password = password.decode("utf-8", errors="ignore")
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Tạo JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency để lấy user hiện tại từ JWT token.
    Đây là "bảo vệ" cho các endpoint cần xác thực.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    try:
        user = await User.find_one(User.email == token_data.email)
        if user is None:
            raise credentials_exception
        return user
    except DocumentNotFound:
        raise credentials_exception

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency để lấy user admin hiện tại.
    Bảo vệ cho các endpoint chỉ dành cho admin.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
