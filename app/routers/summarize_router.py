from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.utils import pre_processing_summarize
from app.utils.summarize import summarize_transcription


class SummarizeRequest(BaseModel):
    patientId: str
    sumarizacoes: list[str]


class SummarizeResponse(BaseModel):
    text: str


router = APIRouter()


@router.post(
    "/medical_history",
    response_description="Generate a Medical History Summary",
    response_model=SummarizeResponse,
)
async def summarize(request: SummarizeRequest = Body(...)):
    full_text = "\n".join(request.sumarizacoes)

    prompt = pre_processing_summarize.gerar_prompt_para_historico_medico(full_text)

    text = await summarize_transcription(prompt)
    return JSONResponse(
        content=text,
        media_type="application/json; charset=utf-8",
    )
