from fastapi import Request, Depends, HTTPException
from typing import List, Optional
from jose import jwt, JWTError
from models.user import User  # Assuming you have a User model
from utils.apierror import ApiError  # Importing the custom ApiError class
from dotenv import load_dotenv
import os
#Loading dot env
load_dotenv()

async def verify_jwt(request: Request):
    """Middleware to verify JWT and attach user to request"""
    token = request.cookies.get("accessToken") or request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    if not token:
        raise ApiError(401, "Unauthorized request")

    try:
        decoded_token = jwt.decode(token, os.getenv("access_token_secret"), algorithms=["HS256"])
        user = await User.find_one({"_id": decoded_token.get("_id")}, projection={"password": 0, "refreshToken": 0, "emailVerificationToken": 0, "emailVerificationExpiry": 0})
        if not user:
            raise ApiError(401, "Invalid access token")
        return user
    except JWTError as error:
        raise ApiError(401, str(error) or "Invalid access token")

async def get_logged_in_user_or_ignore(request: Request) -> Optional[User]:
    """Middleware to get logged-in user if available (for unprotected routes)"""
    token = request.cookies.get("accessToken") or request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    try:
        decoded_token = jwt.decode(token,os.getenv("access_token_secret"), algorithms=["HS256"])
        return await User.find_one({"_id": decoded_token.get("_id")}, projection={"password": 0, "refreshToken": 0, "emailVerificationToken": 0, "emailVerificationExpiry": 0})
    except JWTError:
        return None  # Fail silently

def verify_permission(roles: List[str]):
    """Middleware to check if user has the required roles"""
    async def permission_dependency(user: User = Depends(verify_jwt)):
        if not user or user.role not in roles:
            raise ApiError(403, "You are not allowed to perform this action")
        return user

    return permission_dependency

__all__ = ["verify_jwt", "get_logged_in_user_or_ignore", "verify_permission"]
