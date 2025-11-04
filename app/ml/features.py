def vectorize(features: dict) -> list[float]:
    return [
        float(features.get("temp_avg", 20.0)),
        float(features.get("precip_prob", 0.0)),
        float(features.get("is_weekend", 0)),
        float(features.get("month", 1)),
        float(features.get("weekday", 0)),
    ]
