from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import cast
import argparse
import random
import re
import requests

from app.db.database import Base, engine, SessionLocal
from app.db import models


def _get_or_create_owner(db: Session, name: str, email: str, phone: str) -> models.Owner:
    owner = db.query(models.Owner).filter(models.Owner.email == email).first()
    if owner:
        return owner
    owner = models.Owner(name=name, email=email, phone=phone)
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


def _get_or_create_pet(
    db: Session,
    owner_id: int,
    name: str,
    species: str,
    breed: str | None = None,
):
    pet = (
        db.query(models.Pet)
        .filter(models.Pet.owner_id == owner_id, models.Pet.name == name)
        .first()
    )
    if pet:
        return pet
    pet = models.Pet(name=name, species=species, breed=breed, owner_id=owner_id)
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


def _get_or_create_appointment(
    db: Session, pet_id: int, date: datetime, reason: str, status: str = "scheduled"
):
    ap = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.pet_id == pet_id,
            models.Appointment.appointment_date == date,
            models.Appointment.reason == reason,
        )
        .first()
    )
    if ap:
        return ap
    ap = models.Appointment(pet_id=pet_id, appointment_date=date, reason=reason, status=status)
    db.add(ap)
    db.commit()
    db.refresh(ap)
    return ap


def _get_or_create_vaccination(
    db: Session, pet_id: int, vaccine_name: str, applied_date, due_date
):
    vacc = (
        db.query(models.Vaccination)
        .filter(
            models.Vaccination.pet_id == pet_id,
            models.Vaccination.vaccine_name == vaccine_name,
            models.Vaccination.due_date == due_date,
        )
        .first()
    )
    if vacc:
        return vacc
    vacc = models.Vaccination(
        pet_id=pet_id, 
        vaccine_name=vaccine_name, 
        applied_date=applied_date,
        due_date=due_date, 
        status="upcoming"
    )
    db.add(vacc)
    db.commit()
    db.refresh(vacc)
    return vacc


def seed():
    """Siembra datos base de forma idempotente.

    Criterios de unicidad:
    - Owner: email
    - Pet: (owner_id, name)
    - Appointment: (pet_id, date exacta, reason)
    - Vaccination: (pet_id, vaccine_name, due_date)
    Repetir la siembra no duplica registros.
    """

    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        owner = _get_or_create_owner(
            db,
            name="Juan Perez",
            email="juan@example.com",
            phone="+54 11 1234-5678",
        )

        pet = _get_or_create_pet(
            db,
            owner_id=cast(int, owner.id),
            name="Firulais",
            species="perro",
            breed="mestizo",
        )

        today10 = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        _get_or_create_appointment(
            db, pet_id=cast(int, pet.id), date=today10, reason="vacunación", status="scheduled"
        )

        applied = (today10 - timedelta(days=365)).date()  # Aplicada hace 1 año
        due = (today10 + timedelta(days=14)).date()
        _get_or_create_vaccination(
            db, 
            pet_id=cast(int, pet.id), 
            vaccine_name="Rabia", 
            applied_date=applied,
            due_date=due
        )

        print(
            "Seed idempotente completado: owner (email=juan@example.com), pet (Firulais), appointment hoy 10:00, vaccination Rabia"
        )
    finally:
        db.close()


def seed_bulk(min_count: int = 200):
    """Genera al menos `min_count` Dueños, Mascotas y Turnos de forma idempotente.

    Para i en 1..min_count:
      - Owner: bulk_owner_{i}@example.com
      - Pet:   BulkPet{i} (alternando especie perro/gato)
      - Appt:  hoy 09:00 + i minutos, reason "control {i}"
    """
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        base_dt = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        for i in range(1, min_count + 1):
            email = f"bulk_owner_{i:03d}@example.com"
            name = f"Owner {i:03d}"
            phone = f"+54 11 {1000+i:04d}-{2000+i:04d}"
            owner = _get_or_create_owner(db, name=name, email=email, phone=phone)

            pet_name = f"BulkPet{i:03d}"
            species = "perro" if i % 2 == 0 else "gato"
            breed = "mestizo" if species == "perro" else "siamés"
            pet = _get_or_create_pet(
                db, owner_id=cast(int, owner.id), name=pet_name, species=species, breed=breed
            )

            ap_dt = base_dt + timedelta(minutes=i)
            reason = f"control {i:03d}"
            _get_or_create_appointment(db, pet_id=cast(int, pet.id), date=ap_dt, reason=reason)

        print(
            f"Seed bulk idempotente: asegurados >= {min_count} owners/pets/appointments"
        )
    finally:
        db.close()


def _extract_anchor_texts(html: str) -> list[str]:
    """Extracts anchor texts from HTML, simple regex-based.

    Note: This is a very lightweight parser to avoid extra dependencies.
    It will include many links; callers are expected to trim and uniq.
    """
    # Remove refs/superscripts
    html = re.sub(r"<sup[^>]*>.*?</sup>", "", html, flags=re.DOTALL)
    texts = re.findall(r"<a[^>]+>([^<]+)</a>", html)
    # Clean whitespace and artifacts
    cleaned = []
    for t in texts:
        t = re.sub(r"\[.*?\]", "", t).strip()
        if t:
            cleaned.append(t)
    return cleaned


def _fetch_wikipedia(url: str) -> str:
    res = requests.get(url, timeout=15)
    res.raise_for_status()
    return res.text


def _fetch_dog_breeds_from_wiki(max_items: int = 200) -> list[str]:
    """Fetch dog breed names from Wikipedia (List of dog breeds).

    Source: https://en.wikipedia.org/wiki/List_of_dog_breeds (CC BY-SA 4.0)
    """
    try:
        html = _fetch_wikipedia("https://en.wikipedia.org/wiki/List_of_dog_breeds")
        # Limit to extant breeds section to reduce noise
        m = re.search(
            r"Extant breeds, varieties and types(.*?)Extinct and critically endangered",
            html,
            flags=re.DOTALL | re.IGNORECASE,
        )
        section = m.group(1) if m else html
        names = _extract_anchor_texts(section)
        # Heuristic filters: remove obviously non-breed terms and duplicates
        bad_substrings = [
            "Edit", "Talk", "Read", "View", "Template", "Help:", "Category:",
            "List of", "Most popular", "Portal", "Dog type", "Breed",
        ]
        out: list[str] = []
        seen = set()
        for n in names:
            if any(bs in n for bs in bad_substrings):
                continue
            # Skip generic types
            if n.lower() in {"mongrel", "dog", "dogs"}:
                continue
            key = n.strip()
            if key and key not in seen:
                seen.add(key)
                out.append(key)
            if len(out) >= max_items:
                break
        return out
    except Exception:
        # Fallback minimal list
        return [
            "Labrador Retriever",
            "German Shepherd",
            "Golden Retriever",
            "Bulldog",
            "Poodle",
            "Beagle",
            "Rottweiler",
            "Yorkshire Terrier",
            "Boxer",
            "Dachshund",
        ]


def _fetch_cat_breeds_from_wiki(max_items: int = 200) -> list[str]:
    """Fetch cat breed names from Wikipedia (List of cat breeds / Category page).

    Tries the List page first; on failure, tries the Category page.
    """
    try:
        html = _fetch_wikipedia("https://en.wikipedia.org/wiki/List_of_cat_breeds")
        # The page contains a large table; just pull anchor texts from the breeds section
        m = re.search(r">Breeds<.*?(</table>)", html, flags=re.DOTALL | re.IGNORECASE)
        section = m.group(0) if m else html
        names = _extract_anchor_texts(section)
        bad_words = [
            "Edit", "Talk", "Read", "View", "Template", "Help:", "Category:",
            "List of", "Portal", "Cat family", "Felidae", "Oriental Longhair",
        ]
        out: list[str] = []
        seen = set()
        for n in names:
            if any(bw in n for bw in bad_words):
                continue
            # Many breed names end with 'cat' but not all; keep broad set
            key = n.strip()
            if key and key not in seen and len(key) <= 40:
                seen.add(key)
                out.append(key)
            if len(out) >= max_items:
                break
        if out:
            return out
        raise RuntimeError("empty list")
    except Exception:
        try:
            html = _fetch_wikipedia("https://en.wikipedia.org/wiki/Category:Cat_breeds")
            names = _extract_anchor_texts(html)
            out: list[str] = []
            seen = set()
            for n in names:
                if "cat" in n.lower() or n.istitle():
                    key = n.strip()
                    if key and key not in seen:
                        seen.add(key)
                        out.append(key)
                if len(out) >= max_items:
                    break
            if out:
                return out
        except Exception:
            pass
        # Fallback minimal
        return [
            "Siamese", "Persian", "Maine Coon", "Ragdoll", "Bengal",
            "Sphynx", "British Shorthair", "Abyssinian", "Scottish Fold", "Russian Blue",
        ]


def seed_internet(count: int = 100):
    """Genera N registros (Owner, Pet, Appointment) usando listas de razas obtenidas de Internet.

    Fuentes:
      - Dog breeds: Wikipedia List of dog breeds (CC BY-SA 4.0)
      - Cat breeds: Wikipedia List/Category of cat breeds (CC BY-SA 4.0)

    Idempotente vía llaves:
      Owner: email internet_owner_{i:03d}@example.com
      Pet: (owner_id, pet_name)
      Appointment: (pet_id, date, reason)
    """
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        random.seed(42)  # determinismo suave

        dog_breeds = _fetch_dog_breeds_from_wiki(300)
        cat_breeds = _fetch_cat_breeds_from_wiki(300)

        pet_names = [
            "Luna", "Max", "Bella", "Charlie", "Milo", "Nala", "Rocky", "Coco",
            "Simba", "Lola", "Toby", "Mia", "Lucy", "Leo", "Kira", "Bruno",
        ]
        reasons = [
            "control", "vacunación", "chequeo", "desparasitación", "consulta",
        ]

        base_dt = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
        for i in range(1, count + 1):
            email = f"internet_owner_{i:03d}@example.com"
            name = f"Internet Owner {i:03d}"
            phone = f"+54 11 {3000+i:04d}-{4000+i:04d}"
            owner = _get_or_create_owner(db, name=name, email=email, phone=phone)

            species = "perro" if i % 2 == 1 else "gato"
            breed = (
                random.choice(dog_breeds) if species == "perro" else random.choice(cat_breeds)
            )
            pet_name = f"{random.choice(pet_names)}{i:02d}"
            pet = _get_or_create_pet(
                db,
                owner_id=cast(int, owner.id),
                name=pet_name,
                species=species,
                breed=breed,
            )

            ap_dt = base_dt + timedelta(minutes=i)
            reason = f"{random.choice(reasons)} ({breed})"
            _get_or_create_appointment(
                db, pet_id=cast(int, pet.id), date=ap_dt, reason=reason
            )

        print(
            f"Seed internet: cargados >= {count} registros usando razas de Wikipedia (CC BY-SA 4.0)."
        )
    finally:
        db.close()


def seed_today_appointments(count: int = 10):
    """Genera turnos para el día de hoy con diferentes estados y horarios."""
    db = SessionLocal()
    try:
        # Asegurar que hay al menos algunos dueños y mascotas
        owners_count = db.query(models.Owner).count()
        if owners_count == 0:
            print("No hay dueños en la base. Ejecutando seed base primero...")
            seed()
        
        pets = db.query(models.Pet).all()
        if not pets:
            print("No hay mascotas en la base. No se pueden crear turnos.")
            return
        
        today = datetime.now().date()
        estados = ["scheduled", "attended", "canceled"]
        motivos = [
            "control anual",
            "vacunación",
            "revisión",
            "urgencia",
            "consulta general",
            "chequeo post-operatorio",
            "análisis de sangre",
            "desparasitación",
            "castración",
            "tratamiento dental",
        ]
        
        # Generar turnos distribuidos en horario laboral (9:00 - 18:00)
        horarios_base = [9, 10, 11, 12, 14, 15, 16, 17]
        
        random.seed(42)  # Para reproducibilidad
        
        turnos_creados = 0
        for i in range(count):
            pet = random.choice(pets)
            hora = random.choice(horarios_base)
            minuto = random.choice([0, 15, 30, 45])
            
            date_time = datetime.combine(
                today, datetime.min.time()
            ).replace(hour=hora, minute=minuto)
            
            # Asignar estado según el horario
            # Turnos pasados: mayormente atendidos o cancelados
            # Turnos futuros: scheduled
            now = datetime.now()
            if date_time < now:
                estado = random.choices(
                    estados,
                    weights=[10, 70, 20],  # scheduled, attended, canceled
                    k=1
                )[0]
            else:
                estado = random.choices(
                    estados,
                    weights=[85, 5, 10],  # scheduled, attended, canceled
                    k=1
                )[0]
            
            motivo = random.choice(motivos)
            
            _get_or_create_appointment(
                db,
                pet_id=cast(int, pet.id),
                date=date_time,
                reason=motivo,
                status=estado,
            )
            turnos_creados += 1
        
        print(
            f"Seed today appointments: cargados {turnos_creados} turnos para hoy ({today})."
        )
    finally:
        db.close()


def seed_two_months_appointments(count_per_day: int = 8):
    """Genera turnos distribuidos en los próximos 2 meses."""
    db = SessionLocal()
    try:
        # Asegurar que hay al menos algunos dueños y mascotas
        owners_count = db.query(models.Owner).count()
        if owners_count == 0:
            print("No hay dueños en la base. Ejecutando seed base primero...")
            seed()
        
        pets = db.query(models.Pet).all()
        if not pets:
            print("No hay mascotas en la base. No se pueden crear turnos.")
            return
        
        today = datetime.now().date()
        end_date = today + timedelta(days=60)  # 2 meses
        
        estados = ["scheduled", "attended", "canceled"]
        motivos = [
            "control anual",
            "vacunación",
            "revisión",
            "urgencia",
            "consulta general",
            "chequeo post-operatorio",
            "análisis de sangre",
            "desparasitación",
            "castración",
            "tratamiento dental",
            "limpieza dental",
            "radiografía",
            "ecografía",
            "cirugía menor",
            "control de peso",
        ]
        
        # Horarios laborales
        horarios_base = [9, 10, 11, 12, 14, 15, 16, 17]
        
        random.seed(42)  # Para reproducibilidad
        
        turnos_creados = 0
        current_date = today
        
        while current_date <= end_date:
            # Solo días laborales (lunes a viernes)
            if current_date.weekday() < 5:  # 0=lunes, 4=viernes
                for _ in range(count_per_day):
                    pet = random.choice(pets)
                    hora = random.choice(horarios_base)
                    minuto = random.choice([0, 15, 30, 45])
                    
                    date_time = datetime.combine(
                        current_date, datetime.min.time()
                    ).replace(hour=hora, minute=minuto)
                    
                    # Asignar estado según la fecha
                    now = datetime.now()
                    if date_time < now:
                        # Turnos pasados: mayormente atendidos
                        estado = random.choices(
                            estados,
                            weights=[5, 80, 15],  # scheduled, attended, canceled
                            k=1
                        )[0]
                    else:
                        # Turnos futuros: principalmente scheduled
                        estado = random.choices(
                            estados,
                            weights=[90, 5, 5],  # scheduled, attended, canceled
                            k=1
                        )[0]
                    
                    motivo = random.choice(motivos)
                    
                    _get_or_create_appointment(
                        db,
                        pet_id=cast(int, pet.id),
                        date=date_time,
                        reason=motivo,
                        status=estado,
                    )
                    turnos_creados += 1
            
            current_date += timedelta(days=1)
        
        print(
            f"Seed two months: cargados {turnos_creados} turnos desde {today} hasta {end_date}."
        )
    finally:
        db.close()


def seed_vaccinations_samples(count: int = 50):
    """Genera vacunas de muestra con diferentes estados de vencimiento."""
    db = SessionLocal()
    try:
        pets = db.query(models.Pet).all()
        if not pets:
            print("No hay mascotas en la base. Ejecutando seed base primero...")
            seed()
            pets = db.query(models.Pet).all()
        
        if not pets:
            print("No se pueden crear vacunas sin mascotas.")
            return
        
        today = datetime.now().date()
        
        vaccines = [
            "Rabia",
            "Séxtuple (Parvovirus, Moquillo, Hepatitis, Leptospirosis, Parainfluenza, Coronavirus)",
            "Triple Felina",
            "Antirábica",
            "Parvovirus",
            "Moquillo",
            "Bordetella",
            "Leptospirosis",
            "Leucemia Felina",
            "Giardia",
        ]
        
        random.seed(42)
        
        vacunas_creadas = 0
        
        # Distribuir vacunas en diferentes rangos de tiempo
        # 20% vencidas (hace 1-60 días)
        # 30% próximas urgentes (1-7 días)
        # 30% próximas advertencia (8-30 días)
        # 20% futuras (31-90 días)
        
        for i in range(count):
            pet = random.choice(pets)
            vaccine_name = random.choice(vaccines)
            
            # Determinar rango de fecha
            rand = random.random()
            if rand < 0.2:
                # Vencidas
                days_offset = -random.randint(1, 60)
            elif rand < 0.5:
                # Próximas urgentes (1-7 días)
                days_offset = random.randint(1, 7)
            elif rand < 0.8:
                # Próximas advertencia (8-30 días)
                days_offset = random.randint(8, 30)
            else:
                # Futuras (31-90 días)
                days_offset = random.randint(31, 90)
            
            due_date = today + timedelta(days=days_offset)
            
            # Fecha de aplicación (aprox 1 año antes del vencimiento)
            applied_date = due_date - timedelta(days=365)
            
            status = "overdue" if days_offset < 0 else "due"
            
            # Verificar si ya existe
            exists = (
                db.query(models.Vaccination)
                .filter(
                    models.Vaccination.pet_id == cast(int, pet.id),
                    models.Vaccination.vaccine_name == vaccine_name,
                    models.Vaccination.due_date == due_date,
                )
                .first()
            )
            
            if not exists:
                vac = models.Vaccination(
                    pet_id=cast(int, pet.id),
                    vaccine_name=vaccine_name,
                    applied_date=applied_date,
                    due_date=due_date,
                    status=status,
                )
                db.add(vac)
                vacunas_creadas += 1
        
        db.commit()
        print(
            f"Seed vaccinations: cargadas {vacunas_creadas} vacunas de muestra."
        )
    finally:
        db.close()


def seed_clinical_records_samples(count: int = 30):
    """Genera récords clínicos de muestra para las mascotas existentes."""
    db = SessionLocal()
    try:
        pets = db.query(models.Pet).all()
        if not pets:
            print("No hay mascotas en la base. Ejecutando seed base primero...")
            seed()
            pets = db.query(models.Pet).all()
        
        if not pets:
            print("No se pueden crear récords sin mascotas.")
            return
        
        today = datetime.now().date()
        
        symptoms_list = [
            "Tos persistente",
            "Vómitos",
            "Diarrea",
            "Falta de apetito",
            "Letargo",
            "Fiebre",
            "Cojera",
            "Rascado excesivo",
            "Pérdida de peso",
            "Dificultad para respirar",
        ]
        
        diagnoses_list = [
            "Infección respiratoria leve",
            "Gastroenteritis",
            "Parásitos intestinales",
            "Otitis externa",
            "Dermatitis alérgica",
            "Infección urinaria",
            "Artritis",
            "Conjuntivitis",
            "Control de rutina - sano",
            "Reacción alérgica leve",
        ]
        
        treatments_list = [
            "Reposo y observación",
            "Dieta blanda por 3 días",
            "Antibióticos",
            "Antiinflamatorios",
            "Limpieza de oídos",
            "Baño medicinal",
            "Aplicación de gotas oftálmicas",
            "Cambio de alimentación",
            "Hidratación",
            "Analgésicos",
        ]
        
        medications_list = [
            "Amoxicilina 250mg cada 12hs por 7 días",
            "Carprofeno 50mg cada 24hs por 5 días",
            "Metronidazol 100mg cada 12hs por 5 días",
            "Prednisolona 5mg cada 24hs por 3 días",
            "Omeprazol 20mg cada 24hs por 10 días",
            None,  # Sin medicamentos
        ]
        
        random.seed(42)
        
        records_creados = 0
        
        for i in range(count):
            pet = random.choice(pets)
            
            # Fecha de visita entre hace 6 meses y hoy
            days_ago = random.randint(0, 180)
            visit_date = today - timedelta(days=days_ago)
            
            symptoms = random.choice(symptoms_list)
            diagnosis = random.choice(diagnoses_list)
            treatment = random.choice(treatments_list)
            medications = random.choice(medications_list)
            
            # Verificar si ya existe un record similar
            exists = (
                db.query(models.ClinicalRecord)
                .filter(
                    models.ClinicalRecord.pet_id == cast(int, pet.id),
                    models.ClinicalRecord.visit_date == visit_date,
                    models.ClinicalRecord.diagnosis == diagnosis,
                )
                .first()
            )
            
            if not exists:
                record = models.ClinicalRecord(
                    pet_id=cast(int, pet.id),
                    visit_date=visit_date,
                    symptoms=symptoms,
                    diagnosis=diagnosis,
                    treatment=treatment,
                    medications=medications,
                )
                db.add(record)
                records_creados += 1
        
        db.commit()
        print(
            f"Seed clinical records: cargados {records_creados} récords clínicos de muestra."
        )
    finally:
        db.close()


def _parse_args():
    parser = argparse.ArgumentParser(description="Seeder idempotente")
    parser.add_argument(
        "--bulk",
        type=int,
        default=0,
        help="Genera al menos N dueños/mascotas/turnos (idempotente)",
    )
    parser.add_argument(
        "--internet",
        type=int,
        default=0,
        help="Genera N registros usando listas de razas obtenidas de Internet",
    )
    parser.add_argument(
        "--today-appointments",
        type=int,
        default=0,
        help="Número de turnos a generar para el día de hoy.",
    )
    parser.add_argument(
        "--two-months",
        type=int,
        default=0,
        help="Número de turnos por día a generar para los próximos 2 meses (solo días laborales).",
    )
    parser.add_argument(
        "--vaccinations",
        type=int,
        default=0,
        help="Número de vacunas de muestra a generar con diferentes estados.",
    )
    parser.add_argument(
        "--clinical-records",
        type=int,
        default=0,
        help="Número de récords clínicos de muestra a generar.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    seed()
    if args.bulk and args.bulk > 0:
        seed_bulk(args.bulk)
    if args.internet and args.internet > 0:
        seed_internet(args.internet)
    if args.today_appointments and args.today_appointments > 0:
        seed_today_appointments(args.today_appointments)
    if args.two_months and args.two_months > 0:
        seed_two_months_appointments(args.two_months)
    if args.vaccinations and args.vaccinations > 0:
        seed_vaccinations_samples(args.vaccinations)
    if args.clinical_records and args.clinical_records > 0:
        seed_clinical_records_samples(args.clinical_records)
