# 🏥 Veterinaria Inteligente - IFTS-12

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](#-cómo-ejecutar-los-tests)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688)](https://fastapi.tiangolo.com/)
[![AI](https://img.shields.io/badge/IA-Machine%20Learning-purple)](#-módulo-de-inteligencia-artificial)

Sistema de gestión veterinaria con inteligencia artificial para análisis predictivo, clasificación de intenciones, análisis de sentimientos y predicción de inasistencias.

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación Rápida](#-instalación-rápida)
- [Cómo Ejecutar la Aplicación](#-cómo-ejecutar-la-aplicación)
- [Cómo Probar la Aplicación](#-cómo-probar-la-aplicación)
- [Módulo de Inteligencia Artificial](#-módulo-de-inteligencia-artificial)
- [Cómo Ejecutar los Tests](#-cómo-ejecutar-los-tests)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Endpoints Principales](#-endpoints-principales)
- [Compartir con el Profesor](#-compartir-con-el-profesor)
- [Documentación Adicional](#-documentación-adicional)

---

## 🎯 Descripción del Proyecto

**Veterinaria Inteligente** es un sistema completo de gestión para clínicas veterinarias que incluye:

- 👥 **Gestión de Clientes (Dueños):** Alta, baja, modificación y consulta
- 🐾 **Gestión de Mascotas:** Registro completo con historial médico
- 📅 **Sistema de Turnos:** Agendamiento con seguimiento de estados
- 🏥 **Registros Clínicos:** Historial médico detallado de cada consulta
- 💉 **Control de Vacunaciones:** Seguimiento y alertas de vencimientos
- 🤖 **Inteligencia Artificial:** 4 modelos de ML para análisis predictivo
- 📊 **Reportes y Estadísticas:** Análisis de datos y métricas

---

## ⚙️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10 o superior** → [Descargar Python](https://www.python.org/downloads/)
- **Git** (opcional, para clonar el repositorio) → [Descargar Git](https://git-scm.com/downloads)
- **Visual Studio Code** (recomendado) → [Descargar VS Code](https://code.visualstudio.com/)

---

## 🚀 Instalación Rápida

### Opción 1: Script Automático (Windows - Recomendado)

```powershell
# 1. Clonar el repositorio (si aún no lo tienes)
git clone https://github.com/ATorchia-tech/VETERINARIA-INTELIGENTE.git
cd veterinaria-inteligente

# 2. Ejecutar con doble clic en:
scripts/run_and_open.bat
```

Este script automáticamente:
- ✅ Crea el entorno virtual `.venv`
- ✅ Instala todas las dependencias
- ✅ Inicia la API en `http://127.0.0.1:8000`
- ✅ Abre tu navegador en la documentación

### Opción 2: Instalación Manual

```powershell
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Windows CMD:
.venv\Scripts\activate.bat

# 3. Actualizar pip
python -m pip install --upgrade pip

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Crear base de datos (primera vez)
python -m alembic upgrade head
```

---

## ▶️ Cómo Ejecutar la Aplicación

### Método 1: Usando Tareas de VS Code (Recomendado)

1. Abrir el proyecto en VS Code
2. Presionar `Ctrl+Shift+P` (o `Cmd+Shift+P` en Mac)
3. Escribir: `Tasks: Run Task`
4. Seleccionar: **"Run API"**

La API se iniciará en: **http://127.0.0.1:8000**

### Método 2: Línea de Comandos

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Iniciar la API con recarga automática
uvicorn app.main:app --reload
```

### Método 3: Script de Inicio

```powershell
# Inicia la API y abre el navegador
powershell -ExecutionPolicy Bypass -File .\scripts\run_and_open.ps1
```

---

## 🧪 Cómo Probar la Aplicación

Una vez que la API esté ejecutándose, puedes acceder a:

### 🌐 Interfaces Web Disponibles

| URL | Descripción |
|-----|-------------|
| **http://127.0.0.1:8000/** | 🏠 Página principal con acceso a todos los módulos |
| **http://127.0.0.1:8000/ui** | 👥 Panel de Recepción (gestión de clientes) |
| **http://127.0.0.1:8000/vet/** | 🩺 Panel Veterinario Principal |
| **http://127.0.0.1:8000/vet/clinica/** | 🏥 Módulo de Atención Clínica |
| **http://127.0.0.1:8000/vet/gestion/** | 📊 Módulo de Gestión Operativa |
| **http://127.0.0.1:8000/docs** | 📖 Documentación Técnica (Swagger UI) |
| **http://127.0.0.1:8000/admin/api_docs_friendly** | 📚 Documentación Amigable |

### 🎮 Flujo de Prueba Básico

#### 1. **Registrar un Dueño**
   - Ir a: http://127.0.0.1:8000/ui
   - Click en "➕ Registrar Nuevo Dueño"
   - Completar: Nombre, Teléfono, Email
   - Click en "Guardar"

#### 2. **Registrar una Mascota**
   - Click en "🐾 Ver/Buscar Mascotas"
   - Click en "➕ Registrar Nueva Mascota"
   - Seleccionar dueño, completar datos
   - Click en "Guardar"

#### 3. **Agendar un Turno**
   - Click en "📅 Ver Turnos"
   - Click en "➕ Nuevo Turno"
   - Seleccionar mascota, fecha y hora
   - Click en "Guardar"

#### 4. **Probar la IA**
   - Ir a: http://127.0.0.1:8000/vet/
   - En la sección "🤖 Análisis con IA"
   - Probar análisis de intención, sentimiento o predicción

---

## 🤖 Módulo de Inteligencia Artificial

El sistema incluye **4 modelos de Machine Learning** completamente funcionales:

### 📊 Modelos Disponibles

| Modelo | Función | Algoritmo |
|--------|---------|-----------|
| **Intent Classifier** | Clasifica intenciones en mensajes | Multinomial Naive Bayes |
| **Sentiment Analyzer** | Analiza sentimiento (positivo/negativo/neutral) | Logistic Regression |
| **No-Show Predictor** | Predice probabilidad de inasistencia | Random Forest |
| **Keyword Extractor** | Extrae palabras clave relevantes | TF-IDF |

### 🎓 Entrenar los Modelos de IA

#### Entrenar Modelo de Intenciones
```powershell
# Opción 1: VS Code Task
Ctrl+Shift+P > Tasks: Run Task > "Train Intent Model"

# Opción 2: Terminal
.\.venv\Scripts\Activate.ps1
python -m app.ml.intent
```

#### Entrenar Modelo de Sentimientos
```powershell
python -m app.ml.sentiment
```

#### Entrenar Modelo de Predicción de Inasistencias
```powershell
python -m app.ml.noshow
```

### 📈 Ver Métricas de los Modelos

```powershell
# Ver métricas del modelo de intenciones
python -m app.ml.show_metrics

# Generar matriz de confusión (HTML interactivo)
python -m app.ml.render_confusion_matrix

# Abrir matriz de confusión en navegador
Ctrl+Shift+P > Tasks: Run Task > "Open Confusion Matrix (HTML)"
```

### 🧠 Analizar Modelo de Intenciones (Jupyter Notebook)

```powershell
# Abrir notebook de análisis
jupyter notebook notebooks/intent_model_analysis.ipynb
```

El notebook incluye:
- ✅ Análisis exploratorio de datos
- ✅ Visualización de distribución de clases
- ✅ Matriz de confusión interactiva
- ✅ Métricas de rendimiento por clase
- ✅ Ejemplos de predicciones

### 🔬 Probar los Modelos de IA

#### Desde la Interfaz Web
- Ir a: **http://127.0.0.1:8000/vet/**
- Sección: **"🤖 Análisis con IA"**
- Probar cada modelo con ejemplos

#### Desde la API (Swagger)
- Ir a: **http://127.0.0.1:8000/docs**
- Sección: **"ai"**
- Probar endpoints:
  - `POST /ai/intent` - Clasificar intención
  - `POST /ai/sentiment` - Analizar sentimiento
  - `POST /ai/predict-noshow` - Predecir inasistencia
  - `POST /ai/keywords` - Extraer palabras clave

#### Ejemplo de Uso (Python)
```python
import requests

# Analizar intención de un mensaje
response = requests.post(
    "http://127.0.0.1:8000/ai/intent",
    json={"text": "Necesito un turno urgente para mi perro"}
)
print(response.json())
# Output: {"intent": "agendar_turno", "confidence": 0.89, ...}
```

---

## ✅ Cómo Ejecutar los Tests

### Opción 1: Script Automático (Recomendado)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_and_test.ps1
```

Este script:
- ✅ Verifica el entorno virtual
- ✅ Instala dependencias faltantes
- ✅ Ejecuta todos los tests con pytest
- ✅ Muestra resumen de resultados

### Opción 2: Usando Tareas de VS Code

```
Ctrl+Shift+P > Tasks: Run Task > "Tests"
```

### Opción 3: Manual

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar todos los tests
pytest -q

# Ejecutar tests con más detalle
pytest -v

# Ejecutar tests con cobertura
pytest --cov=app --cov-report=html
```

### 📊 Tests Incluidos

| Archivo | Descripción |
|---------|-------------|
| `test_health.py` | Tests de endpoints de salud |
| `test_ai_intent.py` | Tests del modelo de intenciones |
| `test_ai_sentiment.py` | Tests del modelo de sentimientos |
| `test_ai_noshow.py` | Tests del predictor de inasistencias |
| `test_ai_keywords.py` | Tests del extractor de palabras clave |
| `test_records.py` | Tests de registros clínicos |
| `test_reports.py` | Tests de reportes |
| `test_schedule.py` | Tests de agenda |
| `test_vaccinations.py` | Tests de vacunaciones |

---

## 📁 Estructura del Proyecto

```
veterinaria-inteligente/
├── 📁 app/                          # Código principal de la aplicación
│   ├── 📁 api/routers/              # Endpoints de la API
│   │   ├── health.py                # Endpoints de salud
│   │   ├── owners.py                # CRUD de dueños
│   │   ├── pets.py                  # CRUD de mascotas
│   │   ├── appointments.py          # CRUD de turnos
│   │   ├── records.py               # Registros clínicos
│   │   ├── vaccinations.py          # Control de vacunas
│   │   ├── ai.py                    # Endpoints de IA
│   │   ├── admin.py                 # Panel administrativo
│   │   ├── ui.py                    # Panel de recepción
│   │   ├── vet_ui.py                # Panel veterinario
│   │   ├── vet_clinica.py           # Módulo clínico
│   │   └── vet_gestion.py           # Módulo de gestión
│   ├── 📁 ml/                       # Módulo de Machine Learning
│   │   ├── intent.py                # Modelo de intenciones
│   │   ├── sentiment.py             # Modelo de sentimientos
│   │   ├── noshow.py                # Predictor de inasistencias
│   │   ├── keywords.py              # Extractor de palabras clave
│   │   ├── features.py              # Feature engineering
│   │   ├── 📁 models/               # Modelos entrenados (.joblib)
│   │   └── 📁 data/                 # Datos de entrenamiento
│   ├── 📁 db/                       # Base de datos
│   │   ├── models.py                # Modelos SQLAlchemy
│   │   ├── database.py              # Configuración DB
│   │   └── seed.py                  # Datos de prueba
│   ├── 📁 schemas/                  # Esquemas Pydantic
│   └── main.py                      # Punto de entrada FastAPI
├── 📁 tests/                        # Tests unitarios
├── 📁 scripts/                      # Scripts de automatización
├── 📁 docs/                         # Documentación
├── 📁 notebooks/                    # Jupyter notebooks
├── 📄 requirements.txt              # Dependencias Python
├── 📄 pyproject.toml                # Configuración del proyecto
├── 📄 alembic.ini                   # Configuración de migraciones
└── 📄 README.md                     # Este archivo
```

---

## 🌐 Endpoints Principales

### 👥 Gestión de Dueños
- `GET /owners/` - Listar todos los dueños
- `POST /owners/` - Crear nuevo dueño
- `GET /owners/{id}` - Ver detalles de un dueño
- `PUT /owners/{id}` - Actualizar dueño
- `DELETE /owners/{id}` - Eliminar dueño

### 🐾 Gestión de Mascotas
- `GET /pets/` - Listar todas las mascotas
- `POST /pets/` - Registrar nueva mascota
- `GET /pets/{id}` - Ver detalles de una mascota
- `GET /pets/{id}/clinical-history` - Ver historial médico
- `PUT /pets/{id}` - Actualizar mascota
- `DELETE /pets/{id}` - Eliminar mascota

### 📅 Gestión de Turnos
- `GET /appointments/` - Listar todos los turnos
- `POST /appointments/` - Agendar nuevo turno
- `GET /appointments/{id}` - Ver detalles de un turno
- `POST /appointments/{id}/cancel` - Cancelar turno

### 🏥 Registros Clínicos
- `GET /records/{pet_id}` - Ver historial clínico de una mascota
- `POST /records/` - Crear nuevo registro clínico

### 💉 Vacunaciones
- `GET /vaccinations/` - Listar todas las vacunas
- `POST /vaccinations/` - Registrar nueva vacuna
- `GET /vaccinations/alerts` - Ver alertas de vacunas próximas a vencer

### 🤖 Inteligencia Artificial
- `POST /ai/intent` - Clasificar intención de un mensaje
- `POST /ai/sentiment` - Analizar sentimiento de un texto
- `POST /ai/predict-noshow` - Predecir probabilidad de inasistencia
- `POST /ai/keywords` - Extraer palabras clave de un texto

### 📊 Reportes
- `GET /reports/attendance` - Reporte de asistencia
- `GET /admin/db_counts_form` - Totales del sistema
- `GET /admin/db_details` - Detalles de todos los datos

---

## 👨‍🏫 Compartir con el Profesor

### ⚠️ Importante
La URL `http://127.0.0.1:8000` **solo funciona en tu computadora**. Para que el profesor pueda ver el proyecto, tiene 3 opciones:

### Opción A: Ejecutar Localmente (Recomendado)

**Pasos para el profesor:**

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/ATorchia-tech/VETERINARIA-INTELIGENTE.git
   cd veterinaria-inteligente
   ```

2. **Ejecutar con un solo click**
   - Windows: Doble click en `scripts/run_and_open.bat`
   - PowerShell: `powershell -ExecutionPolicy Bypass -File .\scripts\run_and_open.ps1`

3. **Acceder a la aplicación**
   - Se abrirá automáticamente en el navegador
   - URL: http://127.0.0.1:8000

### Opción B: Usando Docker

```bash
# Construir imagen
docker build -t veterinaria-inteligente .

# Ejecutar contenedor
docker run --rm -p 8000:8000 veterinaria-inteligente
```

Luego acceder a: http://127.0.0.1:8000

### Opción C: Desplegar en la Nube (URL Pública)

Servicios recomendados:
- **Render** (gratuito): https://render.com
- **Railway** (gratuito): https://railway.app
- **Fly.io** (gratuito): https://fly.io

El proyecto incluye `Dockerfile`, facilitando el despliegue.

---

## 📚 Documentación Adicional

- 📄 **Informe Completo:** `docs/Informe_Veterinaria_Inteligente.md`
- 📖 **Documentación Amigable:** http://127.0.0.1:8000/admin/api_docs_friendly
- 🔧 **Documentación Técnica:** http://127.0.0.1:8000/docs
- 📊 **Presentación del Proyecto:** http://127.0.0.1:8000/presentation (próximamente)

---

## 🛠️ Comandos Útiles

### Gestión de Base de Datos

```powershell
# Crear migración automática
.\.venv\Scripts\alembic.exe revision --autogenerate -m "descripción"

# Aplicar migraciones
.\.venv\Scripts\alembic.exe upgrade head

# Resetear y sembrar base de datos
python -m app.db.reset_db
python -m app.db.seed

# Ver contadores de datos
python -m app.db.counts
```

### Formateo y Linting

```powershell
# Formatear código con Black
python -m black app tests

# Verificar con Ruff
python -m ruff check .
```

### Tareas Disponibles en VS Code

- ✅ **Run API** - Inicia la aplicación
- ✅ **Tests** - Ejecuta todos los tests
- ✅ **Format (black)** - Formatea el código
- ✅ **Lint (ruff)** - Verifica el código
- ✅ **Train Intent Model** - Entrena modelo de intenciones
- ✅ **Train Sentiment Model** - Entrena modelo de sentimientos
- ✅ **Train No-Show Model** - Entrena predictor de inasistencias
- ✅ **Show Intent Metrics** - Muestra métricas del modelo
- ✅ **Render Confusion Matrix** - Genera matriz de confusión
- ✅ **Reset DB + Seed + Run** - Reinicia DB y ejecuta

---

## 📞 Soporte

Si encuentras algún problema:

1. Verificar que Python 3.10+ esté instalado: `python --version`
2. Verificar que las dependencias estén instaladas: `pip list`
3. Revisar logs en la terminal donde se ejecuta la API
4. Consultar documentación en: http://127.0.0.1:8000/docs

---

## 📝 Licencia

Este es un proyecto educativo desarrollado para el **IFTS-12**.

---

**Desarrollado con ❤️ para la materia de Desarrollo de Software - IFTS-12**
