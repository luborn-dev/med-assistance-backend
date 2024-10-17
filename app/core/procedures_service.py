from datetime import datetime, timezone
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
        "summarize": procedure.get("summarize", ""),
        "created_at": procedure.get("created_at"),
    }


async def get_procedures_collection():
    return await db.get_collection("Procedures")


async def add_procedure(procedure_data: dict) -> dict:
    procedures_collection = await get_procedures_collection()

    # procedure_data["created_at"] = datetime.now(timezone.utc)

    procedure = await procedures_collection.insert_one(procedure_data)
    new_procedure = await procedures_collection.find_one({"_id": procedure.inserted_id})
    return procedure_helper(new_procedure)


async def get_all_procedures(doctor_id: str) -> list:
    procedures_collection = await get_procedures_collection()

    procedures = (
        await procedures_collection.find({"doctorId": doctor_id})
        .sort("created_at", -1)
        .to_list(1000)
    )

    return [procedure_helper(procedure) for procedure in procedures]


async def delete_procedure_by_id(procedure_id: str):
    collection = await get_procedures_collection()
    delete_result = await collection.delete_one({"_id": ObjectId(procedure_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Procedimento deletado com sucesso"}
    else:
        return {"message": "Procedimento não encontrado"}
