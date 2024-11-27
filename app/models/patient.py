from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class EnderecoSchema(BaseModel):
    street: str
    city: str
    state: str
    cep: str
    number: str


class PatientSchema(BaseModel):
    name: str
    birth_date: str
    gender: str
    cpf: str
    contact: str
    address: EnderecoSchema
    register_date: Optional[datetime] = datetime.now()

    class Config:
        from_attributes = True


class UpdatePatientSchema(BaseModel):
    name: Optional[str]
    birth_date: Optional[str]
    gender: Optional[str]
    cpf: Optional[str]
    contact: Optional[str]
    address: Optional[EnderecoSchema]

    class Config:
        from_attributes = True
