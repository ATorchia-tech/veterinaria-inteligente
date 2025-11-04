from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.pet import PetCreate, PetRead

router = APIRouter()


@router.post("/", response_model=PetRead)
def create_pet(payload: PetCreate, db: Session = Depends(get_db)):
    owner = db.get(models.Owner, payload.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    pet = models.Pet(
        name=payload.name,
        species=payload.species,
        breed=payload.breed,
        birth_date=payload.birth_date,
        notes=payload.notes,
        owner_id=payload.owner_id,
    )
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.get("/", response_model=List[PetRead])
def list_pets(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(models.Pet).order_by(models.Pet.id.asc())
    return q.offset((page - 1) * page_size).limit(page_size).all()


@router.get("/{pet_id}", response_model=PetRead)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet
