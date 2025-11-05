def test_schemas_imports():
    # Import and instantiate Create models to ensure schemas load and basic validation works
    from app.schemas.owner import OwnerCreate
    from app.schemas.pet import PetCreate
    from app.schemas.appointment import AppointmentCreate
    from app.schemas.clinical_record import ClinicalRecordCreate
    from app.schemas.vaccination import VaccinationCreate

    OwnerCreate(name="Juan Pérez")
    PetCreate(name="Firulais", species="perro", owner_id=1)
    AppointmentCreate(date="2025-11-04T15:00:00", reason="control anual", pet_id=1)
    ClinicalRecordCreate(pet_id=1)
    VaccinationCreate(vaccine_name="Antirrábica", due_date="2025-12-01", pet_id=1)

    assert True
