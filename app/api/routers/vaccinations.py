from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.vaccination import VaccinationCreate, VaccinationRead

router = APIRouter()


@router.post("/", response_model=VaccinationRead)
def create_vaccination(payload: VaccinationCreate, db: Session = Depends(get_db)):
    pet = db.get(models.Pet, payload.pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    v = models.Vaccination(
        pet_id=payload.pet_id,
        vaccine_name=payload.vaccine_name,
        due_date=payload.due_date,
        applied_date=payload.applied_date,
        notes=payload.notes,
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


@router.post("/form", response_model=VaccinationRead)
def create_vaccination_form(
    pet_id: int = Form(...),
    vaccine_name: str = Form(...),
    due_date: date = Form(...),
    applied_date: date = Form(...),
    notes: str | None = Form(None),
    db: Session = Depends(get_db),
):
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    v = models.Vaccination(
        pet_id=pet_id,
        vaccine_name=vaccine_name,
        due_date=due_date,
        applied_date=applied_date,
        notes=notes,
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


@router.get("/upcoming", response_model=List[VaccinationRead])
def upcoming_json(
    days: int = Query(30, ge=1, le=365),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Vacunas próximas en formato JSON."""
    today = date.today()
    limit = today + timedelta(days=days)
    q = (
        db.query(models.Vaccination)
        .filter(
            models.Vaccination.due_date >= today, models.Vaccination.due_date <= limit
        )
        .order_by(models.Vaccination.due_date.asc())
    )
    return q.offset((page - 1) * page_size).limit(page_size).all()


@router.get("/view", response_class=HTMLResponse)
def view_vaccinations(
    pet_id: Optional[int] = Query(None),
    type: Optional[str] = Query(None),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Vista HTML de vacunas próximas o vencidas."""
    today = date.today()
    
    # Si se especifica pet_id, mostrar todas las vacunas de esa mascota
    if pet_id is not None:
        pet = db.get(models.Pet, pet_id)
        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found")
        
        # Obtener emoji de la especie
        species_emoji = "🐕" if pet.species.lower() == "perro" else "🐈" if pet.species.lower() == "gato" else "🐾"
        
        # Todas las vacunas del pet
        vaccinations = (
            db.query(models.Vaccination)
            .filter(models.Vaccination.pet_id == pet_id)
            .order_by(models.Vaccination.due_date.asc())
            .all()
        )
        title = f"{species_emoji} Vacunas de {pet.name}"
        subtitle = f"Dueño/a: {pet.owner.name} - Total: {len(vaccinations)} vacunas"
        gradient = "linear-gradient(135deg, #764ba2 0%, #667eea 100%)"
        color = "#667eea"
        is_overdue = False  # No aplica cuando vemos todas las vacunas
        list_label = "registradas"
    
    # Determinar tipo de vista
    elif type == "overdue":
        # Vacunas vencidas (due_date < hoy)
        vaccinations = (
            db.query(models.Vaccination)
            .filter(models.Vaccination.due_date < today)
            .order_by(models.Vaccination.due_date.asc())
            .all()
        )
        title = "🚨 Vacunas Vencidas"
        subtitle = "Requieren atención urgente"
        gradient = "linear-gradient(135deg, #dc3545 0%, #c82333 100%)"
        color = "#dc3545"
        is_overdue = True
        list_label = "vencidas"
    else:
        # Vacunas próximas (hoy <= due_date <= hoy + days)
        limit = today + timedelta(days=days)
        vaccinations = (
            db.query(models.Vaccination)
            .filter(
                models.Vaccination.due_date >= today,
                models.Vaccination.due_date <= limit
            )
            .order_by(models.Vaccination.due_date.asc())
            .all()
        )
        title = f"⚠️ Vacunas Próximas ({days} días)"
        subtitle = f"Vencen entre hoy y {limit.strftime('%d/%m/%Y')}"
        gradient = "linear-gradient(135deg, #ffc107 0%, #ff9800 100%)"
        color = "#ff9800"
        is_overdue = False
        list_label = "próximas a vencer"
    
    # Calcular urgencia
    def get_urgency(vac):
        delta = (vac.due_date - today).days
        if delta < 0:
            return "overdue", abs(delta)
        elif delta <= 7:
            return "urgent", delta
        elif delta <= 30:
            return "warning", delta
        else:
            return "normal", delta
    
    # Generar HTML
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>{title} - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: {gradient};
          min-height: 100vh;
        }}
        .container {{
          max-width: 1400px;
          margin: 0 auto;
          background: #fff;
          border-radius: 16px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.3);
          padding: 2rem;
        }}
        header {{
          text-align: center;
          margin-bottom: 2rem;
          padding-bottom: 1.5rem;
          border-bottom: 3px solid #f0f0f0;
        }}
        header h1 {{
          margin: 0 0 .5rem;
          font-size: 2.5rem;
          color: #333;
          font-weight: 700;
        }}
        header p {{
          margin: .5rem 0 0;
          color: #666;
          font-size: 1.1rem;
        }}
        .summary {{
          background: {gradient};
          color: white;
          padding: 2rem;
          border-radius: 12px;
          margin-bottom: 2rem;
          text-align: center;
        }}
        .summary h2 {{
          margin: 0;
          font-size: 3rem;
          font-weight: 700;
        }}
        .summary p {{
          margin: 0.5rem 0 0;
          font-size: 1.2rem;
          opacity: 0.9;
        }}
        .vaccinations-grid {{
          display: grid;
          gap: 1rem;
        }}
        .vaccination-card {{
          background: #f8f9fa;
          border-left: 5px solid {color};
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          transition: transform 0.2s, box-shadow 0.2s;
        }}
        .vaccination-card:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}
        .vaccination-card.overdue {{
          border-left-color: #dc3545;
          background: #fff5f5;
        }}
        .vaccination-card.urgent {{
          border-left-color: #ff6b6b;
          background: #fff9f9;
        }}
        .vaccination-card.warning {{
          border-left-color: #ffc107;
          background: #fffef5;
        }}
        .vaccination-header {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
          flex-wrap: wrap;
          gap: 1rem;
        }}
        .vaccination-name {{
          font-size: 1.5rem;
          font-weight: 700;
          color: #333;
        }}
        .due-date {{
          font-size: 1.2rem;
          color: #666;
          font-weight: 600;
        }}
        .urgency-badge {{
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 600;
          text-transform: uppercase;
        }}
        .urgency-badge.overdue {{
          background: #dc3545;
          color: white;
        }}
        .urgency-badge.urgent {{
          background: #ff6b6b;
          color: white;
        }}
        .urgency-badge.warning {{
          background: #ffc107;
          color: #333;
        }}
        .urgency-badge.normal {{
          background: #28a745;
          color: white;
        }}
        .vaccination-details {{
          display: grid;
          gap: 0.75rem;
        }}
        .detail-row {{
          display: grid;
          grid-template-columns: 180px 1fr;
          gap: 1rem;
          align-items: start;
        }}
        .detail-label {{
          font-weight: 600;
          color: #666;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }}
        .detail-value {{
          color: #333;
          line-height: 1.5;
        }}
        .detail-value.highlight {{
          font-weight: 600;
          color: {color};
          font-size: 1.1rem;
        }}
        .contact-info {{
          background: #e3f2fd;
          padding: 1rem;
          border-radius: 8px;
          margin-top: 0.5rem;
          border-left: 3px solid #2196f3;
        }}
        .contact-info p {{
          margin: 0.25rem 0;
          color: #0d47a1;
        }}
        .contact-info strong {{
          color: #01579b;
        }}
        .no-vaccinations {{
          text-align: center;
          padding: 3rem;
          color: #666;
          font-size: 1.2rem;
        }}
        .no-vaccinations-icon {{
          font-size: 4rem;
          margin-bottom: 1rem;
        }}
        .back-link {{
          display: inline-block;
          margin-top: 2rem;
          padding: 0.75rem 1.5rem;
          background: {gradient};
          color: white;
          text-decoration: none;
          border-radius: 8px;
          font-weight: 600;
          transition: transform 0.2s;
        }}
        .back-link:hover {{
          transform: translateY(-2px);
        }}
        @media (max-width: 768px) {{
          .detail-row {{
            grid-template-columns: 1fr;
            gap: 0.25rem;
          }}
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <header>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </header>
        
        <div class="summary">
          <h2>{len(vaccinations)}</h2>
          <p>vacunas {list_label}</p>
        </div>
        
        <div class="vaccinations-grid">
    """
    
    if vaccinations:
        for vac in vaccinations:
            urgency_type, days_diff = get_urgency(vac)
            
            urgency_text = {
                'overdue': f'VENCIDA hace {days_diff} días',
                'urgent': f'Vence en {days_diff} días',
                'warning': f'Vence en {days_diff} días',
                'normal': f'Vence en {days_diff} días'
            }.get(urgency_type, '')
            
            due_date_str = vac.due_date.strftime('%d/%m/%Y')
            applied_date_str = 'N/A'
            if vac.applied_date is not None:
                applied_date_str = vac.applied_date.strftime('%d/%m/%Y')
            
            pet_name = vac.pet.name if vac.pet else 'N/A'
            pet_species = vac.pet.species if vac.pet else 'N/A'
            pet_breed = vac.pet.breed if vac.pet else 'N/A'
            
            # Nombre del dueño
            if vac.pet and vac.pet.owner:
                owner_name = vac.pet.owner.name
                owner_phone = vac.pet.owner.phone if vac.pet.owner.phone else 'N/A'
                owner_email = vac.pet.owner.email if vac.pet.owner.email else 'N/A'
            else:
                owner_name = 'N/A'
                owner_phone = 'N/A'
                owner_email = 'N/A'
            
            html_content += f"""
          <div class="vaccination-card {urgency_type}">
            <div class="vaccination-header">
              <div class="vaccination-name">💉 {vac.vaccine_name}</div>
              <div class="urgency-badge {urgency_type}">{urgency_text}</div>
            </div>
            <div class="vaccination-details">
              <div class="detail-row">
                <span class="detail-label">📅 Vencimiento:</span>
                <span class="detail-value highlight">{due_date_str}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">📆 Última aplicación:</span>
                <span class="detail-value">{applied_date_str}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">🐾 Mascota:</span>
                <span class="detail-value highlight">{pet_name}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">🔍 Especie/Raza:</span>
                <span class="detail-value">{pet_species} - {pet_breed}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">📋 Estado:</span>
                <span class="detail-value">{vac.status}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">🔑 ID Vacuna:</span>
                <span class="detail-value">#{vac.id}</span>
              </div>
            </div>
            
            <div class="contact-info">
              <p><strong>👤 Dueño:</strong> {owner_name}</p>
              <p><strong>📞 Teléfono:</strong> {owner_phone}</p>
              <p><strong>📧 Email:</strong> {owner_email}</p>
            </div>
          </div>
            """
    else:
        # Mensaje personalizado dependiendo del contexto
        if pet_id is not None:
            no_vac_icon = "😊"
            no_vac_msg = "Esta mascota aún no tiene vacunas registradas."
        elif is_overdue:
            no_vac_icon = "✅"
            no_vac_msg = "¡Excelente! No hay vacunas vencidas."
        else:
            no_vac_icon = "😌"
            no_vac_msg = "No hay vacunas próximas a vencer en este período."
        
        html_content += f"""
          <div class="no-vaccinations">
            <div class="no-vaccinations-icon">{no_vac_icon}</div>
            <p>{no_vac_msg}</p>
          </div>
        """
    
    html_content += """
        </div>
        
        <div style="text-align: center;">
          <a href="/vet/gestion" class="back-link">⬅️ Volver a Gestión Veterinaria</a>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content

