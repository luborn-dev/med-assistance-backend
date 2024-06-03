from datetime import datetime
from pydoc import doc

from bson import ObjectId

from app.config.database import db


def procedure_helper(procedure) -> dict:
    return {
        "id": str(procedure["_id"]),
        "procedure_type": procedure["procedure_type"],
        "patient_name": procedure["patient_name"],
        "exact_procedure_name": procedure["exact_procedure_name"],
        "doctor_id": procedure["doctorId"],
        "transcription": procedure["transcription"],
    }


async def get_procedures_collection():
    return await db.get_collection("Procedures")


async def add_procedure(procedure_data: dict) -> dict:
    print(procedure_data)
    procedures_collection = await get_procedures_collection()
    procedure = await procedures_collection.insert_one(procedure_data)
    new_procedure = await procedures_collection.find_one({"_id": procedure.inserted_id})
    return procedure_helper(new_procedure)


async def get_all_procedures(doctor_id: str) -> list:

    procedures_collection = await get_procedures_collection()
    procedures = await procedures_collection.find({"doctorId": doctor_id}).to_list(1000)

    return [procedure_helper(procedure) for procedure in procedures]


from bson import ObjectId


async def delete_procedure_by_id(procedure_id: str):
    collection = await get_procedures_collection()
    delete_result = await collection.delete_one({"_id": ObjectId(procedure_id)})
    return delete_result
