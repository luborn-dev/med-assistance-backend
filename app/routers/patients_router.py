import logging
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

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/patients", response_description="Add new patient", response_model=dict())
async def create_patient(patient: PatientSchema = Body(...)):
    logger.info("Received request to create a new patient.")
    try:
        new_patient = await add_patient(patient.model_dump())
        logger.info(f"Patient created successfully: {new_patient}")
        return new_patient
    except Exception as e:
        logger.error(f"Error creating patient: {e}")
        raise HTTPException(status_code=500, detail="Error creating patient")


@router.get(
    "/patients",
    response_description="Get patients",
    response_model=List[dict],
)
async def get_all_patients_data(skip: int = 0, limit: int = 10):
    logger.info(f"Fetching patients with skip={skip} and limit={limit}.")
    patients = await get_all_patients()
    if not patients:
        logger.warning("No patients found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No patients found"
        )
    logger.info(f"Fetched {len(patients)} patients.")
    return patients


@router.get(
    "/patients/{id}", response_description="Get a patient", response_model=dict()
)
async def get_patient_data(id: str):
    logger.info(f"Fetching patient with ID: {id}")
    patient = await get_patient(id)
    if not patient:
        logger.warning(f"Patient not found for ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    logger.info(f"Patient found: {patient}")
    return patient


@router.put(
    "/patients/{id}",
    response_description="Update a patient",
    response_model=dict(),
)
async def update_patient_data(id: str, patient: UpdatePatientSchema = Body(...)):
    logger.info(f"Received request to update patient with ID: {id}")
    patient_data = {
        key: value
        for key, value in patient.model_dump(exclude_unset=True).items()
        if value is not None
    }
    logger.debug(f"Update data for patient: {patient_data}")

    if not patient_data:
        logger.warning("No valid data provided for update.")
        raise HTTPException(status_code=400, detail="No valid data provided for update")

    updated = await update_patient(id, patient_data)
    if not updated:
        logger.warning(f"Patient not found or not updated for ID: {id}")
        raise HTTPException(status_code=404, detail="Patient not found")

    updated_patient = await get_patient(id)
    logger.info(f"Patient updated successfully: {updated_patient}")
    return updated_patient


@router.delete("/patients/{id}", response_description="Delete a patient")
async def delete_patient_data(id: str):
    logger.info(f"Received request to delete patient with ID: {id}")
    deleted = await delete_patient(id)
    if not deleted:
        logger.warning(f"Patient not found for deletion with ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    logger.info(f"Patient deleted successfully with ID: {id}")
    return {"message": "Patient deleted successfully"}
