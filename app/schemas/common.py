from datetime import date
from pydantic import BaseModel


class AffluencePrediction(BaseModel):
    date: date
    label: str  # Baja, Media, Alta
    probability: float


class NoShowPrediction(BaseModel):
    date: date
    hour: int
    label: str  # no-show | show
    probability: float  # probability of no-show
