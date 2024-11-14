import datetime

from bson import ObjectId

from app.config.database import db
from app.core.utils.password_hash import PasswordHash

pw_hash = PasswordHash()


async def get_usuarios_collection():
    return await db.get_collection("Usuarios")


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "professional_id": user["professional_id"],
        "date_creation": user.get("date_creation"),
    }


async def add_user(user_data: dict) -> dict:
    user_data["password"] = pw_hash.hash_password(user_data["password"])
    user_data["date_creation"] = datetime.datetime.utcnow()
    usuarios_collection = await get_usuarios_collection()

    user = await usuarios_collection.insert_one(user_data)
    new_user = await usuarios_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def get_user_by_id(user_id: str):
    usuarios_collection = await get_usuarios_collection()
    if not ObjectId.is_valid(user_id):
        return None
    user = await usuarios_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user_helper(user)
    return None


async def authenticate_user(email: str, password: str):
    usuarios_collection = await get_usuarios_collection()
    user = await usuarios_collection.find_one({"email": email})

    if user and pw_hash.verify_password(password, user["password"]):
        return user_helper(user)
    return None


async def update_user(user_id: str, user_data: dict):
    usuarios_collection = await get_usuarios_collection()
    if "password" in user_data:
        user_data["password"] = pw_hash.hash_password(user_data["password"])

    result = await usuarios_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": user_data}
    )

    if result.modified_count > 0:
        updated_user = await usuarios_collection.find_one({"_id": ObjectId(user_id)})
        return user_helper(updated_user)
    return None


async def delete_user(user_id: str):
    usuarios_collection = await get_usuarios_collection()
    result = await usuarios_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0
