from fastapi import APIRouter, Body, HTTPException

from app.core.users_service import (
    add_user,
    authenticate_user,
    delete_user,
    get_user_by_id,
    update_user,
)
from app.models.user import LoginSchema, UpdateUserSchema, UserSchema

router = APIRouter()


@router.post("/users", response_description="Add new user", response_model=UserSchema)
async def create_user(user: UserSchema = Body(...)):
    try:
        user = user.model_dump()
        new_user = await add_user(user)
        return new_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao criar o usuário")


@router.get(
    "/users/{user_id}", response_description="Get a user", response_model=UserSchema
)
async def get_user(user_id: str):
    user = await get_user_by_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.put(
    "/users/{user_id}", response_description="Update user", response_model=UserSchema
)
async def update_user_data(user_id: str, user: UpdateUserSchema = Body(...)):
    updated_user = await update_user(user_id, user.model_dump(exclude_unset=True))
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/users/{user_id}", response_description="Delete user")
async def delete_user_by_id(user_id: str):
    deleted = await delete_user(user_id)
    if deleted:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/users/login", response_description="Login user")
async def login_user(login: LoginSchema = Body(...)):
    user = await authenticate_user(login.email, login.password)
    if user:
        return user
    raise HTTPException(status_code=400, detail="Invalid email or password")
