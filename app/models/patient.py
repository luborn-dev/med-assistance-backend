from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class EnderecoSchema(BaseModel):
    rua: str
    cidade: str
    estado: str
    cep: str


class PatientSchema(BaseModel):
    nome: str
    data_nascimento: date
    genero: str
    cpf: str
    endereco: EnderecoSchema
    data_registro: Optional[datetime] = datetime.now()
    historico_medico: List[str] = []

    class Config:
        orm_mode = True


class UpdatePatientSchema(BaseModel):
    nome: Optional[str]
    data_nascimento: Optional[date]
    genero: Optional[str]
    cpf: Optional[str]
    endereco: Optional[EnderecoSchema]
    contato: Optional[ContatoSchema]
    historico_medico: Optional[List[str]]

    class Config:
        orm_mode = True
