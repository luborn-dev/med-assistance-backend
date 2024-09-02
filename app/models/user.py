from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    affiliation: Optional[str] = None


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class UpdatePasswordSchema(BaseModel):
    email: str
    old_password: str
    new_password: str
