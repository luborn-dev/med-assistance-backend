import logging

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.models.summarize import SummarizeRequest, SummarizeResponse
from app.utils import pre_processing_summarize
from app.utils.summarize import summarize_transcription

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/medical_history",
    response_description="Generate a Medical History Summary",
    response_model=SummarizeResponse,
)
async def summarize(request: SummarizeRequest = Body(...)):
    try:
        if not request.sumarizacoes:
            raise HTTPException(
                status_code=400, detail="The 'sumarizacoes' field cannot be empty."
            )

        full_text = "\n".join(request.sumarizacoes)

        prompt = pre_processing_summarize.gerar_prompt_para_historico_medico(full_text)

        text = await summarize_transcription(prompt)
        if not text:
            raise HTTPException(
                status_code=500, detail="Summarization returned an empty response."
            )

        logger.info(f"Summarization successful: {text}")
        return JSONResponse(
            content=text,
            media_type="application/json; charset=utf-8",
        )

    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=422, detail="Invalid input data.")

    except HTTPException as he:
        logger.warning(f"HTTP exception: {he.detail}")
        raise he

    except Exception as e:
        logger.error(f"Unexpected error during summarization: {e}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred during summarization."
        )
