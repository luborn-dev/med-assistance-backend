from datetime import date, datetime

from bson import ObjectId

from app.config.database import db


async def get_pacientes_collection():
    return await db.get_collection("Pacientes")


def mask_cpf(cpf: str) -> str:
    """Mascarar o CPF no formato 'XXX.XXX.XXX-XX'."""
    if cpf and len(cpf) == 14:
        return f"{cpf[:3]}.***.***-{cpf[-2:]}"
    return cpf


def patient_helper(patient) -> dict:
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
    patients_collection = await get_pacientes_collection()

    if "birth_date" in patient_data and isinstance(patient_data["birth_date"], date):
        patient_data["birth_date"] = datetime.combine(
            patient_data["birth_date"], datetime.min.time()
        )

    patient_data["register_date"] = datetime.now()

    patient = await patients_collection.insert_one(patient_data)
    new_patient = await patients_collection.find_one({"_id": patient.inserted_id})
    return patient_helper(new_patient)


async def get_patient(id: str) -> dict:
    patients_collection = await get_pacientes_collection()
    patient = await patients_collection.find_one({"_id": ObjectId(id)})
    if patient:
        return patient_helper(patient)
    return None


async def get_all_patients() -> list:
    patients_collection = await get_pacientes_collection()
    patients_cursor = patients_collection.find()
    patients = []
    async for patient in patients_cursor:
        patients.append(patient_helper(patient))
    return patients


async def update_patient(id: str, patient_data: dict):
    patients_collection = await get_pacientes_collection()

    if "birth_date" in patient_data and isinstance(patient_data["birth_date"], date):
        patient_data["birth_date"] = datetime.combine(
            patient_data["birth_date"], datetime.min.time()
        )

    if not patient_data:
        return False

    result = await patients_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": patient_data}
    )
    return result.modified_count > 0


async def delete_patient(id: str):
    patients_collection = await get_pacientes_collection()
    result = await patients_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
