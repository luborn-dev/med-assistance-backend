import logging
import uuid
from pathlib import Path

import speech_recognition as sr
from bson import ObjectId
from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile, status
from pydub import AudioSegment

from app.core.procedures_service import (
    add_gravacao,
    get_all_gravacoes,
    get_all_gravacoes_by_paciente_id,
    get_procedures_collection,
)
from app.models.procedure import GravacaoSchema
from app.utils import pre_processing_summarize
from app.utils.summarize import summarize_transcription

logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_DIR = Path.home() / "temp_audio"

if not UPLOAD_DIR.exists():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post(
    "/procedures",
    response_description="Adicionar nova gravação",
)
async def create_gravacao(gravacao: GravacaoSchema = Body(...)):
    logger.info("Received request to add a new recording.")
    try:
        new_procedure = await add_gravacao(gravacao.model_dump())
        logger.info(f"Recording added successfully: {new_procedure}")
        return new_procedure
    except Exception as e:
        logger.error(f"Error adding recording: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao adicionar gravação: {str(e)}"
        )


@router.post(
    "/procedures/upload",
    response_description="Adicionar nova gravação com arquivo de áudio",
)
async def create_gravacao_with_audio(
    paciente_id: str = Form(...),
    medico_id: str = Form(...),
    tipo: str = Form(...),
    procedimento: str = Form(""),
    transcricao: str = Form(""),
    sumarizacao: str = Form(""),
    arquivo_audio: UploadFile = File(...),
):
    logger.info(
        f"Received request to add a recording with audio for patient ID: {paciente_id}"
    )

    if not paciente_id or not medico_id:
        logger.warning("Missing required fields: paciente_id or medico_id.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="paciente_id e medico_id são obrigatórios.",
        )

    try:
        paciente_id = ObjectId(paciente_id)
        medico_id = ObjectId(medico_id)
    except Exception:
        logger.error("Invalid ObjectId format for paciente_id or medico_id.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="paciente_id e medico_id devem ser ObjectId válidos.",
        )

    file_extension = arquivo_audio.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_location = UPLOAD_DIR / unique_filename

    try:
        with open(file_location, "wb") as f:
            f.write(await arquivo_audio.read())
        logger.info(f"Audio file saved at {file_location}")
    except Exception as e:
        logger.error(f"Error saving audio file: {e}")
        raise HTTPException(status_code=500, detail="Não foi possível salvar o arquivo")

    try:
        audio = AudioSegment.from_file(str(file_location))
        wav_location = file_location.with_suffix(".wav")
        audio.export(wav_location, format="wav")
        logger.info(f"Audio converted to WAV format: {wav_location}")
    except Exception as e:
        logger.error(f"Error converting audio file: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao converter o arquivo: {str(e)}"
        )

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(str(wav_location)) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="pt-BR")
            logger.info(f"Transcription successful: {text}")
    except sr.UnknownValueError:
        logger.warning("Audio transcription failed: Unable to understand audio.")
        raise HTTPException(
            status_code=400,
            detail="Não foi possível entender o áudio. Verifique a qualidade da gravação e tente novamente.",
        )
    except sr.RequestError as e:
        logger.error(f"Speech recognition service unavailable: {e}")
        raise HTTPException(
            status_code=503,
            detail="Serviço de reconhecimento de voz indisponível. Por favor, tente novamente mais tarde.",
        )
    except Exception as e:
        logger.error(f"Unexpected error during transcription: {e}")
        raise HTTPException(
            status_code=500, detail=f"Ocorreu um erro durante a transcrição: {str(e)}"
        )

    if file_location.exists():
        file_location.unlink()
        logger.debug(f"Temporary file {file_location} deleted.")
    if wav_location.exists():
        wav_location.unlink()
        logger.debug(f"Temporary WAV file {wav_location} deleted.")

    try:
        prompt = pre_processing_summarize.gerar_prompt_para_sumarizacao(text)
        summarize = await summarize_transcription(prompt, "medical_procedure")
        logger.info(f"Summarization generated successfully.")
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao adicionar gravação: {str(e)}"
        )

    gravacao_data = {
        "paciente_id": paciente_id,
        "medico_id": medico_id,
        "tipo": tipo,
        "procedimento": procedimento,
        "transcricao": text,
        "sumarizacao": summarize,
    }
    gravacao = GravacaoSchema(**gravacao_data)

    new_procedure = await add_gravacao(gravacao.model_dump())
    logger.info(f"Recording with audio added successfully: {new_procedure}")
    return new_procedure


@router.get(
    "/procedures/{paciente_id}",
    response_description="Obter todas as gravações de um paciente",
    response_model=dict(),
)
async def get_gravacoes_paciente(paciente_id: str):
    logger.info(f"Fetching all recordings for patient ID: {paciente_id}")
    gravacoes = await get_all_gravacoes_by_paciente_id(paciente_id)
    if not gravacoes:
        logger.warning(f"No recordings found for patient ID: {paciente_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado ou sem gravações",
        )
    logger.info(f"Found {len(gravacoes)} recordings for patient ID: {paciente_id}")
    return gravacoes


@router.get(
    "/procedures",
    response_description="Obter todas as gravações",
)
async def get_all_gravacoes_endpoint():
    logger.info("Fetching all recordings.")
    try:
        gravacoes = await get_all_gravacoes()
        if not gravacoes:
            logger.warning("No recordings found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma gravação encontrada",
            )
        logger.info(f"Fetched {len(gravacoes)} recordings.")
        return gravacoes
    except Exception as e:
        logger.error(f"Error fetching recordings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter gravações: {str(e)}",
        )


@router.delete(
    "/procedures/{procedure_id}/recordings/{recording_id}",
    response_description="Deletar uma gravação específica",
)
async def delete_gravacao(procedure_id: str, recording_id: str):
    procedures_collection = await get_procedures_collection()
    result = await procedures_collection.update_one(
        {"_id": ObjectId(procedure_id)},
        {"$pull": {"gravacoes": {"_id": ObjectId(recording_id)}}},
    )
    if result.modified_count == 1:
        return {"message": "Gravação deletada com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Gravação não encontrada")
