from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Text
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

from app.db.database import Base


class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(120), nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")


class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    species = Column(String(50), nullable=False)
    breed = Column(String(120), nullable=True)
    birth_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    owner = relationship("Owner", back_populates="pets")

    clinical_records = relationship(
        "ClinicalRecord", back_populates="pet", cascade="all, delete-orphan"
    )
    appointments = relationship(
        "Appointment", back_populates="pet", cascade="all, delete-orphan"
    )
    vaccinations = relationship(
        "Vaccination", back_populates="pet", cascade="all, delete-orphan"
    )


class ClinicalRecord(Base):
    __tablename__ = "clinical_records"
    id = Column(Integer, primary_key=True, index=True)
    visit_date = Column(Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    # Use timezone-aware timestamps to avoid deprecation warnings and ensure UTC storage
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    symptoms = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=False)
    treatment = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)

    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    pet = relationship("Pet", back_populates="clinical_records")


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    appointment_date = Column(DateTime, nullable=False)
    reason = Column(String(120), nullable=False)  # vacunación, control, urgencia
    status = Column(String(50), default="scheduled")  # scheduled, canceled, attended
    notes = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    pet = relationship("Pet", back_populates="appointments")


class Vaccination(Base):
    __tablename__ = "vaccinations"
    id = Column(Integer, primary_key=True, index=True)
    vaccine_name = Column(String(120), nullable=False)
    applied_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(50), default="due")  # due, upcoming, done, overdue

    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    pet = relationship("Pet", back_populates="vaccinations")
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
