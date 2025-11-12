from app.db.database import SessionLocal, Base, engine
from app.db import models


def main() -> None:
    Base.metadata.create_all(bind=engine)
    s = SessionLocal()
    try:
        owners = s.query(models.Owner).count()
        pets = s.query(models.Pet).count()
        appts = s.query(models.Appointment).count()
        print(f"owners {owners}")
        print(f"pets {pets}")
        print(f"appts {appts}")
    finally:
        s.close()


if __name__ == "__main__":
    main()
