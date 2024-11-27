from pydantic import BaseModel


class SummarizeRequest(BaseModel):
    patientId: str
    sumarizacoes: list[str]


class SummarizeResponse(BaseModel):
    text: str
