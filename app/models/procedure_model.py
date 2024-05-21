from datetime import date

from pydantic import BaseModel, Field


class ProcedureModel(BaseModel):
    procedure_type: str
    patient_name: str
    exact_procedure_name: str
    birthdate: date

    class Config:
        schema_extra = {
            "example": {
                "procedure_type": "Cirurgia",
                "patient_name": "João Silva",
                "exact_procedure_name": "Cirurgia de Apendicite",
                "birthdate": "1980-01-01",
            }
        }

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["birthdate"] = d["birthdate"].isoformat()  # Converte para string
        return d