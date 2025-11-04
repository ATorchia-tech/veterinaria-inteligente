from pydantic import BaseModel
from typing import List


class IntentRequest(BaseModel):
    text: str


class IntentResponse(BaseModel):
    label: str
    probability: float
    top3: List[dict] | None = None
