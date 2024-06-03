from datetime import date

from pydantic import BaseModel, Field


class ProcedureModel(BaseModel):
    procedure_type: str
    patient_name: str
    exact_procedure_name: str
    birthdate: date

    class Config:
        json_schema_extra = {
            "example": {
                "procedure_type": "Cirurgia",
                "patient_name": "João Silva",
                "exact_procedure_name": "Cirurgia de Apendicite",
            }
        }

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["birthdate"] = d["birthdate"].format()  # Converte para string
        return d
