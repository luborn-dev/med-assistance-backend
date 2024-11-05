from bson import ObjectId

from app.config.database import db


async def get_procedures_collection():
    return await db.get_collection("prontuarios")


def procedure_helper(procedure) -> dict:
    return {
        "id": str(procedure["_id"]),
        "paciente_id": str(procedure["paciente_id"]),
        "medico_id": str(procedure["medico_id"]),
        "data_atendimento": procedure["data_atendimento"].strftime("%Y-%m-%d"),
        "gravacoes": procedure.get("gravacoes", []),
        "resumo_inteligencia": procedure.get("resumo_inteligencia", {}),
    }


async def add_procedure(procedure_data: dict) -> dict:
    procedures_collection = await get_procedures_collection()
    procedure = await procedures_collection.insert_one(procedure_data)
    new_procedure = await procedures_collection.find_one({"_id": procedure.inserted_id})
    return procedure_helper(new_procedure)


async def get_procedure(id: str) -> dict:
    procedures_collection = await get_procedures_collection()
    procedure = await procedures_collection.find_one({"_id": ObjectId(id)})
    if procedure:
        return procedure_helper(procedure)
    return None


async def get_procedures_by_patient_id(patient_id: str):
    procedures_collection = await get_procedures_collection()
    procedures = []
    async for procedure in procedures_collection.find(
        {"paciente_id": ObjectId(patient_id)}
    ):
        procedures.append(procedure_helper(procedure))
    return procedures


async def update_procedure(id: str, procedure_data: dict):
    procedures_collection = await get_procedures_collection()
    result = await procedures_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": procedure_data}
    )
    return result.modified_count > 0


async def delete_procedure(id: str):
    procedures_collection = await get_procedures_collection()
    result = await procedures_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
