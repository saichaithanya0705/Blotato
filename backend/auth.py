from datetime import datetime, timedelta
from typing import Optional, Union
from fastapi import HTTPException, Security, status, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyHeader
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
import secrets
from models import User, TokenData
from config import get_config, get_user_data

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Get configuration
config = get_config()

# JWT Settings
SECRET_KEY = config.jwt_secret_key
ALGORITHM = config.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.jwt_expire_minutes

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_api_key() -> str:
    """Generate a new API key."""
    return secrets.token_urlsafe(config.api_key_length)

async def validate_api_key(api_key: str) -> bool:
    """Validate an API key."""
    from storage import api_keys_collection

    key_data = await api_keys_collection.find_one({"key": api_key, "is_active": True})
    if key_data:
        # Update last used timestamp
        await api_keys_collection.update_one(
            {"key": api_key},
            {"$set": {"last_used": datetime.utcnow()}}
        )
        return True
    return False

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token and return user_id."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data.user_id

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key and return user_id."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if not await validate_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return config.get_user_id()

async def verify_auth(
    request: Request,
    jwt_credentials: HTTPAuthorizationCredentials = Security(security),
    api_key: str = Security(api_key_header)
) -> str:
    """Verify either JWT token or API key authentication."""

    # Try API key first
    if api_key:
        try:
            return await verify_api_key(api_key)
        except HTTPException:
            pass

    # Try JWT token
    if jwt_credentials:
        try:
            return verify_token(jwt_credentials)
        except HTTPException:
            pass

    # Neither authentication method worked
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Valid authentication required (JWT token or API key)",
        headers={"WWW-Authenticate": "Bearer, ApiKey"},
    )