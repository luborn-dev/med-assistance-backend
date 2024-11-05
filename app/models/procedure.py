from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class GravacaoSchema(BaseModel):
    data_gravacao: datetime
    tipo: str
    transcricao: str


class ResumoInteligenciaSchema(BaseModel):
    descricao_geral: str
    condicoes_cronicas: List[str]
    medicamentos_em_uso: List[str]
    alertas: List[str]


class ProcedureSchema(BaseModel):
    paciente_id: PyObjectId
    medico_id: PyObjectId
    data_atendimento: datetime
    gravacoes: List[GravacaoSchema]
    resumo_inteligencia: Optional[ResumoInteligenciaSchema] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateProcedureSchema(BaseModel):
    gravacoes: Optional[List[GravacaoSchema]]
    resumo_inteligencia: Optional[ResumoInteligenciaSchema]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
