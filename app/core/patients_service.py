from datetime import date, datetime

from bson import ObjectId
from fastapi import HTTPException

from app.config.database import db


async def get_pacientes_collection():
    return await db.get_collection("pacientes")


def patient_helper(patient) -> dict:
    return {
        "id": str(patient["_id"]),
        "nome": patient["nome"],
        "data_nascimento": patient["data_nascimento"].strftime("%Y-%m-%d"),
        "genero": patient["genero"],
        "cpf": patient["cpf"],
        "endereco": patient["endereco"],
        "data_registro": patient.get("data_registro"),
        "historico_medico": patient.get("historico_medico", []),
    }


async def add_patient(patient_data: dict) -> dict:
    patients_collection = await get_pacientes_collection()

    if "data_nascimento" in patient_data and isinstance(
        patient_data["data_nascimento"], date
    ):
        patient_data["data_nascimento"] = datetime.combine(
            patient_data["data_nascimento"], datetime.min.time()
        )

    patient_data["data_registro"] = datetime.utcnow()

    patient = await patients_collection.insert_one(patient_data)
    new_patient = await patients_collection.find_one({"_id": patient.inserted_id})
    return patient_helper(new_patient)


async def get_patient(id: str) -> dict:
    patients_collection = await get_pacientes_collection()
    patient = await patients_collection.find_one({"_id": ObjectId(id)})
    if patient:
        return patient_helper(patient)
    return None


async def get_patients_by_doctor_id(doctor_id: str):
    patients_collection = await get_pacientes_collection()
    patients = []
    async for patient in patients_collection.find({"medico_id": ObjectId(doctor_id)}):
        patients.append(patient_helper(patient))
    return patients


async def update_patient(id: str, patient_data: dict):
    patients_collection = await get_pacientes_collection()

    if "data_nascimento" in patient_data and isinstance(
        patient_data["data_nascimento"], date
    ):
        patient_data["data_nascimento"] = datetime.combine(
            patient_data["data_nascimento"], datetime.min.time()
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
