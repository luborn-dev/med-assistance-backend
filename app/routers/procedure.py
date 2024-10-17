import os
from pathlib import Path

import speech_recognition as sr
from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydub import AudioSegment

from app.core.procedures_service import (
    add_procedure,
    delete_procedure_by_id,
    get_all_procedures,
)
from app.core.summarize_service import summarize_transcription
from app.models.procedure import ProcedureModel
from app.utils.pre_processing_summarize import gerar_prompt_para_sumarizacao

router = APIRouter()

UPLOAD_DIR = Path.home() / "recordings"

if not UPLOAD_DIR.exists():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/api/procedures", response_description="Get all procedures")
async def get_procedures(doctor_id: str = None):
    procedures = await get_all_procedures(doctor_id)

    if procedures:
        return procedures
    raise HTTPException(status_code=404, detail="No procedures found")


@router.post("/api/procedures", response_description="Add new procedure")
async def create_procedure(procedure: ProcedureModel = Body(...)):
    procedure = procedure.model_dump()
    new_procedure = await add_procedure(procedure)
    return new_procedure


@router.post("/api/procedures/upload", response_description="Upload a recording")
async def upload_recording(
    procedure_type: str = Form(...),
    patient_name: str = Form(...),
    exact_procedure_name: str = Form(...),
    doctor_id: str = Form(...),
    file: UploadFile = File(...),
):
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
            status_code=400, detail=f"Invalid file type: {file.content_type}"
        )

    file_location = UPLOAD_DIR / file.filename

    with open(file_location, "wb") as f:
        f.write(await file.read())

    if not file_location.exists():
        raise HTTPException(status_code=500, detail="File could not be saved")

    try:
        audio = AudioSegment.from_file(str(file_location))
        wav_location = file_location.with_suffix(".wav")
        audio.export(wav_location, format="wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting file: {e}")

    recognizer = sr.Recognizer()
    text = ""
    try:
        with sr.AudioFile(str(wav_location)) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="pt-BR")
            print(f"Transcription: {text}")

    except sr.UnknownValueError:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível entender o áudio. Verifique a qualidade da gravação e tente novamente.",
        )
    except sr.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Serviço de reconhecimento de voz indisponível. Por favor, tente novamente mais tarde.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ocorreu um erro durante a transcrição: {e}"
        )

    prompt = gerar_prompt_para_sumarizacao(text)
    summarize = await summarize_transcription(prompt)

    procedure_data = {
        "procedure_type": procedure_type,
        "patient_name": patient_name,
        "exact_procedure_name": exact_procedure_name,
        "doctorId": doctor_id,
        "transcription": text,
        "summarize": summarize,
    }

    new_procedure = await add_procedure(procedure_data)

    return JSONResponse(
        content={
            "filename": file.filename,
            "content_type": file.content_type,
            "saved_location": str(file_location),
            "doctorId": doctor_id,
            "transcription": text,
            "procedure": new_procedure,
        }
    )


@router.delete(
    "/api/procedures/{procedure_id}", response_description="Delete a procedure"
)
async def delete_procedure(procedure_id: str):
    delete_result = await delete_procedure_by_id(procedure_id)

    if delete_result.deleted_count == 1:
        return JSONResponse(
            status_code=200, content={"message": "Procedure deleted successfully"}
        )
    else:
        raise HTTPException(status_code=404, detail="Procedure not found")
