from typing import List

from app.config.database import db


async def listar_medicos() -> List[dict]:
    medicos_collection = await db.get_collection("Medicos")
    medicos_cursor = medicos_collection.find()
    medicos = await medicos_cursor.to_list(None)
    return medicos
