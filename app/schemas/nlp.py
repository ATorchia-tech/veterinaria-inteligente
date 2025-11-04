from pydantic import BaseModel
from typing import List


class MessageRequest(BaseModel):
    text: str


class ClassificationResponse(BaseModel):
    label: str
    keywords: List[str]
    confidence: float
