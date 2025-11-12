from typing import List, Optional
from datetime import datetime, date as date_type, timedelta
from fastapi import APIRouter, Depends, HTTPException, Form, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.appointment import AppointmentCreate, AppointmentRead

router = APIRouter()


@router.post("/", response_model=AppointmentRead)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    pet = db.get(models.Pet, payload.pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    ap = models.Appointment(
        date=payload.date,
        reason=payload.reason,
        status="scheduled",
        pet_id=payload.pet_id,
    )
    db.add(ap)
    db.commit()
    db.refresh(ap)
    return ap


@router.post("/form", response_class=HTMLResponse)
def create_appointment_form(
    date: datetime = Form(...),
    reason: str = Form(...),
    pet_id: int = Form(...),
    db: Session = Depends(get_db),
):
    """Crear un turno desde formulario HTML y mostrar confirmación."""
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    ap = models.Appointment(
        date=date,
        reason=reason,
        status="scheduled",
        pet_id=pet_id,
    )
    db.add(ap)
    db.commit()
    db.refresh(ap)
    
    # Obtener información relacionada
    owner = pet.owner
    
    # Formatear fecha y hora
    fecha_turno = ap.date.strftime('%d/%m/%Y')
    hora_turno = ap.date.strftime('%H:%M')
    dia_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][ap.date.weekday()]
    
    # Estado del turno en español
    status_text = {
        'scheduled': 'Programado',
        'attended': 'Atendido',
        'canceled': 'Cancelado'
    }.get(ap.status, ap.status)
    
    # Color según estado
    status_color = {
        'scheduled': '#28a745',
        'attended': '#007bff',
        'canceled': '#dc3545'
    }.get(ap.status, '#6c757d')
    
    # Generar HTML de confirmación
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>✅ Turno Agendado - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
        }}
        .container {{
          max-width: 900px;
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
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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
        .appointment-card {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 2.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
          text-align: center;
        }}
        .appointment-date {{
          font-size: 3rem;
          font-weight: 700;
          margin: 0 0 0.5rem;
        }}
        .appointment-time {{
          font-size: 2rem;
          opacity: 0.95;
          margin: 0 0 1rem;
        }}
        .appointment-day {{
          font-size: 1.2rem;
          opacity: 0.9;
          margin: 0 0 1rem;
        }}
        .appointment-id {{
          background: rgba(255, 255, 255, 0.2);
          display: inline-block;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-weight: 600;
        }}
        .info-grid {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1rem;
          margin-bottom: 2rem;
        }}
        .info-card {{
          background: #f8f9fa;
          border-left: 4px solid #f093fb;
          border-radius: 8px;
          padding: 1.5rem;
        }}
        .info-label {{
          font-weight: 700;
          color: #555;
          margin-bottom: 0.5rem;
          font-size: 0.9rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }}
        .info-icon {{
          font-size: 1.3rem;
        }}
        .info-value {{
          color: #333;
          font-size: 1.1rem;
          line-height: 1.6;
        }}
        .status-badge {{
          display: inline-block;
          padding: 0.5rem 1.2rem;
          border-radius: 20px;
          font-weight: 600;
          color: white;
          background: {status_color};
        }}
        .pet-section {{
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          padding: 1.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
        }}
        .pet-section h3 {{
          margin: 0 0 1rem;
          font-size: 1.5rem;
        }}
        .pet-info {{
          display: grid;
          gap: 0.5rem;
        }}
        .owner-section {{
          background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
          color: #333;
          padding: 1.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
        }}
        .owner-section h3 {{
          margin: 0 0 1rem;
          font-size: 1.5rem;
          color: #333;
        }}
        .owner-info {{
          display: grid;
          gap: 0.5rem;
        }}
        .next-steps {{
          background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
          border-radius: 12px;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }}
        .next-steps h3 {{
          margin: 0 0 1rem;
          color: #333;
          font-size: 1.3rem;
        }}
        .step {{
          display: flex;
          align-items: flex-start;
          gap: 1rem;
          margin-bottom: 1rem;
          padding: 1rem;
          background: white;
          border-radius: 8px;
        }}
        .step:last-child {{
          margin-bottom: 0;
        }}
        .step-number {{
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
          width: 32px;
          height: 32px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          flex-shrink: 0;
        }}
        .step-text {{
          flex: 1;
          color: #333;
          line-height: 1.6;
        }}
        .actions {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
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
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-3px);
          box-shadow: 0 6px 20px rgba(240, 147, 251, 0.4);
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
        .reminder {{
          background: #fff3cd;
          border-left: 4px solid #ffc107;
          padding: 1rem 1.5rem;
          border-radius: 8px;
          margin-bottom: 2rem;
        }}
        .reminder-title {{
          font-weight: 700;
          color: #856404;
          margin-bottom: 0.5rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }}
        .reminder-text {{
          color: #856404;
          line-height: 1.6;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="success-icon">📅</div>
          <h1>¡Turno Agendado!</h1>
          <p>El turno se programó exitosamente en el sistema</p>
        </div>
        
        <div class="content">
          <div class="appointment-card">
            <div class="appointment-date">{fecha_turno}</div>
            <div class="appointment-time">🕐 {hora_turno}</div>
            <div class="appointment-day">{dia_semana}</div>
            <span class="appointment-id">Turno #{ap.id}</span>
          </div>
          
          <div class="info-grid">
            <div class="info-card">
              <div class="info-label">
                <span class="info-icon">📝</span>
                Motivo de Consulta
              </div>
              <div class="info-value">{ap.reason}</div>
            </div>
            <div class="info-card">
              <div class="info-label">
                <span class="info-icon">🏷️</span>
                Estado
              </div>
              <div class="info-value">
                <span class="status-badge">{status_text}</span>
              </div>
            </div>
          </div>
          
          <div class="pet-section">
            <h3>🐾 Mascota</h3>
            <div class="pet-info">
              <div><strong>Nombre:</strong> {pet.name}</div>
              <div><strong>Especie:</strong> {pet.species.title()}</div>
              {f'<div><strong>Raza:</strong> {pet.breed}</div>' if pet.breed else ''}
              <div><strong>ID:</strong> #{pet.id}</div>
            </div>
          </div>
          
          <div class="owner-section">
            <h3>👤 Dueño</h3>
            <div class="owner-info">
              <div><strong>Nombre:</strong> {owner.name}</div>
              {f'<div><strong>Teléfono:</strong> {owner.phone}</div>' if owner.phone else ''}
              {f'<div><strong>Email:</strong> {owner.email}</div>' if owner.email else ''}
            </div>
          </div>
          
          <div class="reminder">
            <div class="reminder-title">
              <span>⏰</span>
              Recordatorio Importante
            </div>
            <div class="reminder-text">
              Se recomienda confirmar el turno 24 horas antes de la cita. En caso de no poder asistir, por favor cancelar con anticipación.
            </div>
          </div>
          
          <div class="next-steps">
            <h3>🎯 Próximos Pasos</h3>
            <div class="step">
              <div class="step-number">1</div>
              <div class="step-text">
                <strong>Confirmar asistencia:</strong> Contacta al dueño un día antes para confirmar
              </div>
            </div>
            <div class="step">
              <div class="step-number">2</div>
              <div class="step-text">
                <strong>Preparar historial:</strong> Revisa las atenciones previas de {pet.name}
              </div>
            </div>
            <div class="step">
              <div class="step-number">3</div>
              <div class="step-text">
                <strong>Registrar atención:</strong> Completa el historial clínico después de la consulta
              </div>
            </div>
          </div>
          
          <div class="timestamp">
            <p>📅 Turno creado el {ap.created_at.strftime('%d/%m/%Y a las %H:%M:%S')}</p>
          </div>
          
          <div class="actions">
            <a href="/appointments/{ap.id}/view" class="btn btn-primary" target="_blank">
              👁️ Ver detalles del turno
            </a>
            <a href="/ui" class="btn btn-success">
              ➕ Agendar otro turno
            </a>
            <a href="/ui" class="btn btn-secondary">
              🏠 Ir al inicio
            </a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/", response_model=List[AppointmentRead])
def list_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).order_by(models.Appointment.appointment_date.asc()).all()


# NOTA: Esta ruta /view está deshabilitada porque hay una definición duplicada más completa
# en la línea ~1245 que incluye parámetros de filtro (status, date, pet_id)
# Si se necesita paginación simple, renombrar esta ruta a /view-all o similar
@router.get("/view-all", response_class=HTMLResponse)
def list_appointments_view(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Vista HTML amigable de todos los turnos con paginación."""
    q = db.query(models.Appointment).order_by(models.Appointment.appointment_date.desc())
    total_count = q.count()
    appointments = q.offset((page - 1) * page_size).limit(page_size).all()
    
    total_pages = (total_count + page_size - 1) // page_size
    
    # Generar filas de la tabla
    appointment_rows = ""
    for apt in appointments:
        # Formatear fecha y hora
        fecha_display = apt.appointment_date.strftime('%d/%m/%Y')
        hora_display = apt.appointment_date.strftime('%H:%M')
        dia_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'][apt.appointment_date.weekday()]
        
        # Estado y colores
        status_config = {
            'scheduled': {'text': 'Programado', 'color': '#28a745', 'icon': '📅'},
            'attended': {'text': 'Atendido', 'color': '#007bff', 'icon': '✅'},
            'canceled': {'text': 'Cancelado', 'color': '#dc3545', 'icon': '❌'}
        }
        status_info = status_config.get(apt.status, {'text': apt.status, 'color': '#6c757d', 'icon': '❓'})
        
        pet_name = apt.pet.name if apt.pet else '<span style="color: #999;">-</span>'
        owner_name = apt.pet.owner.name if apt.pet and apt.pet.owner else '<span style="color: #999;">-</span>'
        
        appointment_rows += f"""
        <tr>
            <td style="text-align: center; font-weight: 600;">#{apt.id}</td>
            <td style="text-align: center;">
                <div><strong>{fecha_display}</strong></div>
                <div style="font-size: 0.85rem; color: #666;">{dia_semana} · {hora_display}</div>
            </td>
            <td>{apt.reason}</td>
            <td style="text-align: center;">
                <span style="background: {status_info['color']}; color: white; padding: 0.4rem 0.8rem; border-radius: 12px; font-size: 0.85rem; font-weight: 600; display: inline-block;">
                    {status_info['icon']} {status_info['text']}
                </span>
            </td>
            <td>{pet_name}</td>
            <td>{owner_name}</td>
            <td style="text-align: center;">
                <div style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
                    <a href="/appointments/{apt.id}/view" class="btn-view" target="_blank">👁️ Ver</a>
                    <a href="/appointments/{apt.id}/cancel-form" class="btn-cancel" onclick="return confirm('¿Deseas cancelar este turno? Esta acción quedará registrada en el historial.')">❌ Cancelar</a>
                </div>
            </td>
        </tr>
        """
    
    # Controles de paginación
    pagination = ""
    if total_pages > 1:
        prev_disabled = 'disabled' if page <= 1 else ''
        next_disabled = 'disabled' if page >= total_pages else ''
        prev_page = max(1, page - 1)
        next_page = min(total_pages, page + 1)
        
        pagination = f"""
        <div class="pagination">
            <a href="/appointments/view?page={prev_page}&page_size={page_size}" class="btn-page" {prev_disabled}>← Anterior</a>
            <span class="page-info">Página {page} de {total_pages} | Total: {total_count} turnos</span>
            <a href="/appointments/view?page={next_page}&page_size={page_size}" class="btn-page" {next_disabled}>Siguiente →</a>
        </div>
        """
    else:
        pagination = f'<div class="pagination"><span class="page-info">Total: {total_count} turnos</span></div>'
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>📅 Listado de Turnos - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          min-height: 100vh;
        }}
        .container {{
          max-width: 1600px;
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
        .actions {{
          display: flex;
          gap: 1rem;
          margin-bottom: 2rem;
          flex-wrap: wrap;
        }}
        .btn {{
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 600;
          transition: all 0.2s;
          display: inline-block;
          border: none;
          cursor: pointer;
          font-size: 1rem;
        }}
        .btn-primary {{
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(240, 147, 251, 0.4);
        }}
        .btn-secondary {{
          background: #6c757d;
          color: white;
        }}
        .btn-secondary:hover {{
          background: #5a6268;
          transform: translateY(-2px);
        }}
        .summary {{
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
          padding: 1.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }}
        .summary .count {{
          font-size: 2.5rem;
          font-weight: 700;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
          margin-bottom: 2rem;
          background: white;
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        thead {{
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
        }}
        th {{
          padding: 1rem;
          text-align: left;
          font-weight: 600;
          font-size: 0.95rem;
        }}
        td {{
          padding: 1rem;
          border-bottom: 1px solid #f0f0f0;
        }}
        tbody tr:hover {{
          background: #f8f9fa;
        }}
        tbody tr:last-child td {{
          border-bottom: none;
        }}
        .btn-view {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 6px;
          text-decoration: none;
          font-size: 0.9rem;
          font-weight: 600;
          transition: all 0.2s;
          display: inline-block;
        }}
        .btn-view:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        .btn-cancel {{
          background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 6px;
          text-decoration: none;
          font-size: 0.9rem;
          font-weight: 600;
          transition: all 0.2s;
          display: inline-block;
        }}
        .btn-cancel:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
        }}
        .pagination {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 1rem;
          margin-top: 2rem;
          flex-wrap: wrap;
        }}
        .btn-page {{
          padding: 0.75rem 1.5rem;
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
          text-decoration: none;
          border-radius: 8px;
          font-weight: 600;
          transition: all 0.2s;
        }}
        .btn-page:hover:not([disabled]) {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(240, 147, 251, 0.4);
        }}
        .btn-page[disabled] {{
          background: #ccc;
          cursor: not-allowed;
          pointer-events: none;
        }}
        .page-info {{
          color: #666;
          font-weight: 600;
        }}
        .empty-state {{
          text-align: center;
          padding: 4rem 2rem;
          color: #666;
        }}
        .empty-state .icon {{
          font-size: 4rem;
          margin-bottom: 1rem;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <header>
          <h1>📅 Listado de Turnos</h1>
          <p>Gestión de citas veterinarias</p>
        </header>
        
        <div class="actions">
          <a href="/ui" class="btn btn-primary">➕ Agendar nuevo turno</a>
          <a href="/appointments/search" class="btn btn-secondary">🔍 Búsqueda avanzada</a>
          <a href="/schedule/daily" class="btn btn-secondary">📋 Agenda del día</a>
          <a href="/" class="btn btn-secondary">🏠 Ir al inicio</a>
        </div>
        
        <div class="summary">
          <div>
            <div class="count">{total_count}</div>
            <div>Turnos registrados</div>
          </div>
          <div style="text-align: right;">
            <div>Página {page} de {total_pages}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Mostrando {len(appointments)} registros</div>
          </div>
        </div>
        
        {f'''
        <table>
          <thead>
            <tr>
              <th style="text-align: center;">ID</th>
              <th style="text-align: center;">Fecha y Hora</th>
              <th>Motivo</th>
              <th style="text-align: center;">Estado</th>
              <th>Mascota</th>
              <th>Dueño</th>
              <th style="text-align: center;">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {appointment_rows}
          </tbody>
        </table>
        ''' if appointments else '''
        <div class="empty-state">
          <div class="icon">📅</div>
          <h2>No hay turnos registrados</h2>
          <p>Comienza agendando el primer turno en el sistema</p>
          <a href="/ui" class="btn btn-primary" style="margin-top: 1rem;">➕ Agendar turno</a>
        </div>
        '''}
        
        {pagination}
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/search", response_class=HTMLResponse)
def search_appointments(
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Vista HTML de búsqueda avanzada de turnos con filtros."""
    # Parsear fechas
    start_date = None
    end_date = None
    
    if from_date:
        try:
            start_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        except ValueError:
            pass
    
    if to_date:
        try:
            end_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            pass
    
    # Construir query
    query = db.query(models.Appointment)
    
    # Filtrar por rango de fechas
    if start_date:
        start_datetime = datetime.combine(start_date, datetime.min.time())
        query = query.filter(models.Appointment.appointment_date >= start_datetime)
    
    if end_date:
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(models.Appointment.appointment_date <= end_datetime)
    
    # Filtrar por estado
    if status:
        query = query.filter(models.Appointment.status == status)
    
    appointments = query.order_by(models.Appointment.appointment_date.asc()).all()
    
    # Configuración de vista según filtros
    status_config = {
        'attended': {'name': 'Atendidos', 'color': '#28a745'},
        'scheduled': {'name': 'Programados', 'color': '#667eea'},
        'canceled': {'name': 'Cancelados', 'color': '#dc3545'}
    }
    
    status_info = status_config.get(status or 'all', {'name': 'Todos', 'color': '#667eea'})
    
    # Agrupar por fecha para mejor visualización
    from collections import defaultdict
    appointments_by_date = defaultdict(list)
    for apt in appointments:
        date_key = apt.appointment_date.date()
        appointments_by_date[date_key].append(apt)
    
    # Ordenar fechas
    sorted_dates = sorted(appointments_by_date.keys())
    
    # Generar HTML
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>🔍 Búsqueda Avanzada de Turnos - Veterinaria Inteligente</title>
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
        .filters-summary {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 1rem;
        }}
        .filters-summary .count {{
          font-size: 2.5rem;
          font-weight: 700;
        }}
        .filters-summary .info {{
          flex: 1;
          text-align: right;
        }}
        .toggle-filters {{
          background: rgba(255, 255, 255, 0.3);
          color: white;
          border: 2px solid white;
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          cursor: pointer;
          font-size: 1rem;
          font-weight: 600;
          transition: all 0.3s;
        }}
        .toggle-filters:hover {{
          background: white;
          color: #667eea;
          transform: translateY(-2px);
        }}
        #filters-detail {{
          animation: slideDown 0.3s ease-out;
        }}
        @keyframes slideDown {{
          from {{
            opacity: 0;
            transform: translateY(-10px);
          }}
          to {{
            opacity: 1;
            transform: translateY(0);
          }}
        }}
        .stats-cards {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
          margin-bottom: 2rem;
        }}
        .stat-card {{
          background: #f8f9fa;
          padding: 1.5rem;
          border-radius: 12px;
          text-align: center;
          border-left: 5px solid #667eea;
        }}
        .stat-card.attended {{ border-left-color: #28a745; }}
        .stat-card.scheduled {{ border-left-color: #667eea; }}
        .stat-card.canceled {{ border-left-color: #dc3545; }}
        .stat-card h3 {{
          margin: 0;
          font-size: 2rem;
          color: #333;
        }}
        .stat-card p {{
          margin: 0.5rem 0 0;
          color: #666;
        }}
        .date-group {{
          margin-bottom: 2rem;
        }}
        .date-header {{
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          padding: 1rem 1.5rem;
          border-radius: 8px;
          margin-bottom: 1rem;
          font-size: 1.3rem;
          font-weight: 600;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }}
        .appointments-grid {{
          display: grid;
          gap: 1rem;
          margin-bottom: 1rem;
        }}
        .appointment-card {{
          background: #f8f9fa;
          border-left: 5px solid {status_info['color']};
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
          flex-wrap: wrap;
          gap: 1rem;
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
          gap: 0.75rem;
        }}
        .detail-row {{
          display: grid;
          grid-template-columns: 150px 1fr;
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
          font-size: 1.1rem;
          color: #667eea;
        }}
        .no-results {{
          text-align: center;
          padding: 3rem;
          color: #666;
          font-size: 1.2rem;
        }}
        .no-results-icon {{
          font-size: 4rem;
          margin-bottom: 1rem;
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
          <h1>🔍 Búsqueda Avanzada de Turnos</h1>
          <p>Resultados de la búsqueda</p>
        </header>
        
        <div class="filters-summary">
          <div>
            <div class="count">{len(appointments)}</div>
            <div>turnos encontrados</div>
          </div>
          <div class="info">
            <button class="toggle-filters" onclick="toggleFilters()">
              📋 Ver filtros aplicados
            </button>
            <div id="filters-detail" style="display: none; margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.2); border-radius: 8px; text-align: left;">
              <strong style="display: block; margin-bottom: 0.5rem;">Filtros aplicados:</strong>
              {'<p style="margin: 0.25rem 0;">📅 Desde: ' + start_date.strftime('%d/%m/%Y') + '</p>' if start_date else '<p style="margin: 0.25rem 0; opacity: 0.7;">📅 Desde: Sin filtro</p>'}
              {'<p style="margin: 0.25rem 0;">📅 Hasta: ' + end_date.strftime('%d/%m/%Y') + '</p>' if end_date else '<p style="margin: 0.25rem 0; opacity: 0.7;">📅 Hasta: Sin filtro</p>'}
              {'<p style="margin: 0.25rem 0;">📊 Estado: ' + status_info['name'] + '</p>' if status else '<p style="margin: 0.25rem 0; opacity: 0.7;">📊 Estado: Todos</p>'}
            </div>
          </div>
        </div>
        
        <script>
          function toggleFilters() {{
            const detail = document.getElementById('filters-detail');
            const btn = document.querySelector('.toggle-filters');
            if (detail.style.display === 'none') {{
              detail.style.display = 'block';
              btn.textContent = '📋 Ocultar filtros';
            }} else {{
              detail.style.display = 'none';
              btn.textContent = '📋 Ver filtros aplicados';
            }}
          }}
        </script>
        
        <div class="stats-cards">
          <div class="stat-card attended">
            <h3>{sum(1 for a in appointments if str(a.status) == 'attended')}</h3>
            <p>Atendidos</p>
          </div>
          <div class="stat-card scheduled">
            <h3>{sum(1 for a in appointments if str(a.status) == 'scheduled')}</h3>
            <p>Programados</p>
          </div>
          <div class="stat-card canceled">
            <h3>{sum(1 for a in appointments if str(a.status) == 'canceled')}</h3>
            <p>Cancelados</p>
          </div>
        </div>
    """
    
    if appointments:
        for date_key in sorted_dates:
            date_appointments = appointments_by_date[date_key]
            weekday = date_key.strftime('%A')
            weekday_es = {
                'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
                'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
            }.get(weekday, weekday)
            
            html_content += f"""
        <div class="date-group">
          <div class="date-header">
            <span>📅 {weekday_es}, {date_key.strftime('%d de %B de %Y')}</span>
            <span>{len(date_appointments)} turnos</span>
          </div>
          <div class="appointments-grid">
            """
            
            for apt in date_appointments:
                apt_status = str(apt.status)
                status_text = {
                    'scheduled': 'Programado',
                    'attended': 'Atendido',
                    'canceled': 'Cancelado'
                }.get(apt_status, apt_status)
                
                time_str = apt.appointment_date.strftime('%H:%M')
                pet_name = apt.pet.name if apt.pet else 'N/A'
                owner_name = apt.pet.owner.name if apt.pet and apt.pet.owner else 'N/A'
                owner_phone = apt.pet.owner.phone if apt.pet and apt.pet.owner else 'N/A'
                pet_species = apt.pet.species if apt.pet else 'N/A'
                pet_breed = apt.pet.breed if apt.pet else 'N/A'
                
                html_content += f"""
            <div class="appointment-card {apt_status}">
              <div class="appointment-header">
                <div class="appointment-time">🕐 {time_str}</div>
                <div class="status-badge {apt_status}">{status_text}</div>
              </div>
              <div class="appointment-details">
                <div class="detail-row">
                  <span class="detail-label">🐾 Mascota:</span>
                  <span class="detail-value highlight">{pet_name}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">🔍 Especie/Raza:</span>
                  <span class="detail-value">{pet_species} - {pet_breed}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">👤 Dueño:</span>
                  <span class="detail-value">{owner_name}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">📞 Teléfono:</span>
                  <span class="detail-value">{owner_phone}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">📋 Motivo:</span>
                  <span class="detail-value">{apt.reason or 'No especificado'}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">🔑 ID:</span>
                  <span class="detail-value">#{apt.id}</span>
                </div>
              </div>
            </div>
                """
            
            html_content += """
          </div>
        </div>
            """
    else:
        html_content += """
        <div class="no-results">
          <div class="no-results-icon">🔍</div>
          <p>No se encontraron turnos con los filtros seleccionados.</p>
          <p style="font-size: 1rem; color: #999;">Intenta ajustar los criterios de búsqueda.</p>
        </div>
        """
    
    html_content += """
        <div style="text-align: center;">
          <a href="/vet/gestion" class="back-link">⬅️ Volver a Gestión Veterinaria</a>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/view", response_class=HTMLResponse)
def view_appointments(
    pet_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Vista HTML de turnos filtrados por mascota, estado y/o fecha."""
    # Obtener información de la mascota si se proporciona pet_id
    pet = None
    if pet_id:
        pet = db.get(models.Pet, pet_id)
        if not pet:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
    
    # Parsear fecha
    target_date = None
    if date:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            pass
    
    # Construir query
    query = db.query(models.Appointment)
    
    # Filtrar por mascota si se proporciona
    if pet_id:
        query = query.filter(models.Appointment.pet_id == pet_id)
    
    # Filtrar por fecha si se proporciona
    if target_date:
        start = datetime.combine(target_date, datetime.min.time())
        end = start + timedelta(days=1)
        query = query.filter(
            models.Appointment.appointment_date >= start,
            models.Appointment.appointment_date < end
        )
    
    # Filtrar por estado si se proporciona
    if status:
        query = query.filter(models.Appointment.status == status)
    
    appointments = query.order_by(models.Appointment.appointment_date.asc()).all()
    
    # Definir títulos y colores según el contexto
    if pet:
        # Emoji de especie
        species_lower = pet.species.lower()
        if 'perro' in species_lower or 'dog' in species_lower:
            species_emoji = '🐕'
        elif 'gato' in species_lower or 'cat' in species_lower:
            species_emoji = '🐈'
        else:
            species_emoji = '🐾'
        
        title = f'📅 Turnos de {pet.name}'
        subtitle = f'{species_emoji} {pet.species} | Dueño: {pet.owner.name if pet.owner else "N/A"}'
        color = '#667eea'
        gradient = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    else:
        # Definir títulos y colores según el estado
        status_config = {
            'attended': {
                'title': '✅ Turnos Atendidos',
                'color': '#28a745',
                'gradient': 'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'text': 'Atendido'
            },
            'scheduled': {
                'title': '⏳ Turnos Programados',
                'color': '#667eea',
                'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'text': 'Programado'
            },
            'canceled': {
                'title': '❌ Turnos Cancelados',
                'color': '#dc3545',
                'gradient': 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)',
                'text': 'Cancelado'
            }
        }
        
        config = status_config.get(status or 'all', {
            'title': '📋 Todos los Turnos',
            'color': '#667eea',
            'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'text': 'Turno'
        })
        
        title = config['title']
        subtitle = target_date.strftime('%d/%m/%Y') if target_date else 'Todas las fechas'
        color = config['color']
        gradient = config['gradient']
    
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
        .appointments-grid {{
          display: grid;
          gap: 1rem;
        }}
        .appointment-card {{
          background: #f8f9fa;
          border-left: 5px solid {color};
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          transition: transform 0.2s, box-shadow 0.2s;
        }}
        .appointment-card:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}
        .appointment-header {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
          flex-wrap: wrap;
          gap: 1rem;
        }}
        .appointment-datetime {{
          display: flex;
          gap: 1rem;
          align-items: center;
        }}
        .appointment-time {{
          font-size: 1.5rem;
          font-weight: 700;
          color: #333;
        }}
        .appointment-date {{
          font-size: 1rem;
          color: #666;
          font-weight: 500;
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
        .status-badge.scheduled {{
          background: #667eea;
          color: white;
        }}
        .status-badge.canceled {{
          background: #dc3545;
          color: white;
        }}
        .appointment-details {{
          display: grid;
          gap: 0.75rem;
        }}
        .detail-row {{
          display: grid;
          grid-template-columns: 150px 1fr;
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
        .no-appointments {{
          text-align: center;
          padding: 3rem;
          color: #666;
          font-size: 1.2rem;
        }}
        .no-appointments-icon {{
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
          <h2>{len(appointments)}</h2>
          <p>turnos encontrados</p>
        </div>
        
        <div class="appointments-grid">
    """
    
    if appointments:
        for apt in appointments:
            time_str = apt.appointment_date.strftime('%H:%M')
            date_full = apt.appointment_date.strftime('%d/%m/%Y')
            pet_name = apt.pet.name if apt.pet else 'N/A'
            owner_name = apt.pet.owner.name if apt.pet and apt.pet.owner else 'N/A'
            owner_phone = apt.pet.owner.phone if apt.pet and apt.pet.owner else 'N/A'
            pet_species = apt.pet.species if apt.pet else 'N/A'
            pet_breed = apt.pet.breed if apt.pet else 'N/A'
            
            # Calcular estado del turno
            today = datetime.now().date()
            apt_date = apt.appointment_date.date()
            
            if apt.status == 'attended':
                status_class = "attended"
                status_text = "✓ Atendido"
            elif apt.status == 'canceled':
                status_class = "canceled"
                status_text = "✗ Cancelado"
            elif apt_date >= today:
                status_class = "scheduled"
                status_text = "◷ Programado"
            else:
                status_class = "scheduled"
                status_text = "◷ Pendiente"
            
            html_content += f"""
          <div class="appointment-card">
            <div class="appointment-header">
              <div class="appointment-datetime">
                <div class="appointment-time">🕐 {time_str}</div>
                <div class="appointment-date">📅 {date_full}</div>
              </div>
              <div class="status-badge {status_class}">{status_text}</div>
            </div>
            <div class="appointment-details">
              <div class="detail-row">
                <span class="detail-label">🐾 Mascota:</span>
                <span class="detail-value highlight">{pet_name}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">🔍 Especie/Raza:</span>
                <span class="detail-value">{pet_species} - {pet_breed}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">👤 Dueño:</span>
                <span class="detail-value">{owner_name}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">📞 Teléfono:</span>
                <span class="detail-value">{owner_phone}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">📋 Motivo:</span>
                <span class="detail-value">{apt.reason or 'No especificado'}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">🔑 ID Turno:</span>
                <span class="detail-value">#{apt.id}</span>
              </div>
            </div>
          </div>
            """
    else:
        html_content += """
          <div class="no-appointments">
            <div class="no-appointments-icon">😴</div>
            <p>No se encontraron turnos con los filtros seleccionados.</p>
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


@router.get("/{appointment_id}/view", response_class=HTMLResponse)
def view_appointment_detail(appointment_id: int, db: Session = Depends(get_db)):
    """Ver detalles completos de un turno."""
    apt = db.get(models.Appointment, appointment_id)
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Formatear fecha y hora
    fecha_turno = apt.appointment_date.strftime('%d/%m/%Y')
    hora_turno = apt.appointment_date.strftime('%H:%M')
    dia_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][apt.appointment_date.weekday()]
    
    # Estado del turno en español
    status_text = {
        'scheduled': 'Programado',
        'attended': 'Atendido',
        'canceled': 'Cancelado'
    }.get(apt.status, apt.status)  # type: ignore
    
    # Color según estado
    status_color = {
        'scheduled': '#28a745',
        'attended': '#007bff',
        'canceled': '#dc3545'
    }.get(apt.status, '#6c757d')  # type: ignore
    
    # Emoji según estado
    status_emoji = {
        'scheduled': '📅',
        'attended': '✅',
        'canceled': '❌'
    }.get(apt.status, '📋')  # type: ignore
    
    # Información de la mascota y dueño
    pet_name = apt.pet.name if apt.pet else 'N/A'
    pet_species = apt.pet.species if apt.pet else 'N/A'
    pet_breed = apt.pet.breed if apt.pet and apt.pet.breed else 'N/A'
    owner_name = apt.pet.owner.name if apt.pet and apt.pet.owner else 'N/A'
    owner_phone = apt.pet.owner.phone if apt.pet and apt.pet.owner else 'N/A'
    
    # Emoji según especie
    species_emoji = {
        'perro': '🐕',
        'gato': '🐈',
        'ave': '🦜',
        'conejo': '🐰',
        'hamster': '🐹',
        'otro': '🐾'
    }.get(pet_species.lower() if pet_species != 'N/A' else 'otro', '🐾')
    
    # Notas (incluye info de cancelación si aplica)
    notes_html = f"<p>{apt.notes}</p>" if apt.notes else "<p style='color: #888;'><em>Sin notas adicionales</em></p>"
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>👁️ Detalles del Turno #{apt.id} - Veterinaria Inteligente</title>
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
          max-width: 900px;
          margin: 0 auto;
          background: #fff;
          border-radius: 20px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.3);
          overflow: hidden;
          animation: slideIn 0.5s ease-out;
        }}
        @keyframes slideIn {{
          from {{ opacity: 0; transform: translateY(-30px); }}
          to {{ opacity: 1; transform: translateY(0); }}
        }}
        .header {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 2.5rem;
          text-align: center;
        }}
        .header h1 {{
          margin: 0;
          font-size: 2.5rem;
          font-weight: bold;
          text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        .header p {{
          margin: 0.5rem 0 0 0;
          font-size: 1.1rem;
          opacity: 0.95;
        }}
        .content {{
          padding: 2.5rem;
        }}
        .status-badge {{
          display: inline-block;
          padding: 0.75rem 1.5rem;
          border-radius: 50px;
          font-weight: bold;
          font-size: 1.1rem;
          margin-bottom: 2rem;
          background: {status_color};
          color: white;
          box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .info-section {{
          margin-bottom: 2rem;
          padding: 1.5rem;
          background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
          border-radius: 15px;
          box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }}
        .info-section h2 {{
          margin: 0 0 1rem 0;
          color: #333;
          font-size: 1.5rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }}
        .info-grid {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1rem;
        }}
        .info-item {{
          background: white;
          padding: 1rem;
          border-radius: 10px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .info-item strong {{
          display: block;
          color: #667eea;
          font-size: 0.9rem;
          margin-bottom: 0.3rem;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }}
        .info-item span {{
          display: block;
          color: #333;
          font-size: 1.1rem;
          font-weight: 500;
        }}
        .notes-section {{
          background: #fffbea;
          border-left: 5px solid #f39c12;
          padding: 1.5rem;
          border-radius: 10px;
          margin-top: 1.5rem;
        }}
        .notes-section h3 {{
          margin: 0 0 1rem 0;
          color: #f39c12;
          font-size: 1.2rem;
        }}
        .buttons {{
          display: flex;
          gap: 1rem;
          justify-content: center;
          margin-top: 2.5rem;
          flex-wrap: wrap;
        }}
        .btn {{
          display: inline-block;
          padding: 1rem 2rem;
          border-radius: 50px;
          text-decoration: none;
          font-weight: bold;
          font-size: 1rem;
          transition: all 0.3s ease;
          box-shadow: 0 4px 15px rgba(0,0,0,0.2);
          text-align: center;
        }}
        .btn-primary {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-3px);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        .btn-secondary {{
          background: linear-gradient(135deg, #868f96 0%, #596164 100%);
          color: white;
        }}
        .btn-secondary:hover {{
          transform: translateY(-3px);
          box-shadow: 0 6px 20px rgba(134, 143, 150, 0.4);
        }}
        .btn-danger {{
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
        }}
        .btn-danger:hover {{
          transform: translateY(-3px);
          box-shadow: 0 6px 20px rgba(245, 87, 108, 0.4);
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>👁️ Detalles del Turno</h1>
          <p>Turno #{apt.id}</p>
        </div>
        
        <div class="content">
          <div style="text-align: center;">
            <span class="status-badge">{status_emoji} {status_text}</span>
          </div>
          
          <div class="info-section">
            <h2>📅 Información del Turno</h2>
            <div class="info-grid">
              <div class="info-item">
                <strong>📆 Fecha</strong>
                <span>{dia_semana}, {fecha_turno}</span>
              </div>
              <div class="info-item">
                <strong>🕐 Hora</strong>
                <span>{hora_turno}</span>
              </div>
              <div class="info-item">
                <strong>📋 Motivo</strong>
                <span>{apt.reason}</span>
              </div>
              <div class="info-item">
                <strong>🏷️ Estado</strong>
                <span style="color: {status_color};">{status_text}</span>
              </div>
            </div>
          </div>
          
          <div class="info-section">
            <h2>{species_emoji} Información de la Mascota</h2>
            <div class="info-grid">
              <div class="info-item">
                <strong>🐾 Nombre</strong>
                <span>{pet_name}</span>
              </div>
              <div class="info-item">
                <strong>🦴 Especie</strong>
                <span>{pet_species}</span>
              </div>
              <div class="info-item">
                <strong>🎯 Raza</strong>
                <span>{pet_breed}</span>
              </div>
            </div>
          </div>
          
          <div class="info-section">
            <h2>👤 Información del Dueño</h2>
            <div class="info-grid">
              <div class="info-item">
                <strong>👨 Nombre</strong>
                <span>{owner_name}</span>
              </div>
              <div class="info-item">
                <strong>📞 Teléfono</strong>
                <span>{owner_phone}</span>
              </div>
            </div>
          </div>
          
          <div class="notes-section">
            <h3>📝 Notas y Observaciones</h3>
            {notes_html}
          </div>
          
          <div class="buttons">
            <a href="/appointments/view" class="btn btn-secondary">⬅️ Volver al Listado</a>
    """
    
    # Agregar botón de cancelar solo si el turno está programado
    if apt.status == 'scheduled':  # type: ignore
        html_content += f"""
            <a href="/appointments/{apt.id}/cancel-form" class="btn btn-danger">❌ Cancelar Turno</a>
        """
    
    html_content += """
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.post("/{appointment_id}/cancel", response_model=AppointmentRead)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    ap = db.get(models.Appointment, appointment_id)
    if not ap:
        raise HTTPException(status_code=404, detail="Appointment not found")
    setattr(ap, 'status', 'canceled')  # type: ignore
    db.commit()
    db.refresh(ap)
    return ap


@router.get("/{appointment_id}/cancel-form", response_class=HTMLResponse)
def cancel_appointment_form(appointment_id: int, db: Session = Depends(get_db)):
    """Formulario para cancelar un turno con motivo de cancelación."""
    apt = db.get(models.Appointment, appointment_id)
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if apt.status == 'canceled':  # type: ignore
        raise HTTPException(status_code=400, detail="Este turno ya está cancelado")
    
    # Formatear fecha y hora
    fecha_turno = apt.appointment_date.strftime('%d/%m/%Y')
    hora_turno = apt.appointment_date.strftime('%H:%M')
    dia_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][apt.appointment_date.weekday()]
    
    pet_name = apt.pet.name if apt.pet else 'N/A'
    owner_name = apt.pet.owner.name if apt.pet and apt.pet.owner else 'N/A'
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>❌ Cancelar Turno - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
        }}
        .container {{
          max-width: 700px;
          width: 100%;
          background: #fff;
          border-radius: 20px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.3);
          overflow: hidden;
        }}
        .header {{
          background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
          color: white;
          padding: 2rem;
          text-align: center;
        }}
        .header h1 {{
          margin: 0 0 0.5rem;
          font-size: 2rem;
          font-weight: 700;
        }}
        .header p {{
          margin: 0;
          opacity: 0.95;
        }}
        .content {{
          padding: 2rem;
        }}
        .appointment-card {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
        }}
        .appointment-header {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }}
        .appointment-date {{
          font-size: 1.8rem;
          font-weight: 700;
        }}
        .appointment-time {{
          font-size: 1.3rem;
          opacity: 0.95;
        }}
        .appointment-details {{
          display: grid;
          gap: 0.5rem;
          padding-top: 1rem;
          border-top: 1px solid rgba(255,255,255,0.3);
        }}
        .form-group {{
          margin-bottom: 1.5rem;
        }}
        label {{
          display: block;
          font-weight: 600;
          margin-bottom: 0.5rem;
          color: #333;
        }}
        select,
        textarea {{
          width: 100%;
          padding: 0.75rem;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 1rem;
          transition: border-color 0.3s;
          font-family: inherit;
        }}
        textarea {{
          min-height: 100px;
          resize: vertical;
        }}
        select:focus,
        textarea:focus {{
          outline: none;
          border-color: #e74c3c;
        }}
        .required {{
          color: #e74c3c;
        }}
        .warning-box {{
          background: #fff3cd;
          border-left: 4px solid #f39c12;
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 1.5rem;
        }}
        .warning-box p {{
          margin: 0;
          color: #856404;
        }}
        .actions {{
          display: flex;
          gap: 1rem;
          margin-top: 2rem;
        }}
        .btn {{
          flex: 1;
          padding: 0.75rem;
          border-radius: 8px;
          font-weight: 600;
          font-size: 1rem;
          border: none;
          cursor: pointer;
          transition: all 0.2s;
          text-decoration: none;
          text-align: center;
        }}
        .btn-danger {{
          background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
          color: white;
        }}
        .btn-danger:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
        }}
        .btn-secondary {{
          background: #6c757d;
          color: white;
        }}
        .btn-secondary:hover {{
          background: #5a6268;
          transform: translateY(-2px);
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>❌ Cancelar Turno</h1>
          <p>ID: #{apt.id}</p>
        </div>
        
        <div class="content">
          <div class="appointment-card">
            <div class="appointment-header">
              <div class="appointment-date">📅 {fecha_turno}</div>
              <div class="appointment-time">🕐 {hora_turno}</div>
            </div>
            <div>{dia_semana}</div>
            <div class="appointment-details">
              <div><strong>🐾 Mascota:</strong> {pet_name}</div>
              <div><strong>👤 Dueño:</strong> {owner_name}</div>
              <div><strong>📋 Motivo:</strong> {apt.reason}</div>
            </div>
          </div>
          
          <div class="warning-box">
            <p><strong>⚠️ Importante:</strong> Esta acción quedará registrada en el historial de cancelaciones. El motivo ayudará a generar reportes precisos.</p>
          </div>
          
          <form method="POST" action="/appointments/{apt.id}/cancel-confirm">
            <div class="form-group">
              <label>Motivo de Cancelación <span class="required">*</span></label>
              <select name="cancellation_reason" required>
                <option value="">Selecciona un motivo...</option>
                <option value="paciente_no_asistio">Paciente no asistió (No-show)</option>
                <option value="solicitud_dueno">Solicitud del dueño</option>
                <option value="emergencia_dueno">Emergencia del dueño</option>
                <option value="mascota_mejor">Mascota mejoró</option>
                <option value="clima">Problemas climáticos</option>
                <option value="transporte">Problemas de transporte</option>
                <option value="reprogramado">Turno reprogramado</option>
                <option value="otro">Otro motivo</option>
              </select>
            </div>
            
            <div class="form-group">
              <label>Observaciones Adicionales</label>
              <textarea name="cancellation_notes" placeholder="Información adicional sobre la cancelación..."></textarea>
            </div>
            
            <div class="actions">
              <button type="submit" class="btn btn-danger">❌ Confirmar Cancelación</button>
              <a href="/appointments/view" class="btn btn-secondary">⬅️ Volver</a>
            </div>
          </form>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.post("/{appointment_id}/cancel-confirm", response_class=HTMLResponse)
def cancel_appointment_confirm(
    appointment_id: int,
    cancellation_reason: str = Form(...),
    cancellation_notes: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """Confirmar cancelación de turno y registrar en historial."""
    apt = db.get(models.Appointment, appointment_id)
    if not apt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if apt.status == 'canceled':  # type: ignore
        raise HTTPException(status_code=400, detail="Este turno ya está cancelado")
    
    # Formatear fecha y hora
    fecha_turno = apt.appointment_date.strftime('%d/%m/%Y')
    hora_turno = apt.appointment_date.strftime('%H:%M')
    
    pet_name = apt.pet.name if apt.pet else 'N/A'
    owner_name = apt.pet.owner.name if apt.pet and apt.pet.owner else 'N/A'
    owner_phone = apt.pet.owner.phone if apt.pet and apt.pet.owner else 'N/A'
    
    # Mapear motivos a texto legible
    reason_map = {
        'paciente_no_asistio': 'Paciente no asistió (No-show)',
        'solicitud_dueno': 'Solicitud del dueño',
        'emergencia_dueno': 'Emergencia del dueño',
        'mascota_mejor': 'Mascota mejoró',
        'clima': 'Problemas climáticos',
        'transporte': 'Problemas de transporte',
        'reprogramado': 'Turno reprogramado',
        'otro': 'Otro motivo'
    }
    reason_text = reason_map.get(cancellation_reason, cancellation_reason)
    
    # Actualizar estado y agregar nota de cancelación
    apt.status = 'canceled'  # type: ignore
    
    # Agregar motivo de cancelación a las notas
    cancel_record = f"[CANCELADO] {reason_text}"
    if cancellation_notes:
        cancel_record += f": {cancellation_notes}"
    
    if apt.notes:  # type: ignore
        apt.notes = f"{apt.notes}\n\n{cancel_record}"  # type: ignore
    else:
        apt.notes = cancel_record  # type: ignore
    
    db.commit()
    db.refresh(apt)
    
    # Página de confirmación
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>✅ Turno Cancelado - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
        }}
        .container {{
          max-width: 700px;
          width: 100%;
          background: #fff;
          border-radius: 20px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.3);
          overflow: hidden;
          animation: slideIn 0.5s ease-out;
        }}
        @keyframes slideIn {{
          from {{ opacity: 0; transform: translateY(-30px); }}
          to {{ opacity: 1; transform: translateY(0); }}
        }}
        .header {{
          background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
          color: white;
          padding: 3rem 2rem;
          text-align: center;
        }}
        .icon {{
          font-size: 5rem;
          margin-bottom: 1rem;
        }}
        .header h1 {{
          margin: 0 0 0.5rem;
          font-size: 2.5rem;
          font-weight: 700;
        }}
        .content {{
          padding: 2rem;
        }}
        .info-box {{
          background: #f8f9fa;
          border-radius: 12px;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }}
        .info-box h3 {{
          margin: 0 0 1rem;
          color: #333;
        }}
        .info-row {{
          padding: 0.75rem;
          background: white;
          border-radius: 8px;
          margin-bottom: 0.5rem;
          display: flex;
          justify-content: space-between;
        }}
        .info-row:last-child {{ margin-bottom: 0; }}
        .reason-box {{
          background: #fff3cd;
          border-left: 4px solid #f39c12;
          padding: 1.5rem;
          border-radius: 8px;
          margin-bottom: 2rem;
        }}
        .reason-box h3 {{
          margin: 0 0 0.75rem;
          color: #856404;
        }}
        .reason-box p {{
          margin: 0;
          color: #856404;
        }}
        .note-box {{
          background: #e7f3ff;
          border-left: 4px solid #2196f3;
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 2rem;
        }}
        .note-box strong {{
          color: #1976d2;
        }}
        .note-box p {{
          margin: 0.5rem 0 0;
          color: #0d47a1;
        }}
        .actions {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
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
        }}
        .btn-primary {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-3px);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        .btn-secondary {{
          background: #6c757d;
          color: white;
        }}
        .btn-secondary:hover {{
          background: #5a6268;
          transform: translateY(-3px);
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="icon">❌</div>
          <h1>Turno Cancelado</h1>
          <p>La cancelación se registró correctamente</p>
        </div>
        
        <div class="content">
          <div class="info-box">
            <h3>📋 Información del Turno Cancelado</h3>
            <div class="info-row">
              <strong>ID:</strong>
              <span>#{apt.id}</span>
            </div>
            <div class="info-row">
              <strong>Fecha:</strong>
              <span>{fecha_turno} a las {hora_turno}</span>
            </div>
            <div class="info-row">
              <strong>Mascota:</strong>
              <span>{pet_name}</span>
            </div>
            <div class="info-row">
              <strong>Dueño:</strong>
              <span>{owner_name}</span>
            </div>
            <div class="info-row">
              <strong>Teléfono:</strong>
              <span>{owner_phone}</span>
            </div>
          </div>
          
          <div class="reason-box">
            <h3>📝 Motivo de Cancelación</h3>
            <p><strong>{reason_text}</strong></p>
            {f'<p style="margin-top: 0.5rem; font-style: italic;">{cancellation_notes}</p>' if cancellation_notes else ''}
          </div>
          
          <div class="note-box">
            <strong>📊 Registro en Historial</strong>
            <p>Esta cancelación quedó registrada y será considerada en los reportes de gestión y análisis predictivo de no-show.</p>
          </div>
          
          <div class="actions">
            <a href="/appointments/view" class="btn btn-primary">📋 Ver todos los turnos</a>
            <a href="/schedule/daily" class="btn btn-secondary">📅 Agenda del día</a>
            <a href="/ui" class="btn btn-secondary">🏠 Ir al inicio</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content
