from typing import Any, Dict, List

from pydantic import BaseModel


class SummarizeRequest(BaseModel):
    patientId: str
    sumarizacoes: List[Dict[str, Any]]


class SummarizeResponse(BaseModel):
    text: str
