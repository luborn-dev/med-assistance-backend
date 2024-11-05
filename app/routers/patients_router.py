from typing import List

from fastapi import APIRouter, Body, HTTPException, Query, status

from app.core.patients_service import (
    add_patient,
    delete_patient,
    get_patient,
    get_patients_by_doctor_id,
    update_patient,
)
from app.models.patient import PatientSchema, UpdatePatientSchema

router = APIRouter()


@router.post(
    "/patients", response_description="Add new patient", response_model=PatientSchema
)
async def create_patient(patient: PatientSchema = Body(...)):
    try:
        new_patient = await add_patient(patient.dict())
        return new_patient
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating patient")


@router.get(
    "/patients",
    response_description="Get patients by doctor ID",
    response_model=List[PatientSchema],
)
async def get_patients_by_doctor_id(doctor_id: str = Query(...)):
    patients = await get_patients_by_doctor_id(doctor_id)
    return patients


@router.get(
    "/patients/{id}", response_description="Get a patient", response_model=PatientSchema
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
    response_model=PatientSchema,
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
