from datetime import date

from pydantic import BaseModel, Field


class PatientModel(BaseModel):
    name: str = Field(..., example="João Silva")
    birthdate: date = Field(..., example="1985-12-25")
    address: str = Field(..., example="Rua das Flores, 123")
    cpf: str = Field(..., example="123.456.789-00")
    phone: str = Field(..., example="(12) 34567-8901")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "João Silva",
                "birthdate": "1985-12-25",
                "address": "Rua das Flores, 123",
                "cpf": "123.456.789-00",
                "phone": "(12) 34567-8901",
            }
        }
