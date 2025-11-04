from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.api.routers.health import router as health_router
from app.api.routers.owners import router as owners_router
from app.api.routers.pets import router as pets_router
from app.api.routers.appointments import router as appointments_router
from app.api.routers.records import router as records_router
from app.api.routers.schedule import router as schedule_router
from app.api.routers.vaccinations import router as vaccinations_router
from app.api.routers.reports import router as reports_router
from app.api.routers.ai import router as ai_router


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
    app.include_router(health_router)
    app.include_router(owners_router, prefix="/owners", tags=["owners"])
    app.include_router(pets_router, prefix="/pets", tags=["pets"])
    app.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
    app.include_router(records_router, prefix="/records", tags=["records"])
    app.include_router(schedule_router, prefix="/schedule", tags=["schedule"])
    app.include_router(vaccinations_router, prefix="/vaccinations", tags=["vaccinations"])
    app.include_router(reports_router, prefix="/reports", tags=["reports"])
    app.include_router(ai_router, prefix="/ai", tags=["ai"]) 

    return app


app = create_app()
