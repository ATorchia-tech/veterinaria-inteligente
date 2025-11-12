from datetime import date, datetime, timedelta
import requests
from typing import Dict, List


def get_weather_forecast_buenos_aires(days: int = 5) -> List[Dict]:
    """
    Obtiene el pronóstico del tiempo de Buenos Aires desde Open-Meteo API.
    
    Args:
        days: Cantidad de días de pronóstico (máximo 16)
    
    Returns:
        Lista de diccionarios con datos del clima por día
    """
    # Coordenadas de Buenos Aires, Argentina
    BUENOS_AIRES_LAT = -34.6037
    BUENOS_AIRES_LON = -58.3816
    
    try:
        # API gratuita de Open-Meteo (no requiere API key)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": BUENOS_AIRES_LAT,
            "longitude": BUENOS_AIRES_LON,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "precipitation_sum",
                "windspeed_10m_max",
                "relative_humidity_2m_mean",
            ],
            "timezone": "America/Argentina/Buenos_Aires",
            "forecast_days": min(days, 16),
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Procesar los datos diarios
        daily_data = data.get("daily", {})
        dates = daily_data.get("time", [])
        
        forecast = []
        for i in range(len(dates)):
            temp_max = daily_data.get("temperature_2m_max", [])[i]
            temp_min = daily_data.get("temperature_2m_min", [])[i]
            temp_avg = (temp_max + temp_min) / 2 if temp_max and temp_min else 20.0
            
            forecast.append({
                "date": datetime.strptime(dates[i], "%Y-%m-%d").date(),
                "temp_max": temp_max or 25.0,
                "temp_min": temp_min or 15.0,
                "temp_avg": temp_avg,
                "precipitation_probability": daily_data.get("precipitation_probability_max", [])[i] or 0.0,
                "precipitation_sum": daily_data.get("precipitation_sum", [])[i] or 0.0,
                "windspeed_max": daily_data.get("windspeed_10m_max", [])[i] or 0.0,
                "humidity": daily_data.get("relative_humidity_2m_mean", [])[i] or 65.0,
            })
        
        return forecast
        
    except Exception as e:
        # Si falla la API, devolver datos simulados realistas
        print(f"Error obteniendo datos del clima: {e}")
        return _get_simulated_forecast(days)


def _get_simulated_forecast(days: int = 5) -> List[Dict]:
    """
    Genera datos simulados realistas para Buenos Aires cuando la API no está disponible.
    """
    import random
    
    forecast = []
    base_date = date.today()
    
    # Temperaturas típicas de Buenos Aires en noviembre (primavera)
    for i in range(days):
        day = base_date + timedelta(days=i)
        temp_avg = random.uniform(18, 26)
        
        forecast.append({
            "date": day,
            "temp_max": temp_avg + random.uniform(2, 5),
            "temp_min": temp_avg - random.uniform(2, 5),
            "temp_avg": temp_avg,
            "precipitation_probability": random.uniform(10, 50),
            "precipitation_sum": random.uniform(0, 10),
            "windspeed_max": random.uniform(10, 25),
            "humidity": random.uniform(50, 80),
        })
    
    return forecast


def get_weather_features(day: date | None = None) -> dict:
    """
    Obtiene features del clima para un día específico.
    Si no se especifica día, usa el día actual.
    """
    d = day or date.today()
    
    # Obtener pronóstico de 7 días
    forecast = get_weather_forecast_buenos_aires(7)
    
    # Buscar el día específico en el pronóstico
    weather_data = None
    for daily in forecast:
        if daily["date"] == d:
            weather_data = daily
            break
    
    # Si no se encuentra el día, usar el primer día del pronóstico
    if not weather_data and forecast:
        weather_data = forecast[0]
    
    # Si aún no hay datos, usar valores por defecto
    if not weather_data:
        weather_data = {
            "temp_avg": 20.0,
            "precipitation_probability": 20.0,
        }
    
    return {
        "date": d,
        "temp_avg": weather_data.get("temp_avg", 20.0),
        "precip_prob": weather_data.get("precipitation_probability", 20.0) / 100.0,
        "is_weekend": 1 if d.weekday() >= 5 else 0,
        "month": d.month,
        "weekday": d.weekday(),
    }
