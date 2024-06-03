from bson import ObjectId

from app.config.database import db
from app.models.patient_model import PatientModel


async def get_patients_collection():
    return db.get_collection("Patients")


def patient_helper(patient) -> dict:
    return {
        "id": str(patient["_id"]),
        "name": patient["name"],
        "birthdate": str(patient["birthdate"]),
        "address": patient["address"],
        "cpf": patient["cpf"],
        "phone": patient["phone"],
    }


async def add_patient(patient_data: dict) -> dict:
    patients_collection = await get_patients_collection()
    patient = await patients_collection.insert_one(patient_data)
    new_patient = await patients_collection.find_one({"_id": patient.inserted_id})
    return patient_helper(new_patient)


async def get_patient(id: str) -> dict:
    patients_collection = await get_patients_collection()
    patient = await patients_collection.find_one({"_id": ObjectId(id)})
    if patient:
        return patient_helper(patient)
    return None


async def get_all_patients():
    patients_collection = await get_patients_collection()
    patients = []
    async for patient in patients_collection.find():
        patients.append(patient_helper(patient))
    return patients


async def update_patient(id: str, patient_data: dict):
    patients_collection = await get_patients_collection()
    if len(patient_data) < 1:
        return False
    patient = await patients_collection.find_one({"_id": ObjectId(id)})
    if patient:
        updated_patient = await patients_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": patient_data}
        )
        if updated_patient:
            return True
    return False


async def delete_patient(id: str):
    patients_collection = await get_patients_collection()
    patient = await patients_collection.find_one({"_id": ObjectId(id)})
    if patient:
        await patients_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False
