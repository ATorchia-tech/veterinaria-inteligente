from __future__ import annotations

import re
import unicodedata
from typing import Dict, List, Tuple


def _normalize(text: str) -> str:
    # lower + remove accents
    text = text.lower()
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


# Categories and indicative Spanish keywords (simple baseline)
KEYWORDS: Dict[str, List[str]] = {
    "turnos": [
        "turno",
        "cita",
        "agendar",
        "reservar",
        "disponibilidad",
        "horario",
        "cancelar",
        "reprogramar",
    ],
    "vacunacion": [
        "vacuna",
        "vacunacion",
        "refuerzo",
        "antirrabica",
        "rabia",
        "triple",
        "quintuple",
    ],
    "emergencia": [
        "emergencia",
        "urgente",
        "sangrando",
        "convulsion",
        "accidente",
        "envenenado",
        "no respira",
    ],
    "precios": [
        "precio",
        "costo",
        "cuanto sale",
        "cuanto cuesta",
        "arancel",
        "tarifa",
        "presupuesto",
    ],
    "horarios": [
        "horario",
        "abren",
        "cierran",
        "atencion",
        "domingos",
        "feriados",
    ],
    "ubicacion": [
        "direccion",
        "ubicacion",
        "como llegar",
        "mapa",
        "estacionamiento",
    ],
    "contacto": [
        "telefono",
        "whatsapp",
        "mail",
        "correo",
        "contacto",
    ],
    "servicios": [
        "banio",
        "bano",
        "peluqueria",
        "castracion",
        "cirugia",
        "radiografia",
        "analisis",
        "desparasitacion",
    ],
}


_PHRASE_PATTERNS: Dict[str, List[re.Pattern]] = {
    cat: [re.compile(r"\b" + re.escape(_normalize(kw)) + r"\b") for kw in kws]
    for cat, kws in KEYWORDS.items()
}


def classify_text(text: str) -> Tuple[str, List[str], float]:
    """
    Classify a client message into one category using simple keyword matching.
    Returns (label, matched_keywords, confidence [0..1]).
    """
    norm = _normalize(text)
    matches_by_cat: Dict[str, List[str]] = {cat: [] for cat in KEYWORDS}

    for cat, patterns in _PHRASE_PATTERNS.items():
        for kw, pattern in zip(KEYWORDS[cat], patterns):
            if pattern.search(norm):
                matches_by_cat[cat].append(kw)

    # Choose the category with most matches; tie-break by a fixed priority order
    priority = [
        "emergencia",
        "turnos",
        "vacunacion",
        "precios",
        "horarios",
        "servicios",
        "ubicacion",
        "contacto",
    ]

    best_label = "otros"
    best_matches: List[str] = []
    best_count = 0
    for cat in priority:
        cnt = len(matches_by_cat[cat])
        if cnt > best_count:
            best_label = cat
            best_matches = matches_by_cat[cat]
            best_count = cnt

    # Simple confidence heuristic: number of matches capped
    confidence = min(1.0, best_count / 3.0) if best_count > 0 else 0.2
    return best_label, best_matches, float(confidence)


if __name__ == "__main__":
    examples = [
        "Quiero agendar un turno para mañana",
        "Necesito el refuerzo de la vacuna antirrábica",
        "Es una emergencia, está sangrando",
        "¿Cuál es el precio de la castración?",
        "¿Qué horarios tienen los domingos?",
    ]
    for t in examples:
        print(t, "->", classify_text(t))
