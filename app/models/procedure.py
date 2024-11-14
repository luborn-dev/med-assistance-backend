from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.custom_object_id import PyObjectId


class GravacaoSchema(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    data_gravacao: datetime = Field(default_factory=datetime.utcnow)
    paciente_id: ObjectId
    medico_id: ObjectId
    tipo: str
    procedimento: str
    transcricao: Optional[str] = None
    sumarizacao: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}


class ResumoInteligenciaSchema(BaseModel):
    paciente_id: PyObjectId = Field(...)
    descricao_geral: str
    condicoes_cronicas: List[str]
    medicamentos_em_uso: List[str]
    alertas: List[str]

    class Config:
        json_encoders = {ObjectId: str}


class ProcedureSchema(BaseModel):
    gravacoes: List[GravacaoSchema]
    resumo_inteligencia: Optional[ResumoInteligenciaSchema] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UpdateProcedureSchema(BaseModel):
    gravacoes: Optional[List[GravacaoSchema]]
    resumo_inteligencia: Optional[ResumoInteligenciaSchema]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
