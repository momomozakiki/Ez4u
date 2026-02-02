from datetime import timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from app.database.base import AsyncSessionLocal
from app.database.models import User, UserIdentity
from app.core.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# Dependency
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

# Pydantic Models
class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

# Auth Logic
async def authenticate_user(db: AsyncSession, username: str, password: str):
    stmt = select(UserIdentity).where(
        UserIdentity.provider == "local", 
        UserIdentity.subject == username
    )
    result = await db.execute(stmt)
    identity = result.scalar_one_or_none()
    
    if not identity or not identity.password_hash:
        return False
    if not verify_password(password, identity.password_hash):
        return False
    
    # Fetch full user
    user_stmt = select(User).where(User.id == identity.user_id)
    user_result = await db.execute(user_stmt)
    return user_result.scalar_one()

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        # Fallback to header for API testing tools
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # In a real app, we might verify user still exists in DB
    # For now, we trust the token or do a quick lookup
    # We used 'username' (subject) as 'sub'. But wait, our 'subject' in UserIdentity is the username.
    # We need to find the user associated with this subject.
    stmt = select(UserIdentity).where(UserIdentity.subject == username, UserIdentity.provider == "local")
    result = await db.execute(stmt)
    identity = result.scalar_one_or_none()
    if identity is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
    user_stmt = select(User).where(User.id == identity.user_id)
    user_result = await db.execute(user_stmt)
    return user_result.scalar_one()

# Routes
@router.post("/login")
async def login(form_data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=form_data.username, expires_delta=access_token_expires
    )
    
    # Set HttpOnly Cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True, # Should be True in Prod, but OK for localhost usually if browser allows
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return {"message": "Login successful", "user": {"email": user.email, "name": user.full_name}}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active
    }
