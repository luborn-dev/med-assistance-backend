from typing import List

from fastapi import APIRouter, HTTPException

from app.services.medicos_service import listar_medicos

router = APIRouter()


@router.get("/m2", response_model=List[dict])
async def mock():
    return [{"worked": "yes"}]


@router.get("/medicos", response_model=List[dict])
async def obter_medicos():
    try:
        medicos = await listar_medicos()
        return medicos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
