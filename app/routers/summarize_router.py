from fastapi import APIRouter, Body
from pydantic import BaseModel

from app.models.summarize_service import summarize_transcription


class SummarizeRequest(BaseModel):
    text: str


class SummarizeResponse(BaseModel):
    text: str


router = APIRouter()


@router.post(
    "/api/summarize",
    response_description="Summarize a Transcription",
    response_model=SummarizeResponse,
)
async def summarize(request: SummarizeRequest = Body(...)):
    text = await summarize_transcription(request.text)
    return SummarizeResponse(text=text)
