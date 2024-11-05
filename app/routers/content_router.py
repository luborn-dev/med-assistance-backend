from typing import List

from fastapi import APIRouter, HTTPException

from app.core.content_service import get_content_by_id, get_content_by_type
from app.models.content import Content

router = APIRouter()


@router.get("/content/{content_type}", response_model=List[Content])
async def read_contents(content_type: str):
    try:
        content = await get_content_by_type(content_type)
        if not content:
            raise HTTPException(
                status_code=404, detail=f"Content type '{content_type}' not found"
            )
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/content/{id}", response_model=Content)
async def read_content(id: str):
    return await get_content_by_id(id)
