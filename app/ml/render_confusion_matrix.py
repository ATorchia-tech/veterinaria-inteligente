from __future__ import annotations

import os
from typing import List

from .intent import METRICS_JSON_PATH, MODEL_DIR
import json


def _color_scale(value: float) -> str:
    """
    Mapea un valor 0..1 a un color azul (claro->oscuro) en formato hex.
    """
    # Interpolar entre #f7fbff (247,251,255) y #08306b (8,48,107)
    a = (247, 251, 255)
    b = (8, 48, 107)
    r = int(a[0] + (b[0] - a[0]) * value)
    g = int(a[1] + (b[1] - a[1]) * value)
    c = int(a[2] + (b[2] - a[2]) * value)
    return f"#{r:02x}{g:02x}{c:02x}"


def main() -> None:
    if not os.path.exists(METRICS_JSON_PATH):
        print(
            f"No se encontró {METRICS_JSON_PATH}. Entrená el modelo primero: python -m app.ml.intent"
        )
        return

    with open(METRICS_JSON_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    labels: List[str] = metrics.get("labels", [])
    cm: List[List[int]] = metrics.get("confusion_matrix_cv", [])
    if not labels or not cm:
        print("No hay datos de matriz de confusión en las métricas.")
        return

    max_val = max(max(row) for row in cm) if cm else 1
    max_val = max(1, max_val)

    rows_html = []
    # Header row
    header_cells = "".join(f"<th>{lbl}</th>" for lbl in labels)
    rows_html.append(f"<tr><th></th>{header_cells}</tr>")

    # Data rows
    for i, row in enumerate(cm):
        cells = []
        for val in row:
            frac = (val / max_val) if max_val else 0.0
            color = _color_scale(frac)
            cells.append(f"<td style=\"background:{color}; text-align:center;\">{val}</td>")
        rows_html.append(f"<tr><th>{labels[i]}</th>{''.join(cells)}</tr>")

    html = f"""
<!doctype html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <title>Matriz de Confusión - Intenciones</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    table {{ border-collapse: collapse; }}
    th, td {{ border: 1px solid #ddd; padding: 6px 10px; }}
    th {{ background: #f0f0f0; }}
    caption {{ caption-side: top; font-weight: bold; margin-bottom: 10px; }}
  </style>
  </head>
<body>
  <h1>Matriz de Confusión - Clasificador de Intenciones</h1>
  <p>Etiquetas: {', '.join(labels)}</p>
  <table>
    <caption>Filas = reales, Columnas = predichas</caption>
    {''.join(rows_html)}
  </table>
  <p>Fuente: {METRICS_JSON_PATH}</p>
</body>
</html>
"""

    out_path = os.path.join(MODEL_DIR, "intent_confusion_matrix.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML generado: {out_path}")


if __name__ == "__main__":
    main()
