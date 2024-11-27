import logging
from typing import Any, Dict

from bson import ObjectId
from fastapi import HTTPException

from app.config.database import db

logger = logging.getLogger(__name__)


async def get_content_collection():
    logger.debug("Fetching 'Conteudo' collection from the database.")
    try:
        return await db.get_collection("Conteudo")
    except Exception as e:
        logger.error(f"Error accessing the collection 'Conteudo': {e}")
        raise HTTPException(status_code=500, detail="Database connection error")


def content_helper(conteudo: dict) -> dict:
    logger.debug(f"Formatting content data: {conteudo}")
    try:
        return {
            "id": str(conteudo["_id"]),
            "content_type": conteudo["content_type"],
            "content": conteudo["content"],
        }
    except KeyError as e:
        logger.error(f"Error processing content data: Missing key {e}")
        raise HTTPException(status_code=500, detail="Error processing content data")


async def get_content_by_type(content_type: str) -> Dict[str, Any]:
    logger.info(f"Fetching content by type: {content_type}")
    try:
        content_collection = await get_content_collection()
        content = await content_collection.find_one({"content_type": content_type})
        if content:
            logger.info(f"Content found for type: {content_type}")
            return content_helper(content)
        logger.warning(f"Content type '{content_type}' not found")
        raise HTTPException(
            status_code=404, detail=f"Content type '{content_type}' not found"
        )
    except HTTPException as e:
        logger.warning(f"HTTP exception during fetch: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching content: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching content",
        )
