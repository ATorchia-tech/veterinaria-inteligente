from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.database import Base, engine, SessionLocal
from app.db import models


def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        # Owner
        owner = models.Owner(name="Juan Perez", email="juan@example.com", phone="+54 11 1234-5678")
        db.add(owner)
        db.commit()
        db.refresh(owner)

        # Pet
        pet = models.Pet(name="Firulais", species="perro", breed="mestizo", owner_id=owner.id)
        db.add(pet)
        db.commit()
        db.refresh(pet)

        # Appointment (hoy 10:00)
        today10 = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        ap = models.Appointment(date=today10, reason="vacunación", status="scheduled", pet_id=pet.id)
        db.add(ap)

        # Vaccination próxima en 14 días
        due = (today10 + timedelta(days=14)).date()
        vacc = models.Vaccination(pet_id=pet.id, vaccine_name="Rabia", due_date=due, status="upcoming")
        db.add(vacc)

        db.commit()
        print("Seed completado: owner, pet, appointment, vaccination")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
