from typing import List

from fastapi import APIRouter, Body, HTTPException, status

from app.core.patients_service import (
    add_patient,
    delete_patient,
    get_all_patients,
    get_patient,
    update_patient,
)
from app.models.patient import PatientSchema, UpdatePatientSchema

router = APIRouter()


@router.post("/patients", response_description="Add new patient", response_model=dict())
async def create_patient(patient: PatientSchema = Body(...)):
    try:
        new_patient = await add_patient(patient.model_dump())
        return new_patient
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating patient")


@router.get(
    "/patients",
    response_description="Get patients",
    response_model=List[dict],
)
async def get_all_patients_data(skip: int = 0, limit: int = 10):
    patients = await get_all_patients()
    if not patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No patients found"
        )
    return patients


@router.get(
    "/patients/{id}", response_description="Get a patient", response_model=dict()
)
async def get_patient_data(id: str):
    patient = await get_patient(id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    return patient


@router.put(
    "/patients/{id}",
    response_description="Update a patient",
    response_model=dict(),
)
async def update_patient_data(id: str, patient: UpdatePatientSchema = Body(...)):
    updated = await update_patient(id, patient.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    return await get_patient(id)


@router.delete("/patients/{id}", response_description="Delete a patient")
async def delete_patient_data(id: str):
    deleted = await delete_patient(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    return {"message": "Patient deleted successfully"}
