from datetime import date
from fastapi import APIRouter

from app.ml.predict import predict_affluence
from app.external.weather_client import (
    get_weather_features,
    get_weather_forecast_buenos_aires,
)
from app.schemas.common import AffluencePrediction, NoShowPrediction
from app.schemas.sentiment import SentimentRequest, SentimentResponse
from app.schemas.nlp import MessageRequest, ClassificationResponse
from app.schemas.intent import IntentRequest, IntentResponse
from app.ml.sentiment import predict_sentiment
from app.ml.noshow import predict_noshow
from app.ml.keywords import classify_text
from app.ml.intent import predict_intent, predict_intent_topk

router = APIRouter()


@router.get("/forecast")
def get_forecast(days: int = 5):
    """
    Obtiene el pronóstico del tiempo de Buenos Aires para los próximos días.
    """
    forecast = get_weather_forecast_buenos_aires(days)
    return {
        "location": "Buenos Aires, Argentina",
        "forecast": [
            {
                "date": str(day["date"]),
                "temp_max": round(day["temp_max"], 1),
                "temp_min": round(day["temp_min"], 1),
                "temp_avg": round(day["temp_avg"], 1),
                "precipitation_probability": round(day["precipitation_probability"], 1),
                "precipitation_sum": round(day["precipitation_sum"], 1),
                "windspeed_max": round(day["windspeed_max"], 1),
                "humidity": round(day["humidity"], 1),
            }
            for day in forecast
        ],
    }


@router.get("/predict", response_model=AffluencePrediction)
def predict(day: date | None = None):
    # Obtener features de clima (stub) + fecha
    f = get_weather_features(day)
    label, prob = predict_affluence(f)
    return AffluencePrediction(date=f["date"], label=label, probability=prob)


@router.post("/sentiment", response_model=SentimentResponse)
def sentiment(body: SentimentRequest):
    label, prob = predict_sentiment(body.text)
    return SentimentResponse(label=label, probability=prob)


@router.get("/noshow", response_model=NoShowPrediction)
def no_show(day: date, hour: int):
    label, prob = predict_noshow(day, hour)
    return NoShowPrediction(date=day, hour=hour, label=label, probability=prob)


@router.post("/classify", response_model=ClassificationResponse)
def classify(body: MessageRequest):
    label, kws, conf = classify_text(body.text)
    return ClassificationResponse(label=label, keywords=kws, confidence=conf)


@router.post("/intent", response_model=IntentResponse)
def intent(body: IntentRequest):
    # Intento con modelo supervisado; si no existe, fallback a keywords
    try:
        label, prob = predict_intent(body.text)
        # top-3 para transparencia
        top = predict_intent_topk(body.text, k=3)
        return IntentResponse(
            label=label,
            probability=prob,
            top3=[{"label": lbl, "probability": prob_} for lbl, prob_ in top],
        )
    except FileNotFoundError:
        label, _kws, conf = classify_text(body.text)
        # map confidence ~ probability
        return IntentResponse(label=label, probability=float(conf), top3=None)
