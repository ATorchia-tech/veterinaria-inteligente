# Veterinaria Inteligente

Proyecto inicial que provee una API con FastAPI, persistencia SQLite con SQLAlchemy, endpoints para propietarios, mascotas, turnos, registros médicos, vacunas, reportes y un módulo de ML simple para predecir afluencia.

Requisitos mínimos
- Python 3.10+
- Crear entorno virtual: python -m venv .venv
- Instalar dependencias: pip install -r requirements.txt o usar pyproject.toml

Cómo ejecutar
1. Copiar `.env.example` a `.env` y adaptar variables (DB_URL, WEATHER_API_KEY).
2. Crear entorno virtual e instalar dependencias.
3. Ejecutar migraciones (si aplica) o dejar que la app cree tablas al iniciar.
4. Ejecutar la API rápidamente:

    - Doble clic en `scripts/run_and_open.bat` (abre el navegador en /docs y arranca la API si no está corriendo)
    - o en VS Code: Terminal > Run Task > "Run API + Open Docs (one-shot)"
    - o manual: `uvicorn app.main:app --reload`

Endpoints principales (v1)
- GET /health
- /owners -> CRUD propietarios
- /pets -> CRUD mascotas
- /appointments -> CRUD turnos
- /records -> CRUD registros médicos
- /schedule?date=YYYY-MM-DD -> agenda diaria (usa WeatherClient placeholder)
- /vaccinations/reminders -> recordatorios de vacunas
- /reports/attendance -> reporte de asistencia (simulado)
- /ai/predict -> forecast de afluencia (usa modelo ML)

Entrenar modelo ML (ejemplo)
1. Ejecutar: python -m app.ml.train
2. El modelo entrenado se guarda en `app/ml/models/`

Tests
- Ejecutar: pytest -q
# Veterinaria Inteligente

Proyecto FastAPI con SQLite/SQLAlchemy, Pydantic v2 y módulos de IA (afluencia, sentimiento, no-show, intención). Incluye tests (pytest), migraciones (Alembic), tareas de VS Code y un notebook de análisis.

- Informe para presentar: ver `docs/Informe_Veterinaria_Inteligente.md`.
- Tareas de VS Code disponibles en `.vscode/tasks.json` (run API, tests, lint/format, migraciones, entrenar modelos IA).

## Compartir el proyecto con otra persona (profesor/a)

Importante: la URL `http://127.0.0.1:8000/ui` funciona solo en la computadora donde se está ejecutando la API. Si le envías ese enlace a otra persona, no le abrirá nada a menos que ejecute la API en su propia máquina (o que despliegues el servicio en Internet con una URL pública).

### Opción A — Que lo ejecute localmente (Windows)
1. Clonar el repositorio público de GitHub.
2. Doble clic en `scripts/run_and_open.bat`.
    - El script creará automáticamente un entorno `.venv`, instalará dependencias y levantará la API si no existe aún.
    - Abrirá el navegador en `http://127.0.0.1:8000/docs` y también podés usar `http://127.0.0.1:8000/ui` (UI mínima con formularios).

Alternativa PowerShell (manual):

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_and_open.ps1
# o forzar instalación del entorno si fuera necesario:
powershell -ExecutionPolicy Bypass -File .\scripts\run_and_open.ps1 -Setup
```

Requisitos mínimos: tener instalado Python 3.10+ y permisos para ejecutar scripts de PowerShell (el `.bat` ya usa `-ExecutionPolicy Bypass`).

### Opción B — Docker (URL local en su equipo)
Con Docker instalado, puede ejecutar la API sin instalar Python:

```bash
docker build -t veterinaria-inteligente .
docker run --rm -p 8000:8000 veterinaria-inteligente
```

Luego abrir `http://127.0.0.1:8000/ui` o `http://127.0.0.1:8000/docs` en su navegador.

### Opción C — URL pública (despliegue)
Si querés que tu profesor acceda sin instalar nada, desplegá la app:
- Render, Railway, Fly.io, Azure App Service, etc. (este repo trae `Dockerfile`, lo que simplifica el deploy).
- Una vez desplegada, compartí la URL pública (por ejemplo, `https://tuapp.onrender.com/ui`).

## Publicar el repo en GitHub

Podés usar el script `scripts/publish_to_github.ps1` (requiere variable `GITHUB_TOKEN` con un token de acceso personal con permiso `repo`). Ejemplo:

```powershell
$env:GITHUB_TOKEN = 'ghp_xxx'  # tu token
powershell -ExecutionPolicy Bypass -File .\scripts\publish_to_github.ps1 -GithubUser TU_USUARIO -RepoName VETERINARIA-INTELIGENTE -Visibility public
```

Esto crea (si es necesario) el repo y hace push de la rama `main`.

