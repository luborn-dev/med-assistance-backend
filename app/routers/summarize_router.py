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

        full_text = "\n\n".join(
            f"- **Sintomas e Queixas**: {item.get('symptoms_and_complaints', '')}\n"
            f"- **Histórico Médico**: {item.get('medical_history', '')}\n"
            f"- **Diagnóstico**: {item.get('diagnosis', '')}\n"
            f"- **Tratamentos e Procedimentos**: {item.get('treatments_and_procedures', '')}\n"
            f"- **Recomendações**: {item.get('recommendations', '')}\n"
            for item in request.sumarizacoes
        )

        print(full_text)

        response_model = await summarize_transcription(full_text, "medical_history")

        if not response_model:
            raise HTTPException(
                status_code=500, detail="Summarization returned an empty response."
            )

        logger.info(f"Summarization successful: {response_model}")
        return JSONResponse(
            content=response_model,
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
