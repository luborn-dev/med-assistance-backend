from typing import List

from fastapi import APIRouter, Body, HTTPException, Query, status

from app.core.procedures_service import (
    add_procedure,
    delete_procedure,
    get_procedure,
    get_procedures_by_patient_id,
    update_procedure,
)
from app.models.procedure import ProcedureSchema, UpdateProcedureSchema

router = APIRouter()


@router.post(
    "/procedures",
    response_description="Add new procedure",
    response_model=ProcedureSchema,
)
async def create_procedure(procedure: ProcedureSchema = Body(...)):
    try:
        new_procedure = await add_procedure(procedure.dict())
        return new_procedure
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating procedure")


@router.get(
    "/procedures/{id}",
    response_description="Get a procedure",
    response_model=ProcedureSchema,
)
async def get_procedure_data(id: str):
    procedure = await get_procedure(id)
    if not procedure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Procedure not found"
        )
    return procedure


@router.get(
    "/procedures",
    response_description="Get procedures by patient ID",
    response_model=List[ProcedureSchema],
)
async def get_procedures_by_patient(patient_id: str = Query(...)):
    procedures = await get_procedures_by_patient_id(patient_id)
    return procedures


@router.put(
    "/procedures/{id}",
    response_description="Update a procedure",
    response_model=ProcedureSchema,
)
async def update_procedure_data(id: str, procedure: UpdateProcedureSchema = Body(...)):
    updated = await update_procedure(id, procedure.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Procedure not found"
        )
    return await get_procedure(id)


@router.delete("/procedures/{id}", response_description="Delete a procedure")
async def delete_procedure_data(id: str):
    deleted = await delete_procedure(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Procedure not found"
        )
    return {"message": "Procedure deleted successfully"}
