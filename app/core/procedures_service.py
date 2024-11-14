from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from app.config.database import db


async def get_procedures_collection():
    return await db.get_collection("Procedimentos")


async def get_procedures_view_collection():
    return await db.get_collection("ProceduresView")


def format_date(date: datetime) -> str:
    """Converte uma data para o formato dd/MM/yyyy - HH:mm."""
    return date.strftime("%d/%m/%Y - %H:%M") if date else None


def mask_cpf(cpf: str) -> str:
    """Mascarar o CPF no formato 'XXX.XXX.XXX-XX'."""
    if cpf and len(cpf) == 14:
        return f"{cpf[:3]}.***.***-{cpf[-2:]}"
    return cpf


def procedures_view_helper(procedure) -> dict:
    return {
        "paciente_info": {
            "name": procedure["paciente_info"]["name"],
            "birth_date": procedure["paciente_info"].get("birth_date"),
            "gender": procedure["paciente_info"].get("gender"),
            "cpf": mask_cpf(procedure["paciente_info"].get("cpf")),
            "contact": procedure["paciente_info"].get("contact"),
            "address": procedure["paciente_info"].get("address"),
        },
        "gravacoes": [
            {
                "data_gravacao": (
                    format_date(gravacao["data_gravacao"])
                    if "data_gravacao" in gravacao
                    else None
                ),
                "paciente_id": str(gravacao["paciente_id"]),
                "medico_id": str(gravacao["medico_id"]),
                "tipo": gravacao.get("tipo"),
                "procedimento": gravacao.get("procedimento"),
                "transcricao": gravacao.get("transcricao"),
                "sumarizacao": gravacao.get("sumarizacao"),
                "medico_info": {
                    "name": gravacao["medico_info"].get("name"),
                    "email": gravacao["medico_info"].get("email"),
                    "professional_id": gravacao["medico_info"].get("professional_id"),
                },
            }
            for gravacao in procedure.get("gravacoes", [])
        ],
    }


def procedure_helper(procedure) -> dict:
    return {
        "id": str(procedure["_id"]) if "_id" in procedure else None,
        "paciente_id": str(procedure["paciente_id"]),
        "gravacoes": [
            {
                "data_gravacao": format_date(gravacao["data_gravacao"]),
                "paciente_id": str(gravacao["paciente_id"]),
                "medico_id": str(gravacao["medico_id"]),
                "tipo": gravacao["tipo"],
                "procedimento": gravacao.get("procedimento"),
                "transcricao": gravacao.get("transcricao"),
                "sumarizacao": gravacao["sumarizacao"],
            }
            for gravacao in procedure.get("gravacoes", [])
        ],
        "resumo_inteligencia": procedure.get("resumo_inteligencia", {}),
    }


async def add_gravacao(gravacao_data: dict) -> dict:
    procedures_collection = await get_procedures_collection()
    paciente_id = gravacao_data["paciente_id"]

    gravacao_data["_id"] = ObjectId()

    existing_procedure = await procedures_collection.find_one(
        {"paciente_id": ObjectId(paciente_id)}
    )

    if existing_procedure:
        await procedures_collection.update_one(
            {"paciente_id": ObjectId(paciente_id)},
            {"$push": {"gravacoes": gravacao_data}},
        )
    else:
        new_procedure = {
            "paciente_id": ObjectId(paciente_id),
            "gravacoes": [gravacao_data],
            "resumo_inteligencia": None,
        }
        await procedures_collection.insert_one(new_procedure)

    updated_procedure = await procedures_collection.find_one(
        {"paciente_id": ObjectId(paciente_id)}
    )
    return procedure_helper(updated_procedure)


async def get_all_gravacoes_by_paciente_id(paciente_id: str) -> List[dict]:
    procedures_collection = await get_procedures_collection()
    procedure = await procedures_collection.find_one(
        {"paciente_id": ObjectId(paciente_id)}
    )
    if procedure:
        return procedure.get("gravacoes", [])
    return []


async def get_gravacoes_by_paciente_and_medico(
    paciente_id: str, medico_id: str
) -> List[dict]:
    procedures_collection = await get_procedures_collection()
    procedure = await procedures_collection.find_one(
        {"paciente_id": ObjectId(paciente_id)}
    )
    if procedure:
        gravacoes = procedure.get("gravacoes", [])
        filtered_gravacoes = [
            g for g in gravacoes if g.get("medico_id") == ObjectId(medico_id)
        ]
        return filtered_gravacoes
    return []


async def get_all_gravacoes() -> List[dict]:
    procedures_view = await get_procedures_view_collection()
    results = await procedures_view.find().to_list(length=None)
    serializable_results = [procedures_view_helper(procedure) for procedure in results]
    return serializable_results
