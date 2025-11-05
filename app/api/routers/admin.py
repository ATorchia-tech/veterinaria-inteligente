from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import Base, engine, get_db

router = APIRouter()


@router.post("/__admin/reset-db")
def reset_db(db: Session = Depends(get_db)):
    try:
        # Cerrar conexiones de la sesión actual
        db.close()
    except Exception:
        pass
    # Dropear y recrear tablas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"status": "ok", "message": "database reset"}
