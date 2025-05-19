from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.auth.schemas import Token, UserCreate, User
from app.auth.service import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user
)
from app.db.session import get_db
from app.utils.logger import log_auth_event

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # Authentication logic
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        # Log failed login attempt
        log_auth_event("LOGIN_FAILED", form_data.username, request)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Log successful login
    log_auth_event("LOGIN_SUCCESS", user.username, request)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(request: Request, user_data: UserCreate):
    async with get_db() as db:
        existing_user = await db.users.find_one({"username": user_data.username})
        if existing_user:
            log_auth_event("REGISTRATION_FAILED", user_data.username, request)
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = get_password_hash(user_data.password)
        await db.users.insert_one({
            "username": user_data.username,
            "hashed_password": hashed_password
        })
        
        # Log successful registration
        log_auth_event("REGISTRATION_SUCCESS", user_data.username, request)
        
    return {"message": "User created successfully"}