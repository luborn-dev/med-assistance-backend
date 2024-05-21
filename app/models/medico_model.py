from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ContactInfo(BaseModel):
    phone: str
    email: str


class ProfessionalInfo(BaseModel):
    specialization: str
    crm: str


class WorkInfo(BaseModel):
    hospital: str
    address: str


class ScheduleItem(BaseModel):
    day: str
    start_time: str
    end_time: str


class Medico(BaseModel):
    doctor_id: str
    personal_info: dict = Field(
        ...,
        example={
            "name": "Dr. Ricardo Mendes",
            "date_of_birth": "1975-04-12",
            "contact_info": {
                "phone": "(11) 92345-6789",
                "email": "ricardo.mendes@example.com",
            },
            "professional_info": {"specialization": "Cardiologia", "crm": "SP-123456"},
        },
    )
    work_info: WorkInfo
    schedule: List[ScheduleItem]
