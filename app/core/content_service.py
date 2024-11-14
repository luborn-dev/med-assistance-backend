from typing import Any, Dict

from bson import ObjectId
from fastapi import HTTPException

from app.config.database import db


async def get_content_collection():
    return await db.get_collection("Conteudo")


def content_helper(conteudo: dict) -> dict:
    return {
        "id": str(conteudo["_id"]),
        "content_type": conteudo["content_type"],
        "content": conteudo["content"],
    }


async def get_content_by_type(content_type: str) -> Dict[str, Any]:
    content_collection = await get_content_collection()
    content = await content_collection.find_one({"content_type": content_type})
    if content:
        return content_helper(content)
    raise HTTPException(status_code=404, detail="Content not found")
