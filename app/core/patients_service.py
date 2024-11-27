import logging
from datetime import date, datetime

from bson import ObjectId

from app.config.database import db

logger = logging.getLogger(__name__)


async def get_pacientes_collection():
    logger.debug("Fetching 'Pacientes' collection from the database.")
    return await db.get_collection("Pacientes")


def mask_cpf(cpf: str) -> str:
    """Mascarar o CPF no formato 'XXX.XXX.XXX-XX'."""
    logger.debug("Masking CPF.")
    if cpf and len(cpf) == 14:
        return f"{cpf[:3]}.***.***-{cpf[-2:]}"
    return cpf


def patient_helper(patient) -> dict:
    logger.debug(f"Formatting patient data: {patient}")
    return {
        "id": str(patient["_id"]),
        "name": patient["name"],
        "birth_date": patient["birth_date"],
        "gender": patient["gender"],
        "cpf": mask_cpf(patient.get("cpf")),
        "contact": patient["contact"],
        "address": patient["address"],
        "register_date": patient.get("register_date"),
    }


async def add_patient(patient_data: dict) -> dict:
    logger.info("Adding a new patient.")
    patients_collection = await get_pacientes_collection()

    if "birth_date" in patient_data and isinstance(patient_data["birth_date"], date):
        patient_data["birth_date"] = datetime.combine(
            patient_data["birth_date"], datetime.min.time()
        )

    patient_data["register_date"] = datetime.now()

    logger.debug(f"Patient data to be inserted: {patient_data}")
    patient = await patients_collection.insert_one(patient_data)
    new_patient = await patients_collection.find_one({"_id": patient.inserted_id})
    logger.info(f"Patient added successfully with ID: {patient.inserted_id}")
    return patient_helper(new_patient)


async def get_patient(id: str) -> dict:
    logger.info(f"Fetching patient with ID: {id}")
    patients_collection = await get_pacientes_collection()
    patient = await patients_collection.find_one({"_id": ObjectId(id)})
    if patient:
        logger.info(f"Patient found: {patient}")
        return patient_helper(patient)
    logger.warning(f"Patient not found for ID: {id}")
    return None


async def get_all_patients() -> list:
    logger.info("Fetching all patients.")
    patients_collection = await get_pacientes_collection()
    patients_cursor = patients_collection.find()
    patients = []
    async for patient in patients_cursor:
        patients.append(patient_helper(patient))
    logger.info(f"Fetched {len(patients)} patients.")
    return patients


async def update_patient(id: str, patient_data: dict):
    logger.info(f"Updating patient with ID: {id}")
    patients_collection = await get_pacientes_collection()

    try:
        if "birth_date" in patient_data:
            patient_data["birth_date"] = datetime.strptime(
                patient_data["birth_date"], "%Y-%m-%d"
            )

        if not patient_data:
            logger.warning("No valid data provided for update.")
            return False

        logger.debug(f"Patient update data: {patient_data}")
        result = await patients_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": patient_data}
        )
        if result.modified_count > 0:
            logger.info(f"Patient updated successfully with ID: {id}")
            return True
        logger.warning(f"No updates performed for patient ID: {id}")
        return False

    except Exception as e:
        logger.error(f"Error updating patient: {e}")
        return False


async def delete_patient(id: str):
    logger.info(f"Deleting patient with ID: {id}")
    patients_collection = await get_pacientes_collection()
    result = await patients_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        logger.info(f"Patient deleted successfully with ID: {id}")
    else:
        logger.warning(f"Patient not found for deletion with ID: {id}")
    return result.deleted_count > 0
