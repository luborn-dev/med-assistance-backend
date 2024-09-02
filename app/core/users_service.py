from passlib.context import CryptContext

from app.config.database import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_pacientes_collection():
    return await db.get_collection("Medicos")


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "affiliation": user["affiliation"],
    }


async def add_user(user_data: dict) -> dict:
    # Hash the password before storing it
    user_data["password"] = pwd_context.hash(user_data["password"])
    pacientes_collection = await get_pacientes_collection()
    user = await pacientes_collection.insert_one(user_data)
    new_user = await pacientes_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def authenticate_user(email: str, password: str):
    pacientes_collection = await get_pacientes_collection()
    user = await pacientes_collection.find_one({"email": email})
    if user and pwd_context.verify(password, user["password"]):
        return user_helper(user)
    return None


async def update_user_password(email: str, new_password: str):
    pacientes_collection = await get_pacientes_collection()
    hashed_password = pwd_context.hash(new_password)
    await pacientes_collection.update_one(
        {"email": email}, {"$set": {"password": hashed_password}}
    )
