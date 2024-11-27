from typing import Any, Dict, List

from pydantic import BaseModel


class ContentItem(BaseModel):
    id: str
    question: str
    answer: str


class Content(BaseModel):
    id: str
    content_type: str
    content: List[Dict[str, Any]]
