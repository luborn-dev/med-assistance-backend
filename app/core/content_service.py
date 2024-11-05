from typing import List

from bson import ObjectId
from fastapi import HTTPException

from app.config.database import db


async def get_content_collection():
    return await db.get_collection("Conteudo")


def content_helper(conteudo) -> dict:
    return {
        "id": str(conteudo["_id"]),
        "question": conteudo.get("question"),
        "answer": conteudo.get("answer"),
        "content_type": conteudo["content_type"],
    }


async def get_content_by_type(content_type: str) -> List[dict]:
    content_collection = await get_content_collection()
    content = []
    async for item in content_collection.find({"content_type": content_type}):
        content.append(content_helper(item))
    print(content)

    return content


async def get_content_by_id(id: str) -> dict:
    content_collection = await get_content_collection()
    content = await content_collection.find_one({"_id": ObjectId(id)})
    if content:
        return content_helper(content)
    raise HTTPException(status_code=404, detail="Content not found")
