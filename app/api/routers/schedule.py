from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.appointment import AppointmentRead

router = APIRouter()


@router.get("/day", response_model=List[AppointmentRead])
def agenda_diaria_json(
    day: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """Agenda diaria en formato JSON. Acepta 'day' como parámetro."""
    d = day or datetime.now().date()
    start = datetime(d.year, d.month, d.day)
    end = start + timedelta(days=1)
    q = (
        db.query(models.Appointment)
        .filter(models.Appointment.appointment_date >= start, models.Appointment.appointment_date < end)
        .order_by(models.Appointment.appointment_date.asc())
    )
    return q.all()


@router.get("/daily", response_class=HTMLResponse)
def agenda_diaria_html(
    date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Agenda diaria en formato HTML. Acepta 'date' como parámetro (YYYY-MM-DD)."""
    # Parsear fecha
    if date:
        try:
            d = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            d = datetime.now().date()
    else:
        d = datetime.now().date()
    
    start = datetime(d.year, d.month, d.day)
    end = start + timedelta(days=1)
    
    appointments = (
        db.query(models.Appointment)
        .filter(models.Appointment.appointment_date >= start, models.Appointment.appointment_date < end)
        .order_by(models.Appointment.appointment_date.asc())
        .all()
    )
    
    # Calcular estadísticas
    total = len(appointments)
    attended = sum(1 for a in appointments if str(a.status) == 'attended')
    scheduled = sum(1 for a in appointments if str(a.status) == 'scheduled')
    canceled = sum(1 for a in appointments if str(a.status) == 'canceled')
    
    # Generar HTML
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>📅 Agenda del Día - {d.strftime('%d/%m/%Y')}</title>
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
        .stats {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
          margin-bottom: 2rem;
        }}
        .stat-card {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1.5rem;
          border-radius: 12px;
          text-align: center;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
          margin: 0 0 0.5rem;
          font-size: 2rem;
          font-weight: 700;
        }}
        .stat-card p {{
          margin: 0;
          font-size: 0.9rem;
          opacity: 0.9;
        }}
        .appointments-grid {{
          display: grid;
          gap: 1rem;
        }}
        .appointment-card {{
          background: #f8f9fa;
          border-left: 5px solid #667eea;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          transition: transform 0.2s, box-shadow 0.2s;
        }}
        .appointment-card:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}
        .appointment-card.attended {{
          border-left-color: #28a745;
          background: #f0f9f4;
        }}
        .appointment-card.canceled {{
          border-left-color: #dc3545;
          background: #fcf2f3;
        }}
        .appointment-card.scheduled {{
          border-left-color: #667eea;
          background: #f5f6ff;
        }}
        .appointment-header {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }}
        .appointment-time {{
          font-size: 1.5rem;
          font-weight: 700;
          color: #333;
        }}
        .status-badge {{
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 600;
          text-transform: uppercase;
        }}
        .status-badge.attended {{
          background: #28a745;
          color: white;
        }}
        .status-badge.canceled {{
          background: #dc3545;
          color: white;
        }}
        .status-badge.scheduled {{
          background: #667eea;
          color: white;
        }}
        .appointment-details {{
          display: grid;
          gap: 0.5rem;
        }}
        .detail-row {{
          display: flex;
          gap: 0.5rem;
        }}
        .detail-label {{
          font-weight: 600;
          color: #666;
          min-width: 120px;
        }}
        .detail-value {{
          color: #333;
        }}
        .no-appointments {{
          text-align: center;
          padding: 3rem;
          color: #666;
          font-size: 1.2rem;
        }}
        .back-link {{
          display: inline-block;
          margin-top: 2rem;
          padding: 0.75rem 1.5rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          text-decoration: none;
          border-radius: 8px;
          font-weight: 600;
          transition: transform 0.2s;
        }}
        .back-link:hover {{
          transform: translateY(-2px);
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <header>
          <h1>📅 Agenda del Día</h1>
          <p>{d.strftime('%A, %d de %B de %Y')}</p>
        </header>
        
        <div class="stats">
          <div class="stat-card">
            <h3>{total}</h3>
            <p>Total de Turnos</p>
          </div>
          <div class="stat-card" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%);">
            <h3>{attended}</h3>
            <p>Atendidos</p>
          </div>
          <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <h3>{scheduled}</h3>
            <p>Programados</p>
          </div>
          <div class="stat-card" style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);">
            <h3>{canceled}</h3>
            <p>Cancelados</p>
          </div>
        </div>
        
        <div class="appointments-grid">
    """
    
    if appointments:
        for apt in appointments:
            apt_status = str(apt.status)
            status_text = {
                'scheduled': 'Programado',
                'attended': 'Atendido',
                'canceled': 'Cancelado'
            }.get(apt_status, apt_status)
            
            time_str = apt.appointment_date.strftime('%H:%M')
            pet_name = apt.pet.name if apt.pet else 'N/A'
            owner_name = apt.pet.owner.name if apt.pet and apt.pet.owner else 'N/A'
            
            html_content += f"""
          <div class="appointment-card {apt_status}">
            <div class="appointment-header">
              <div class="appointment-time">🕐 {time_str}</div>
              <div class="status-badge {apt_status}">{status_text}</div>
            </div>
            <div class="appointment-details">
              <div class="detail-row">
                <span class="detail-label">🐾 Mascota:</span>
                <span class="detail-value">{pet_name}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">👤 Dueño:</span>
                <span class="detail-value">{owner_name}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">📋 Motivo:</span>
                <span class="detail-value">{apt.reason or 'N/A'}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">🔑 ID:</span>
                <span class="detail-value">#{apt.id}</span>
              </div>
            </div>
          </div>
            """
    else:
        html_content += """
          <div class="no-appointments">
            <p>😴 No hay turnos programados para esta fecha.</p>
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

