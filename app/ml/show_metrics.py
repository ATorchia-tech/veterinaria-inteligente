from __future__ import annotations

import json
import os
from typing import Any

from .intent import METRICS_JSON_PATH


def main() -> None:
    path = METRICS_JSON_PATH
    if not os.path.exists(path):
        print(f"No se encontró el archivo de métricas: {path}\nEntrená primero el modelo con: python -m app.ml.intent")
        return

    with open(path, "r", encoding="utf-8") as f:
        data: Any = json.load(f)

    print(f"Archivo de métricas: {path}")
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
