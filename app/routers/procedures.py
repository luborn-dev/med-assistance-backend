import os
from pathlib import Path

import speech_recognition as sr
from fastapi import APIRouter, Body, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydub import AudioSegment

from app.models.procedure_model import ProcedureModel
from app.services.procedures_service import add_procedure

router = APIRouter()

UPLOAD_DIR = Path.home() / "recordings"

if not UPLOAD_DIR.exists():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/api/procedures", response_description="Adicionar novo procedimento")
async def create_procedure(procedure: ProcedureModel = Body(...)):
    procedure = procedure.model_dump()
    new_procedure = await add_procedure(procedure)
    return new_procedure


@router.post("/api/procedures/upload", response_description="Carregando uma gravação")
async def upload_recording(file: UploadFile = File(...)):
    accepted_file_types = [
        "audio/mpeg",
        "audio/mp4",
        "audio/wav",
        "audio/x-wav",
        "audio/x-m4a",
        "audio/aac",
    ]

    if file.content_type not in accepted_file_types:
        raise HTTPException(
            status_code=400, detail=f"Tipo de arquivo inválido: {file.content_type}"
        )

    file_location = UPLOAD_DIR / file.filename

    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Verifique se o arquivo foi salvo corretamente
    if not file_location.exists():
        raise HTTPException(status_code=500, detail="O arquivo não pôde ser salvo")

    # Convert the audio file to wav format for recognition
    try:
        audio = AudioSegment.from_file(str(file_location))
        wav_location = file_location.with_suffix(".wav")
        audio.export(wav_location, format="wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao converter arquivo: {e}")

    # Perform speech-to-text
    recognizer = sr.Recognizer()
    text = ""
    try:
        with sr.AudioFile(str(wav_location)) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="pt-BR")
            print(f"Transcrição: {text}")
    except sr.UnknownValueError:
        print("O reconhecimento de fala do Google não conseguiu entender o áudio")
    except sr.RequestError as e:
        print(
            f"Não foi possível solicitar resultados do serviço Google Speech Recognition; {e}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during transcription: {e}")

    return JSONResponse(
        content={
            "filename": file.filename,
            "content_type": file.content_type,
            "saved_location": str(file_location),
            "transcription": text,
        }
    )
