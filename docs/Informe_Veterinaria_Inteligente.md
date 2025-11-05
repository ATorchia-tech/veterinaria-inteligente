# Informe del Proyecto: Veterinaria Inteligente

Autor: ATorchia-tech (GitHub)
Fecha: 04/11/2025

---

## 1) Metodología

- Objetivo general: construir una API REST para gestión de una clínica veterinaria y un módulo de IA básico aplicable a casuísticas reales (afluencia, ausentismo, análisis de sentimiento e intención de consultas), priorizando simplicidad, trazabilidad y reproducibilidad.
- Enfoque: iterativo-incremental con validación continua mediante pruebas automáticas (pytest) y documentación viva (README y cuadernos/notebooks de análisis).
- Stack principal:
  - Backend: FastAPI (Uvicorn)
  - Persistencia: SQLite + SQLAlchemy 2.x; migraciones con Alembic
  - Validación y esquemas: Pydantic v2
  - IA/ML: scikit-learn, numpy, pandas, joblib
  - Herramientas: pytest, Black, Ruff, VS Code tasks, Dockerfile, GitHub Actions (CI)
- Prácticas adoptadas:
  - Timestamps timezone-aware en las entidades (UTC) 
  - Migraciones de BD con Alembic y tareas de VS Code para autogeneración/upgrade
  - Pruebas automatizadas de endpoints clave (agenda, vacunaciones, reportes, IA)
  - Modelos de IA persistidos en `app/ml/models/*.joblib`, con métricas guardadas y artefactos de evaluación

## 2) Historias de Usuario (resumen)

- Registro de Mascotas: como recepcionista, quiero registrar una nueva mascota asociada a un dueño para mantener su ficha clínica.
- Agenda de Turnos: como recepcionista/cliente, quiero agendar una cita con fecha y motivo, y poder cancelarla.
- Historial Clínico: como veterinario, quiero consultar y registrar atenciones (síntomas, diagnóstico, tratamiento, medicación) por mascota.
- Vacunación y Recordatorios: como recepcionista, quiero identificar y listar vacunas próximas a vencer para contactar a dueños.
- Reportes de Gestión: como veterinario, quiero ver asistencia/cancelaciones en un rango de fechas.
- IA (Predicción de Afluencia): como veterinario, quiero estimar la afluencia (Baja/Media/Alta) para planificar recursos.
- IA (Análisis de Sentimiento): como responsable de atención, quiero clasificar comentarios de clientes en positivo/negativo.
- IA (No-show/Ausentismo): como gestor, quiero estimar ausentismo probable para reprogramar o sobre-reservar prudentemente.
- IA (Clasificación de Intenciones): como operador, quiero clasificar consultas por intención (turnos, vacunación, precios, horarios, etc.) para dirigir la respuesta adecuada.

Las especificaciones más extensas en formato Gherkin están incluidas en el README del proyecto.

## 3) Diseño del Sistema

- Arquitectura general
  - FastAPI como capa de presentación con routers por dominio: owners, pets, appointments, records, schedule, vaccinations, reports, ai.
  - Capa de persistencia con SQLAlchemy y modelos ORM: Owner, Pet, Appointment, ClinicalRecord, Vaccination.
  - Esquemas Pydantic (v2) en `app/schemas/*` para contratos de entrada/salida; timestamps expuestos en lecturas.
  - Migraciones de esquema con Alembic; base de datos SQLite por defecto (`DB_URL` configurable por entorno).
  - Tareas de VS Code para ejecutar API, tests, format, lint, migraciones y entrenamiento de modelos IA.

- Flujo típico (texto):
  - Cliente (curl/Swagger UI) -> FastAPI -> Router del dominio -> Operaciones ORM (SQLAlchemy) -> SQLite
  - Para endpoints de IA: Router -> Módulo ML (carga modelo joblib) -> Predicción -> Respuesta (con probabilidades)

- Consideraciones transversales
  - Timestamps timezone-aware (UTC) en todas las entidades
  - Paginación en listados (`page`, `page_size`)
  - Semilla de datos (`app.db.seed`) para desarrollo rápido
  - Dockerfile para despliegue (ejecuta `alembic upgrade head` + `uvicorn`)
  - CI (GitHub Actions) con lint, format-check, migraciones y tests

## 4) Módulo de IA: ¿qué hace y cómo funciona?

El módulo de IA cubre cuatro casos prácticos, con datasets sintéticos o mínimos de ejemplo y modelos ligeros en scikit-learn.

### 4.1 Predicción de Afluencia (/ai/predict)
- ¿Qué hace? Devuelve una categoría de afluencia (Baja/Media/Alta) y probabilidad estimada para un día.
- ¿Cómo funciona? Un modelo de bosque aleatorio entrenado con características sintéticas (incluyendo “clima” de un stub). Si no hay modelo, aplica una regla simple de fallback. Entrenamiento en `app/ml/train.py`, predicción en `app/ml/predict.py`.

### 4.2 Análisis de Sentimiento (/ai/sentiment)
- ¿Qué hace? Clasifica texto en positivo/negativo y devuelve probabilidad.
- ¿Cómo funciona? Pipeline `CountVectorizer + LogisticRegression`, entrenado con ejemplos mínimos y persistido con joblib (`app/ml/sentiment.py`). Endpoint usa `predict_sentiment()`.

### 4.3 Predicción de Ausentismo (/ai/noshow)
- ¿Qué hace? Dada una fecha y hora, estima si habrá "no-show" (ausentismo) y la probabilidad asociada.
- ¿Cómo funciona? `LogisticRegression` con características sintéticas (día/hora + “clima” stub). Persistencia con joblib (`app/ml/noshow.py`) y reglas de fallback si no hay modelo.

### 4.4 Clasificación de Intenciones
- Baseline por palabras clave (/ai/classify):
  - ¿Qué hace? Detecta intención principal (turnos, vacunación, emergencia, precios, horarios, servicios, ubicación, contacto, otros) por coincidencia de palabras/expresiones en español.
  - ¿Cómo funciona? Normaliza acentos, busca patrones con regex, decide por conteo y prioridad, y estima una confianza simple (`app/ml/keywords.py`).
- Supervisado (/ai/intent):
  - ¿Qué hace? Clasifica intención y devuelve `label`, `probability` y `top3` clases más probables.
  - ¿Cómo funciona? Pipeline `TfidfVectorizer (preprocesado sin acentos) + LogisticRegression`. Dataset de ejemplo en `app/ml/data/intent_samples.csv`. Entrenamiento/guardado en `app/ml/intent.py`. 
  - Evaluación y trazabilidad:
    - Guarda métricas en `app/ml/models/intent_metrics.json`: accuracy, precision/recall/f1 (macro/micro/weighted), métricas por clase, labels, uso y cantidad de folds de validación cruzada (ajustados dinámicamente según el mínimo por clase), matriz de confusión.
    - Exporta la matriz de confusión como CSV (`intent_confusion_matrix.csv`) y un HTML rendered (`intent_confusion_matrix.html`) con colores.
    - Tareas de VS Code:
      - Train Intent Model: entrena y persiste modelo + métricas
      - Show Intent Metrics: imprime el JSON de métricas
      - Render/Open Confusion Matrix (HTML): genera y abre la matriz en el navegador
  - Fallback: si el modelo no existe, el endpoint usa el clasificador por palabras clave.

## 5) Diseño de datos (modelo simplificado)

- Owner(id, name, phone, email, created_at, updated_at)
- Pet(id, name, species, breed, birth_date, notes, owner_id, created_at, updated_at)
- Appointment(id, date, reason, status, pet_id, created_at, updated_at)
- ClinicalRecord(id, pet_id, symptoms, diagnosis, treatment, medications, created_at, updated_at)
- Vaccination(id, pet_id, vaccine_name, due_date, last_date, status, created_at, updated_at)

Relaciones principales:
- Owner 1..* Pet
- Pet 1..* Appointment, 1..* ClinicalRecord, 1..* Vaccination

## 6) Pruebas, Mantenibilidad y Entrega

- Pruebas (pytest):
  - Cobertura de escenarios de agenda diaria, vacunaciones próximas, reportes, creación/listado de récords clínicos, y endpoints de IA (sentiment, noshow, keywords, intent con entrenamiento previo y top-3).
  - Suite en `tests/` (19 tests en verde al cierre del desarrollo).
- Tareas de VS Code: facilitan ejecutar API, tests, lint/format, migraciones y tareas ML sin recordar comandos.
- CI/CD (opcional): workflow de GitHub Actions para lint, format-check, migraciones y tests en cada push.
- Entrega: repositorio público recomendado para revisión docente (link en GitHub).

## 7) Conclusiones y Próximos Pasos

- El proyecto implementa una API funcional para operaciones típicas de una clínica veterinaria y un conjunto de módulos de IA prácticos con modelos ligeros y trazables.
- Foco en reproducibilidad: scripts de entrenamiento, artefactos de métricas, matriz de confusión, tareas VS Code y documentación.
- Próximos pasos sugeridos:
  - Sustituir el stub de clima por un cliente real y enriquecer características con históricos.
  - Aumentar dataset de intenciones y etiquetado real; experimentar con embeddings.
  - Añadir autenticación/roles y auditoría.
  - Endpoints de reporting más elaborados y dashboards.

---

Para ejecutar y detalles de endpoints, ver el `README.md` en la raíz del proyecto.
