import logging

from fastapi import APIRouter, Body, HTTPException

from app.core.users_service import (
    add_user,
    authenticate_user,
    delete_user,
    get_user_by_id,
    update_user,
)
from app.models.user import LoginSchema, UpdateUserSchema, UserSchema

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/users", response_description="Add new user", response_model=dict())
async def create_user(user: UserSchema = Body(...)):
    logger.info("Received request to create a new user.")
    try:
        user_data = user.model_dump()
        logger.debug(f"User data to be added: {user_data}")
        new_user = await add_user(user_data)
        logger.info(f"User created successfully: {new_user}")
        return new_user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")


@router.get(
    "/users/{user_id}", response_description="Get a user by ID", response_model=dict()
)
async def get_user(user_id: str):
    logger.info(f"Received request to fetch user by ID: {user_id}")
    user = await get_user_by_id(user_id)
    if user:
        logger.info(f"User found: {user}")
        return user
    logger.warning(f"User not found for ID: {user_id}")
    raise HTTPException(status_code=404, detail="User not found")


@router.put(
    "/users/{user_id}", response_description="Update user", response_model=dict()
)
async def update_user_data(user_id: str, user: UpdateUserSchema = Body(...)):
    logger.info(f"Received request to update user with ID: {user_id}")
    user_data = user.model_dump(exclude_unset=True)
    logger.debug(f"Update data: {user_data}")
    updated_user = await update_user(user_id, user_data)
    if updated_user:
        logger.info(f"User updated successfully: {updated_user}")
        return updated_user
    logger.warning(f"User not found or not updated for ID: {user_id}")
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/users/{user_id}", response_description="Delete user")
async def delete_user_by_id(user_id: str):
    logger.info(f"Received request to delete user with ID: {user_id}")
    deleted = await delete_user(user_id)
    if deleted:
        logger.info(f"User deleted successfully with ID: {user_id}")
        return {"message": "User deleted successfully"}
    logger.warning(f"User not found or not deleted for ID: {user_id}")
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/login", response_description="Login user")
async def login_user(login: LoginSchema = Body(...)):
    logger.info(f"Login attempt for email: {login.email}")
    user = await authenticate_user(login.email, login.password)
    if user:
        logger.info(f"Login successful for user: {user}")
        return user
    logger.warning(f"Invalid login attempt for email: {login.email}")
    raise HTTPException(status_code=400, detail="Invalid email or password")
