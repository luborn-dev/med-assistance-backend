from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ContactInfo(BaseModel):
    phone: str
    email: str
    address: str


class PersonalInfo(BaseModel):
    name: str
    date_of_birth: datetime
    contact_info: ContactInfo


class MedicalRecord(BaseModel):
    record_id: str
    date: datetime
    type: str
    observations: str


class Paciente(BaseModel):
    patient_id: str
    personal_info: PersonalInfo
    medical_records: List[MedicalRecord]
