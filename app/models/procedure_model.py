from pydantic import BaseModel


class ProcedureModel(BaseModel):
    procedure_type: str
    patient_name: str
    exact_procedure_name: str
    doctor_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "procedure_type": "Cirurgia",
                "patient_name": "João Silva",
                "exact_procedure_name": "Cirurgia de Apendicite",
                "doctor_id": "29329392929",
            }
        }
