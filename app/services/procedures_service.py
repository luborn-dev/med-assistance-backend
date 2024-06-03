from datetime import datetime

from bson import ObjectId

from app.config.database import db


def procedure_helper(procedure) -> dict:
    return {
        "id": str(procedure["_id"]),
        "procedure_type": procedure["procedure_type"],
        "patient_name": procedure["patient_name"],
        "exact_procedure_name": procedure["exact_procedure_name"],
        "birthdate": procedure["birthdate"],  # Mantemos como string
    }


async def get_procedures_collection():
    return await db.get_collection("Procedures")


async def add_procedure(procedure_data: dict) -> dict:
    # Convertemos a data para string antes de salvar
    procedure_data["birthdate"] = procedure_data["birthdate"].format()
    procedures_collection = await get_procedures_collection()
    procedure = await procedures_collection.insert_one(procedure_data)
    new_procedure = await procedures_collection.find_one({"_id": procedure.inserted_id})
    return procedure_helper(new_procedure)
