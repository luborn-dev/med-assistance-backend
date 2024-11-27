import datetime
import logging

from bson import ObjectId

from app.config.database import db
from app.core.utils.password_hash import PasswordHash

logger = logging.getLogger(__name__)
pw_hash = PasswordHash()


async def get_usuarios_collection():
    logger.debug("Fetching 'Usuarios' collection from the database.")
    return await db.get_collection("Usuarios")


def user_helper(user) -> dict:
    logger.debug(f"Formatting user data: {user}")
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "professional_id": user["professional_id"],
        "date_creation": user.get("date_creation"),
    }


async def add_user(user_data: dict) -> dict:
    logger.info("Adding a new user.")
    user_data["password"] = pw_hash.hash_password(user_data["password"])
    user_data["date_creation"] = datetime.datetime.utcnow()
    logger.debug(f"User data after hashing: {user_data}")
    usuarios_collection = await get_usuarios_collection()

    user = await usuarios_collection.insert_one(user_data)
    new_user = await usuarios_collection.find_one({"_id": user.inserted_id})
    logger.info(f"User added successfully with ID: {user.inserted_id}")
    return user_helper(new_user)


async def get_user_by_id(user_id: str):
    logger.info(f"Fetching user by ID: {user_id}")
    usuarios_collection = await get_usuarios_collection()
    if not ObjectId.is_valid(user_id):
        logger.warning(f"Invalid ObjectId format: {user_id}")
        return None
    user = await usuarios_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        logger.info(f"User found: {user}")
        return user_helper(user)
    logger.warning(f"User not found for ID: {user_id}")
    return None


async def authenticate_user(email: str, password: str):
    logger.info(f"Authenticating user with email: {email}")
    usuarios_collection = await get_usuarios_collection()
    user = await usuarios_collection.find_one({"email": email})

    if user and pw_hash.verify_password(password, user["password"]):
        logger.info(f"User authenticated successfully: {email}")
        return user_helper(user)
    logger.warning(f"Authentication failed for email: {email}")
    return None


async def update_user(user_id: str, user_data: dict):
    logger.info(f"Updating user with ID: {user_id}")
    if "password" in user_data:
        user_data["password"] = pw_hash.hash_password(user_data["password"])
        logger.debug(f"Updated password for user ID: {user_id}")

    usuarios_collection = await get_usuarios_collection()
    result = await usuarios_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": user_data}
    )

    if result.modified_count > 0:
        updated_user = await usuarios_collection.find_one({"_id": ObjectId(user_id)})
        logger.info(f"User updated successfully: {updated_user}")
        return user_helper(updated_user)
    logger.warning(f"No updates performed for user ID: {user_id}")
    return None


async def delete_user(user_id: str):
    logger.info(f"Deleting user with ID: {user_id}")
    usuarios_collection = await get_usuarios_collection()
    result = await usuarios_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count > 0:
        logger.info(f"User deleted successfully with ID: {user_id}")
    else:
        logger.warning(f"User not found for deletion with ID: {user_id}")
    return result.deleted_count > 0
