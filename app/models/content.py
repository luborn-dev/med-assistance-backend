from typing import Optional

from pydantic import BaseModel


class Content(BaseModel):
    id: Optional[str] = None
    question: str
    answer: str
    content_type: str
