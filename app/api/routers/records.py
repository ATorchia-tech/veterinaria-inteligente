from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.clinical_record import ClinicalRecordCreate, ClinicalRecordRead

router = APIRouter()


@router.post("/", response_model=ClinicalRecordRead)
def create_record(payload: ClinicalRecordCreate, db: Session = Depends(get_db)):
    pet = db.get(models.Pet, payload.pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    rec = models.ClinicalRecord(
        pet_id=payload.pet_id,
        symptoms=payload.symptoms,
        diagnosis=payload.diagnosis,
        treatment=payload.treatment,
        medications=payload.medications,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.post("/form", response_class=HTMLResponse)
def create_record_form(
    pet_id: int = Form(...),
    symptoms: str | None = Form(None),
    diagnosis: str | None = Form(None),
    treatment: str | None = Form(None),
    medications: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """Crear un récord clínico desde formulario HTML y mostrar confirmación."""
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    rec = models.ClinicalRecord(
        pet_id=pet_id,
        symptoms=symptoms,
        diagnosis=diagnosis,
        treatment=treatment,
        medications=medications,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    
    # Generar HTML de confirmación
    species_emoji = "🐕" if pet.species.lower() == "perro" else "🐈" if pet.species.lower() == "gato" else "🐾"
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>✅ Atención Registrada - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
        }}
        .container {{
          max-width: 800px;
          width: 100%;
          background: #fff;
          border-radius: 20px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.3);
          overflow: hidden;
          animation: slideIn 0.5s ease-out;
        }}
        @keyframes slideIn {{
          from {{
            opacity: 0;
            transform: translateY(-30px);
          }}
          to {{
            opacity: 1;
            transform: translateY(0);
          }}
        }}
        .header {{
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          padding: 3rem 2rem;
          text-align: center;
        }}
        .success-icon {{
          font-size: 5rem;
          margin-bottom: 1rem;
          animation: bounce 1s ease-in-out;
        }}
        @keyframes bounce {{
          0%, 100% {{ transform: translateY(0); }}
          50% {{ transform: translateY(-20px); }}
        }}
        .header h1 {{
          margin: 0 0 0.5rem;
          font-size: 2.5rem;
          font-weight: 700;
        }}
        .header p {{
          margin: 0;
          font-size: 1.2rem;
          opacity: 0.95;
        }}
        .content {{
          padding: 2rem;
        }}
        .info-card {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
          display: flex;
          align-items: center;
          gap: 1.5rem;
        }}
        .pet-icon {{
          font-size: 4rem;
        }}
        .pet-info {{
          flex: 1;
        }}
        .pet-name {{
          font-size: 1.8rem;
          font-weight: 700;
          margin: 0 0 0.5rem;
        }}
        .pet-details {{
          font-size: 1rem;
          opacity: 0.95;
        }}
        .record-details {{
          background: #f8f9fa;
          border-radius: 12px;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }}
        .detail-section {{
          margin-bottom: 1.5rem;
          padding-bottom: 1.5rem;
          border-bottom: 2px solid #e0e0e0;
        }}
        .detail-section:last-child {{
          margin-bottom: 0;
          padding-bottom: 0;
          border-bottom: none;
        }}
        .detail-label {{
          font-weight: 700;
          color: #555;
          margin-bottom: 0.5rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1.1rem;
        }}
        .detail-value {{
          color: #333;
          line-height: 1.6;
          padding: 0.75rem;
          background: white;
          border-radius: 8px;
          border-left: 4px solid #11998e;
          font-size: 1rem;
        }}
        .detail-value.empty {{
          color: #999;
          font-style: italic;
          border-left-color: #ccc;
        }}
        .record-id {{
          text-align: center;
          padding: 1rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-radius: 12px;
          margin-bottom: 2rem;
          font-size: 1.1rem;
        }}
        .record-id strong {{
          font-size: 1.5rem;
          display: block;
          margin-top: 0.5rem;
        }}
        .actions {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
          margin-top: 2rem;
        }}
        .btn {{
          padding: 1rem 1.5rem;
          border-radius: 10px;
          text-decoration: none;
          font-weight: 600;
          font-size: 1rem;
          transition: all 0.2s;
          display: inline-block;
          text-align: center;
          border: none;
          cursor: pointer;
        }}
        .btn-primary {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-3px);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        .btn-success {{
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
        }}
        .btn-success:hover {{
          transform: translateY(-3px);
          box-shadow: 0 6px 20px rgba(17, 153, 142, 0.4);
        }}
        .btn-secondary {{
          background: #6c757d;
          color: white;
        }}
        .btn-secondary:hover {{
          background: #5a6268;
          transform: translateY(-3px);
        }}
        .timestamp {{
          text-align: center;
          color: #999;
          font-size: 0.9rem;
          margin-top: 2rem;
          padding-top: 1.5rem;
          border-top: 2px solid #f0f0f0;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="success-icon">✅</div>
          <h1>¡Atención Registrada!</h1>
          <p>El récord clínico se guardó exitosamente</p>
        </div>
        
        <div class="content">
          <div class="info-card">
            <div class="pet-icon">{species_emoji}</div>
            <div class="pet-info">
              <h2 class="pet-name">{pet.name}</h2>
              <p class="pet-details">
                {pet.species} | Dueño: {pet.owner.name}<br>
                📅 Fecha de atención: {rec.visit_date.strftime('%d/%m/%Y')}
              </p>
            </div>
          </div>
          
          <div class="record-id">
            📋 Récord Clínico
            <strong>#{rec.id}</strong>
          </div>
          
          <div class="record-details">
            <div class="detail-section">
              <div class="detail-label">🩺 Síntomas Observados</div>
              <div class="detail-value{'empty' if not symptoms else ''}">{symptoms if symptoms else 'No se registraron síntomas'}</div>
            </div>
            
            <div class="detail-section">
              <div class="detail-label">🔍 Diagnóstico</div>
              <div class="detail-value{'empty' if not diagnosis else ''}">{diagnosis if diagnosis else 'No se registró diagnóstico'}</div>
            </div>
            
            <div class="detail-section">
              <div class="detail-label">💊 Tratamiento Prescrito</div>
              <div class="detail-value{'empty' if not treatment else ''}">{treatment if treatment else 'No se prescribió tratamiento'}</div>
            </div>
            
            <div class="detail-section">
              <div class="detail-label">💉 Medicamentos Recetados</div>
              <div class="detail-value{'empty' if not medications else ''}">{medications if medications else 'No se recetaron medicamentos'}</div>
            </div>
          </div>
          
          <div class="timestamp">
            <p>Registrado el {rec.created_at.strftime('%d/%m/%Y a las %H:%M:%S')}</p>
          </div>
          
          <div class="actions">
            <a href="/records/view?pet_id={pet.id}" class="btn btn-primary" target="_blank">
              📋 Ver todos los récords de {pet.name}
            </a>
            <a href="/pets/{pet.id}/clinical-history" class="btn btn-success" target="_blank">
              📖 Historia clínica completa
            </a>
            <a href="/vet/clinica" class="btn btn-secondary">
              ⬅️ Volver a Atención Clínica
            </a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/", response_model=List[ClinicalRecordRead])
def list_records(
    pet_id: Optional[int] = Query(default=None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(models.ClinicalRecord).order_by(
        models.ClinicalRecord.created_at.desc()
    )
    if pet_id is not None:
        q = q.filter(models.ClinicalRecord.pet_id == pet_id)
    return q.offset((page - 1) * page_size).limit(page_size).all()


@router.get("/view", response_class=HTMLResponse)
def view_records(
    pet_id: int = Query(..., description="ID de la mascota"),
    db: Session = Depends(get_db),
):
    """Vista HTML de récords clínicos de una mascota."""
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    
    # Obtener récords clínicos
    records = (
        db.query(models.ClinicalRecord)
        .filter(models.ClinicalRecord.pet_id == pet_id)
        .order_by(models.ClinicalRecord.visit_date.desc())
        .all()
    )
    
    # Emoji de especie
    species_lower = pet.species.lower()
    if 'perro' in species_lower or 'dog' in species_lower:
        species_emoji = '🐕'
    elif 'gato' in species_lower or 'cat' in species_lower:
        species_emoji = '🐈'
    else:
        species_emoji = '🐾'
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>📋 Récords Clínicos - {pet.name}</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          min-height: 100vh;
        }}
        .container {{
          max-width: 1200px;
          margin: 0 auto;
          background: #fff;
          border-radius: 16px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.3);
          overflow: hidden;
        }}
        .header {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 3rem 2rem;
          text-align: center;
        }}
        .header-icon {{
          font-size: 5rem;
          margin-bottom: 1rem;
        }}
        .header h1 {{
          margin: 0 0 1rem;
          font-size: 2.5rem;
          font-weight: 700;
        }}
        .header-subtitle {{
          opacity: 0.9;
          font-size: 1.2rem;
        }}
        .pet-info {{
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          padding: 1.5rem 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 1rem;
        }}
        .pet-info-item {{
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }}
        .content {{
          padding: 2rem;
        }}
        .summary {{
          background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
          padding: 2rem;
          border-radius: 12px;
          margin-bottom: 2rem;
          text-align: center;
        }}
        .summary-count {{
          font-size: 3rem;
          font-weight: 700;
          color: #667eea;
          margin-bottom: 0.5rem;
        }}
        .summary-label {{
          font-size: 1.2rem;
          color: #666;
        }}
        .records-list {{
          display: grid;
          gap: 1.5rem;
        }}
        .record-card {{
          background: #f8f9fa;
          border-left: 6px solid #667eea;
          border-radius: 10px;
          padding: 1.5rem;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          transition: all 0.2s;
        }}
        .record-card:hover {{
          transform: translateX(6px);
          box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}
        .record-header {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
          padding-bottom: 1rem;
          border-bottom: 2px solid #e0e0e0;
        }}
        .record-date {{
          font-size: 1.3rem;
          font-weight: 700;
          color: #333;
        }}
        .record-id {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 0.35rem 1rem;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 600;
        }}
        .record-section {{
          margin-bottom: 1rem;
        }}
        .record-section:last-child {{
          margin-bottom: 0;
        }}
        .record-label {{
          font-weight: 700;
          color: #555;
          margin-bottom: 0.5rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1rem;
        }}
        .record-value {{
          color: #333;
          line-height: 1.6;
          padding-left: 2rem;
          font-size: 1rem;
        }}
        .record-value.empty {{
          color: #999;
          font-style: italic;
        }}
        .no-records {{
          text-align: center;
          padding: 4rem 2rem;
          color: #666;
        }}
        .no-records-icon {{
          font-size: 5rem;
          margin-bottom: 1rem;
        }}
        .actions {{
          display: flex;
          gap: 1rem;
          margin-top: 2rem;
          flex-wrap: wrap;
        }}
        .btn {{
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 600;
          transition: all 0.2s;
          display: inline-block;
          text-align: center;
        }}
        .btn-primary {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        .btn-secondary {{
          background: #11998e;
          color: white;
        }}
        .btn-secondary:hover {{
          background: #38ef7d;
          transform: translateY(-2px);
        }}
        .timestamp {{
          text-align: center;
          color: #999;
          font-size: 0.85rem;
          margin-top: 2rem;
          padding-top: 1rem;
          border-top: 1px solid #e0e0e0;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="header-icon">📋</div>
          <h1>Récords Clínicos</h1>
          <p class="header-subtitle">Historia médica completa</p>
        </div>
        
        <div class="pet-info">
          <div class="pet-info-item">
            <span style="font-size: 2rem;">{species_emoji}</span>
            <div>
              <div style="font-size: 1.5rem; font-weight: 700;">{pet.name}</div>
              <div style="opacity: 0.9;">ID: #{pet.id}</div>
            </div>
          </div>
          <div class="pet-info-item">
            <div style="text-align: right;">
              <div style="font-size: 1rem; opacity: 0.9;">Dueño</div>
              <div style="font-size: 1.2rem; font-weight: 700;">{pet.owner.name}</div>
            </div>
          </div>
        </div>
        
        <div class="content">
          <div class="summary">
            <div class="summary-count">{len(records)}</div>
            <div class="summary-label">Consultas médicas registradas</div>
          </div>
          
          <div class="records-list">
    """
    
    if records:
        for record in records:
            symptoms_html = f'<div class="record-value">{record.symptoms}</div>' if record.symptoms else '<div class="record-value empty">Sin síntomas registrados</div>'
            diagnosis_html = f'<div class="record-value">{record.diagnosis}</div>' if record.diagnosis else '<div class="record-value empty">Sin diagnóstico</div>'
            treatment_html = f'<div class="record-value">{record.treatment}</div>' if record.treatment else '<div class="record-value empty">Sin tratamiento especificado</div>'
            medications_html = f'<div class="record-value">{record.medications}</div>' if record.medications else '<div class="record-value empty">Sin medicamentos recetados</div>'
            
            html_content += f"""
            <div class="record-card">
              <div class="record-header">
                <div class="record-date">📅 {record.visit_date.strftime('%d/%m/%Y')}</div>
                <div class="record-id">Récord #{record.id}</div>
              </div>
              
              <div class="record-section">
                <div class="record-label">🩺 Síntomas</div>
                {symptoms_html}
              </div>
              
              <div class="record-section">
                <div class="record-label">🔍 Diagnóstico</div>
                {diagnosis_html}
              </div>
              
              <div class="record-section">
                <div class="record-label">💊 Tratamiento</div>
                {treatment_html}
              </div>
              
              <div class="record-section">
                <div class="record-label">💉 Medicamentos</div>
                {medications_html}
              </div>
            </div>
            """
    else:
        html_content += """
            <div class="no-records">
              <div class="no-records-icon">📋</div>
              <h2 style="margin: 0 0 1rem;">Sin récords clínicos</h2>
              <p style="margin: 0; font-size: 1.1rem;">Esta mascota no tiene consultas médicas registradas.</p>
            </div>
        """
    
    html_content += f"""
          </div>
          
          <div class="timestamp">
            <p>Generado el {__import__('datetime').datetime.now().strftime('%d/%m/%Y a las %H:%M')}</p>
          </div>
          
          <div class="actions">
            <a href="/pets/{pet.id}/view" class="btn btn-primary">👁️ Ver detalles de {pet.name}</a>
            <a href="/pets/{pet.id}/clinical-history" class="btn btn-secondary">📖 Historia clínica completa</a>
            <a href="/vet/clinica" class="btn btn-secondary">⬅️ Volver a Atención Clínica</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content
