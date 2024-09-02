from fastapi import APIRouter, Body, HTTPException

from app.models.user import LoginSchema, UpdatePasswordSchema, UserSchema
from app.services.users_service import add_user, authenticate_user, update_user_password

router = APIRouter()


@router.post("/api/users/register", response_description="Add new user")
async def create_user(user: UserSchema = Body(...)):
    try:
        user = user.model_dump()
        new_user = await add_user(user)
        print(new_user)
    except Exception as e:
        print(e)
    return new_user


@router.post("/api/users/login", response_description="Login user")
async def login_user(login: LoginSchema = Body(...)):
    user = await authenticate_user(login.email, login.password)
    if user:
        return user
    raise HTTPException(status_code=400, detail="Invalid email or password")


@router.post("/api/users/update_password", response_description="Update user password")
async def update_password(update_password: UpdatePasswordSchema = Body(...)):
    print(update_password)
    user = await authenticate_user(update_password.email, update_password.old_password)
    if user:
        if update_password.old_password == update_password.new_password:
            raise HTTPException(
                status_code=400,
                detail="New password cannot be the same as the old password",
            )

        await update_user_password(update_password.email, update_password.new_password)
        return {"message": "Password updated successfully"}
    raise HTTPException(status_code=400, detail="Invalid email or password")
