from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    professional_id: str
    date_creation: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class UpdateUserSchema(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    professional_id: Optional[str]

    class Config:
        orm_mode = True


class UpdatePasswordSchema(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str
