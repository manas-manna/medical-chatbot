from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from contextlib import asynccontextmanager

from app.auth.schemas import TokenData, UserInDB
from app.db.session import get_db
from app.db.models import UserDB

# Security config
SECRET_KEY = "EQqexli0J8yG7350ceR9u1_RysjRfpxfPmeBk2UXB0U"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def get_user(username: str) -> UserInDB | None:
    async with get_db() as db:  # Proper async context usage
        user = await db.users.find_one({"username": username})
        if user:
            return UserInDB(**user)
    return None

async def authenticate_user(username: str, password: str) -> UserInDB | bool:
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt