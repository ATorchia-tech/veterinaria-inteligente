from datetime import date, datetime


def get_weather_features(day: date | None = None) -> dict:
    """
    Stub de cliente de clima: devuelve features mínimas para la fecha pedida.
    En producción, aquí deberías llamar a una API (ej. Open-Meteo) y mapear a features.
    """
    d = day or date.today()
    # Valores fijos de ejemplo; sustituir por llamada real si se desea.
    return {
        "date": d,
        "temp_avg": 20.0,
        "precip_prob": 0.2,
        "is_weekend": 1 if d.weekday() >= 5 else 0,
        "month": d.month,
        "weekday": d.weekday(),
    }
