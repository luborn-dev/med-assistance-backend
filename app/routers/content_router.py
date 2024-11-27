import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.core.content_service import get_content_by_type
from app.models.content import Content

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/content/{content_type}", response_model=Content)
async def read_contents(content_type: str):
    logger.info(f"Received request to fetch content of type: {content_type}")
    try:
        content = await get_content_by_type(content_type)
        logger.info(f"Content fetched successfully for type: {content_type}")
        return JSONResponse(
            content=content, media_type="application/json; charset=utf-8"
        )
    except HTTPException as e:
        logger.warning(f"HTTP error occurred: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected server error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
