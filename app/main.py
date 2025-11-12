from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine

# Importar modelos antes de crear las tablas para que SQLAlchemy conozca los mapeos
from app.db import models as _models  # noqa: F401
from app.api.routers.admin import router as admin_router
from app.api.routers.health import router as health_router
from app.api.routers.owners import router as owners_router
from app.api.routers.pets import router as pets_router
from app.api.routers.appointments import router as appointments_router
from app.api.routers.records import router as records_router
from app.api.routers.schedule import router as schedule_router
from app.api.routers.vaccinations import router as vaccinations_router
from app.api.routers.reports import router as reports_router
from app.api.routers.ai import router as ai_router
from app.api.routers.ui import router as ui_router
from app.api.routers.vet_ui import router as vet_ui_router
from app.api.routers.vet_clinica import router as vet_clinica_router
from app.api.routers.vet_gestion import router as vet_gestion_router
from app.api.routers.home import router as home_router
from app.api.routers.ai_dashboard import router as ai_dashboard_router


def create_app() -> FastAPI:
    app = FastAPI(title="Veterinaria Inteligente", version="0.1.0")

    # CORS básico (ajusta en producción)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Crear tablas (desarrollo)
    Base.metadata.create_all(bind=engine)

    # Routers
    app.include_router(home_router, tags=["home"], include_in_schema=False)
    app.include_router(health_router)
    app.include_router(admin_router, tags=["admin"])
    app.include_router(owners_router, prefix="/owners", tags=["owners"])
    app.include_router(pets_router, prefix="/pets", tags=["pets"])
    app.include_router(
        appointments_router, prefix="/appointments", tags=["appointments"]
    )
    app.include_router(records_router, prefix="/records", tags=["records"])
    app.include_router(schedule_router, prefix="/schedule", tags=["schedule"])
    app.include_router(
        vaccinations_router, prefix="/vaccinations", tags=["vaccinations"]
    )
    app.include_router(reports_router, prefix="/reports", tags=["reports"])
    app.include_router(ai_router, prefix="/ai", tags=["ai"])
    app.include_router(
        ai_dashboard_router,
        prefix="/ai-dashboard",
        tags=["ai-dashboard"],
        include_in_schema=False,
    )
    app.include_router(ui_router, prefix="/ui", tags=["ui"], include_in_schema=False)
    app.include_router(
        vet_ui_router, prefix="/vet", tags=["vet-ui"], include_in_schema=False
    )
    app.include_router(
        vet_clinica_router,
        prefix="/vet/clinica",
        tags=["vet-clinica"],
        include_in_schema=False,
    )
    app.include_router(
        vet_gestion_router,
        prefix="/vet/gestion",
        tags=["vet-gestion"],
        include_in_schema=False,
    )

    return app


app = create_app()
