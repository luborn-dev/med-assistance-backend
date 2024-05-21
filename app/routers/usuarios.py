from typing import Optional

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from app.services.usuarios_service import add_user, authenticate_user

router = APIRouter()


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    affiliation: Optional[str] = None


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


@router.post("/api/users/register", response_description="Add new user")
async def create_user(user: UserSchema = Body(...)):
    user = user.model_dump()
    new_user = await add_user(user)
    return new_user


@router.post("/api/users/login", response_description="Login user")
async def login_user(login: LoginSchema = Body(...)):
    user = await authenticate_user(login.email, login.password)
    if user:
        return user
    raise HTTPException(status_code=400, detail="Invalid email or password")
