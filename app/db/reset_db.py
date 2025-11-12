from app.db.database import Base, engine

# Asegurar que los modelos están importados para que SQLAlchemy conozca los mapeos
from app.db import models as _models  # noqa: F401


def reset_db() -> None:
    """Droppea y recrea todas las tablas de la base de datos configurada."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_db()
    print("database reset ok")
