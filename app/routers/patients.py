from typing import List

from fastapi import APIRouter, Body, HTTPException, Query, status

from app.core.patients_service import (
    add_patient,
    delete_patient,
    get_patient,
    get_patients_by_doctor_id,
    update_patient,
)
from app.models.patient import PatientModel

router = APIRouter()


@router.post(
    "/api/patients", response_description="Add new patient", response_model=PatientModel
)
async def create_patient(patient: PatientModel = Body(...)):
    new_patient = await add_patient(patient.model_dump())
    return new_patient


@router.get(
    "/api/patients",
    response_description="Get patients by doctor ID",
    response_model=List[PatientModel],
)
async def read_patients_by_doctor_id(doctor_id: str = Query(...)):
    patients = await get_patients_by_doctor_id(doctor_id)
    return patients


@router.put(
    "/api/patients/{id}",
    response_description="Update a patient",
    response_model=PatientModel,
)
async def update_patient_data(id: str, patient: PatientModel = Body(...)):
    updated = await update_patient(id, patient.dict())
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {id} not found",
        )
    return await get_patient(id)


@router.delete("/api/patients/{id}", response_description="Delete a patient")
async def delete_patient_data(id: str):
    deleted = await delete_patient(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID {id} not found",
        )
    return {"message": "Patient deleted successfully"}
