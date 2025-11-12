from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

from app.db.database import Base, engine, get_db
from app.db import models

router = APIRouter()


@router.post("/__admin/reset-db")
def reset_db(db: Session = Depends(get_db)):
    try:
        # Cerrar conexiones de la sesión actual
        db.close()
    except Exception:
        pass
    # Dropear y recrear tablas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"status": "ok", "message": "database reset"}


@router.get("/admin/db_counts", tags=["admin"])
def db_counts(db: Session = Depends(get_db)):
    owners = db.query(models.Owner).count()
    pets = db.query(models.Pet).count()
    appts = db.query(models.Appointment).count()
    vaccs = db.query(models.Vaccination).count()
    return {
        "owners": owners,
        "pets": pets,
        "appointments": appts,
        "vaccinations": vaccs,
    }


@router.get("/admin/db_counts_form", response_class=HTMLResponse, tags=["admin"])
def db_counts_form(db: Session = Depends(get_db)):
        """Página amigable que muestra totales del sistema."""
        owners = db.query(models.Owner).count()
        pets = db.query(models.Pet).count()
        appts = db.query(models.Appointment).count()
        appts_scheduled = db.query(models.Appointment).filter(models.Appointment.status == "scheduled").count()
        appts_attended = db.query(models.Appointment).filter(models.Appointment.status == "attended").count()
        appts_canceled = db.query(models.Appointment).filter(models.Appointment.status == "canceled").count()
        vaccs = db.query(models.Vaccination).count()
        records = db.query(models.ClinicalRecord).count()

        html = f"""
        <!doctype html>
        <html lang="es">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>📊 Estadísticas del Sistema - Veterinaria Inteligente</title>
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    height: 100vh;
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                }}
                .container {{
                    display: flex;
                    flex-direction: column;
                    height: 100vh;
                }}
                .header {{
                    background: rgba(255,255,255,0.98);
                    border-bottom: 3px solid #667eea;
                    padding: 0.8rem 1.5rem;
                    text-align: center;
                    flex-shrink: 0;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 1.5rem;
                    color: #333;
                    font-weight: 700;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                }}
                .header p {{
                    margin: 0.3rem 0 0 0;
                    font-size: 0.8rem;
                    color: #666;
                }}
                .info-banner {{
                    background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
                    border-bottom: 2px solid #f39c12;
                    padding: 0.7rem 1.5rem;
                    text-align: center;
                    flex-shrink: 0;
                }}
                .info-banner p {{
                    margin: 0;
                    color: #333;
                    font-size: 0.8rem;
                    line-height: 1.4;
                }}
                .info-banner strong {{
                    color: #d35400;
                }}
                .main-content {{
                    flex: 1;
                    overflow-y: auto;
                    padding: 1rem 1.5rem 1rem;
                    background: rgba(255,255,255,0.95);
                }}
                .content-wrapper {{
                    max-width: 1400px;
                    margin: 0 auto;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 1rem;
                    margin-bottom: 1rem;
                }}
                .stat-card {{
                    background: #fff;
                    border-radius: 12px;
                    padding: 1.2rem;
                    text-align: center;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    transition: all 0.3s ease;
                    position: relative;
                    overflow: hidden;
                    border: 2px solid #e0e0e0;
                }}
                .stat-card:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
                    border-color: var(--card-color);
                }}
                .stat-card::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: var(--card-color);
                }}
                .stat-card.owners {{ --card-color: #667eea; }}
                .stat-card.pets {{ --card-color: #38ef7d; }}
                .stat-card.appointments {{ --card-color: #fa709a; }}
                .stat-card.vaccinations {{ --card-color: #30cfd0; }}
                .stat-card.records {{ --card-color: #f5576c; }}
                .stat-icon {{
                    font-size: 2.5rem;
                    margin-bottom: 0.5rem;
                    display: block;
                }}
                .stat-number {{
                    font-size: 2.5rem;
                    font-weight: bold;
                    color: #333;
                    margin: 0.3rem 0;
                    display: block;
                }}
                .stat-label {{
                    font-size: 0.85rem;
                    color: #666;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    font-weight: 600;
                }}
                .detail-section {{
                    background: #fff;
                    border-radius: 12px;
                    padding: 1.2rem;
                    margin-top: 1rem;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    border: 2px solid #e0e0e0;
                }}
                .detail-section h2 {{
                    margin: 0 0 1rem 0;
                    color: #333;
                    font-size: 1.1rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 0.5rem;
                }}
                .mini-stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 0.8rem;
                }}
                .mini-stat {{
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    padding: 0.8rem;
                    border-radius: 8px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                    border-left: 4px solid var(--mini-color);
                }}
                .mini-stat.scheduled {{ --mini-color: #28a745; }}
                .mini-stat.attended {{ --mini-color: #007bff; }}
                .mini-stat.canceled {{ --mini-color: #dc3545; }}
                .mini-stat-label {{
                    color: #555;
                    font-size: 0.85rem;
                    font-weight: 600;
                }}
                .mini-stat-value {{
                    font-size: 1.8rem;
                    font-weight: bold;
                    color: #333;
                }}
                .footer {{
                    background: rgba(255,255,255,0.98);
                    border-top: 3px solid #667eea;
                    padding: 0.8rem 1.5rem;
                    flex-shrink: 0;
                    display: flex;
                    justify-content: center;
                    gap: 0.8rem;
                    flex-wrap: wrap;
                    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
                }}
                .btn {{
                    display: inline-block;
                    padding: 0.6rem 1.3rem;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 700;
                    font-size: 0.8rem;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                    border: none;
                    cursor: pointer;
                    white-space: nowrap;
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
                    background: linear-gradient(135deg, #868f96 0%, #596164 100%);
                    color: white;
                }}
                .btn-secondary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(134, 143, 150, 0.4);
                }}
                .btn-success {{
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    color: white;
                }}
                .btn-success:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
                }}
                ::-webkit-scrollbar {{
                    width: 8px;
                }}
                ::-webkit-scrollbar-track {{
                    background: #f1f1f1;
                    border-radius: 4px;
                }}
                ::-webkit-scrollbar-thumb {{
                    background: #667eea;
                    border-radius: 4px;
                }}
                ::-webkit-scrollbar-thumb:hover {{
                    background: #764ba2;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Estadísticas del Sistema</h1>
                    <p>Resumen completo de toda la información registrada</p>
                </div>
                
                <div class="info-banner">
                    <p>💡 <strong>Información en tiempo real:</strong> Estos números muestran el total de registros actuales en el sistema. Presioná "🔄 Actualizar Datos" para refrescar la información.</p>
                </div>
                
                <div class="main-content">
                    <div class="content-wrapper">
                        <div class="stats-grid">
                            <div class="stat-card owners">
                                <span class="stat-icon">👥</span>
                                <span class="stat-number">{owners}</span>
                                <span class="stat-label">Dueños Registrados</span>
                            </div>
                            
                            <div class="stat-card pets">
                                <span class="stat-icon">🐾</span>
                                <span class="stat-number">{pets}</span>
                                <span class="stat-label">Mascotas Registradas</span>
                            </div>
                            
                            <div class="stat-card appointments">
                                <span class="stat-icon">📅</span>
                                <span class="stat-number">{appts}</span>
                                <span class="stat-label">Turnos Totales</span>
                            </div>
                            
                            <div class="stat-card vaccinations">
                                <span class="stat-icon">💉</span>
                                <span class="stat-number">{vaccs}</span>
                                <span class="stat-label">Vacunaciones Aplicadas</span>
                            </div>
                            
                            <div class="stat-card records">
                                <span class="stat-icon">📋</span>
                                <span class="stat-number">{records}</span>
                                <span class="stat-label">Historias Clínicas</span>
                            </div>
                        </div>
                        
                        <div class="detail-section">
                            <h2>📅 Estado de los Turnos</h2>
                            <div class="mini-stats">
                                <div class="mini-stat scheduled">
                                    <span class="mini-stat-label">📅 Programados</span>
                                    <span class="mini-stat-value">{appts_scheduled}</span>
                                </div>
                                <div class="mini-stat attended">
                                    <span class="mini-stat-label">✅ Atendidos</span>
                                    <span class="mini-stat-value">{appts_attended}</span>
                                </div>
                                <div class="mini-stat canceled">
                                    <span class="mini-stat-label">❌ Cancelados</span>
                                    <span class="mini-stat-value">{appts_canceled}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="footer">
                    <a href="/" class="btn btn-success">🏠 IR A INICIO</a>
                    <button onclick="window.location.reload()" class="btn btn-primary">🔄 Actualizar Datos</button>
                    <a href="/admin/db_details" class="btn btn-secondary">📊 Ver Detalles</a>
                    <a href="/ui" class="btn btn-secondary">⬅️ Volver al Panel</a>
                </div>
            </div>
        </body>
        </html>
        """

        return HTMLResponse(content=html)

@router.get("/admin/db_details", response_class=HTMLResponse, tags=["admin"])
def db_details(limit: int = 10, db: Session = Depends(get_db)):
        """Página amigable que muestra los últimos registros de cada tabla."""
        limit = max(1, min(limit, 50))  # seguridad básica, máx 50 para no sobrecargar

        owners = (
                db.query(models.Owner).order_by(models.Owner.id.desc()).limit(limit).all()
        )
        pets = (
                db.query(models.Pet).order_by(models.Pet.id.desc()).limit(limit).all()
        )
        appts = (
                db.query(models.Appointment)
                .order_by(models.Appointment.id.desc())
                .limit(limit)
                .all()
        )
        vaccs = (
                db.query(models.Vaccination)
                .order_by(models.Vaccination.id.desc())
                .limit(limit)
                .all()
        )

        def safe(v):
                return "" if v is None else str(v)
        
        def format_date(dt):
                if dt is None:
                        return ""
                if hasattr(dt, 'strftime'):
                        return dt.strftime('%d/%m/%Y %H:%M') if hasattr(dt, 'hour') else dt.strftime('%d/%m/%Y')
                return str(dt)

        # Generar filas de dueños
        owners_rows = ""
        for owner in owners:
                owners_rows += f"""
                <tr>
                    <td><strong>#{owner.id}</strong></td>
                    <td>{safe(owner.name)}</td>
                    <td>{safe(owner.phone)}</td>
                    <td>{safe(owner.email)}</td>
                    <td style="text-align: center;">
                        <a href="/owners/{owner.id}/view" target="_blank" class="btn-mini btn-view">👁️ Ver</a>
                        <a href="/owners/{owner.id}/edit" target="_blank" class="btn-mini btn-edit">✏️ Editar</a>
                        <a href="/owners/{owner.id}/delete" target="_blank" class="btn-mini btn-delete" onclick="return confirm('¿Estás seguro de eliminar este dueño? Se eliminarán también todas sus mascotas y turnos.')">🗑️ Eliminar</a>
                    </td>
                </tr>
                """
        
        # Generar filas de mascotas
        pets_rows = ""
        species_emoji_map = {
            'perro': '🐕',
            'gato': '🐈',
            'ave': '🦜',
            'conejo': '🐰',
            'hamster': '🐹',
        }
        for pet in pets:
                species_emoji = species_emoji_map.get(safe(pet.species).lower(), '🐾')
                owner_name = pet.owner.name if pet.owner else 'N/A'
                pets_rows += f"""
                <tr>
                    <td><strong>#{pet.id}</strong></td>
                    <td>{species_emoji} {safe(pet.name)}</td>
                    <td>{safe(pet.species)}</td>
                    <td>{safe(pet.breed)}</td>
                    <td>{owner_name}</td>
                    <td style="text-align: center;">
                        <a href="/pets/{pet.id}/view" target="_blank" class="btn-mini btn-view">👁️ Ver</a>
                        <a href="/pets/{pet.id}/edit" target="_blank" class="btn-mini btn-edit">✏️ Editar</a>
                        <a href="/pets/{pet.id}/delete" target="_blank" class="btn-mini btn-delete" onclick="return confirm('¿Estás seguro de eliminar esta mascota? Se eliminarán también todos sus turnos y registros clínicos.')">🗑️ Eliminar</a>
                    </td>
                </tr>
                """
        
        # Generar filas de turnos
        appts_rows = ""
        status_map = {
            'scheduled': {'text': 'Programado', 'color': '#28a745', 'icon': '📅'},
            'attended': {'text': 'Atendido', 'color': '#007bff', 'icon': '✅'},
            'canceled': {'text': 'Cancelado', 'color': '#dc3545', 'icon': '❌'}
        }
        for apt in appts:
                apt_status = str(apt.status) if apt.status else 'scheduled'  # type: ignore
                status_info = status_map.get(apt_status, {'text': apt_status, 'color': '#6c757d', 'icon': '📋'})
                pet_name = apt.pet.name if apt.pet else 'N/A'
                
                # Agregar botón de cancelar solo si el turno está programado
                cancel_button = ""
                if apt_status == 'scheduled':
                    cancel_button = f'<a href="/appointments/{apt.id}/cancel-form" target="_blank" class="btn-mini btn-cancel" onclick="return confirm(\'¿Deseas cancelar este turno? Esta acción quedará registrada en el historial.\')">❌ Cancelar</a>'
                
                appts_rows += f"""
                <tr>
                    <td><strong>#{apt.id}</strong></td>
                    <td>{format_date(apt.appointment_date)}</td>
                    <td>{safe(apt.reason)}</td>
                    <td>
                        <span style="background: {status_info['color']}; color: white; padding: 0.3rem 0.7rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                            {status_info['icon']} {status_info['text']}
                        </span>
                    </td>
                    <td>{pet_name}</td>
                    <td style="text-align: center;">
                        <a href="/appointments/{apt.id}/view" target="_blank" class="btn-mini btn-view">👁️ Ver</a>
                        {cancel_button}
                    </td>
                </tr>
                """
        
        # Generar filas de vacunaciones
        vaccs_rows = ""
        vacc_status_map = {
            'due': {'text': 'Pendiente', 'color': '#ffc107', 'icon': '⏳'},
            'done': {'text': 'Aplicada', 'color': '#28a745', 'icon': '✅'},
            'overdue': {'text': 'Vencida', 'color': '#dc3545', 'icon': '⚠️'},
            'upcoming': {'text': 'Próxima', 'color': '#17a2b8', 'icon': '📅'}
        }
        for vacc in vaccs:
                pet_name = vacc.pet.name if vacc.pet else 'N/A'
                vacc_status = str(vacc.status) if vacc.status else 'due'  # type: ignore
                status_info = vacc_status_map.get(vacc_status, {'text': vacc_status, 'color': '#6c757d', 'icon': '💉'})
                vaccs_rows += f"""
                <tr>
                    <td><strong>#{vacc.id}</strong></td>
                    <td>💉 {safe(vacc.vaccine_name)}</td>
                    <td>{format_date(vacc.applied_date)}</td>
                    <td>{format_date(vacc.due_date)}</td>
                    <td>
                        <span style="background: {status_info['color']}; color: white; padding: 0.3rem 0.7rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                            {status_info['icon']} {status_info['text']}
                        </span>
                    </td>
                    <td>{pet_name}</td>
                </tr>
                """

        html = f"""
        <!doctype html>
        <html lang="es">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>� Registros del Sistema - Veterinaria Inteligente</title>
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    height: 100vh;
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                }}
                .container {{
                    display: flex;
                    flex-direction: column;
                    height: 100vh;
                }}
                .header {{
                    background: rgba(255,255,255,0.98);
                    border-bottom: 3px solid #11998e;
                    padding: 0.8rem 1.5rem;
                    text-align: center;
                    flex-shrink: 0;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 1.5rem;
                    color: #333;
                    font-weight: 700;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                }}
                .header p {{
                    margin: 0.3rem 0 0 0;
                    font-size: 0.8rem;
                    color: #666;
                }}
                .info-banner {{
                    background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
                    border-bottom: 2px solid #f39c12;
                    padding: 0.7rem 1.5rem;
                    text-align: center;
                    flex-shrink: 0;
                }}
                .info-banner p {{
                    margin: 0;
                    color: #333;
                    font-size: 0.8rem;
                    line-height: 1.4;
                }}
                .info-banner strong {{
                    color: #d35400;
                }}
                .controls-bar {{
                    background: rgba(255,255,255,0.95);
                    border-bottom: 2px solid #11998e;
                    padding: 0.6rem 1.5rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 0.8rem;
                    flex-shrink: 0;
                    flex-wrap: wrap;
                }}
                .controls-bar label {{
                    font-weight: 600;
                    color: #333;
                    font-size: 0.85rem;
                }}
                .controls-bar input {{
                    padding: 0.4rem 0.8rem;
                    border: 2px solid #ddd;
                    border-radius: 6px;
                    font-size: 0.85rem;
                    width: 80px;
                }}
                .controls-bar button {{
                    padding: 0.5rem 1rem;
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: 700;
                    font-size: 0.8rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }}
                .controls-bar button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
                }}
                .main-content {{
                    flex: 1;
                    overflow-y: auto;
                    padding: 1rem 1.5rem 1rem;
                    background: rgba(255,255,255,0.95);
                }}
                .content-wrapper {{
                    max-width: 1600px;
                    margin: 0 auto;
                }}
                .table-section {{
                    margin-bottom: 1.5rem;
                    background: #fff;
                    border-radius: 10px;
                    padding: 1rem;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    border: 2px solid #e0e0e0;
                }}
                .table-section h2 {{
                    margin: 0 0 0.8rem 0;
                    color: #333;
                    font-size: 1rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    border-bottom: 2px solid #11998e;
                    padding-bottom: 0.5rem;
                }}
                .table-wrapper {{
                    overflow-x: auto;
                    max-height: 300px;
                    overflow-y: auto;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    font-size: 0.75rem;
                }}
                thead {{
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    position: sticky;
                    top: 0;
                    z-index: 10;
                }}
                th {{
                    color: white;
                    padding: 0.6rem 0.8rem;
                    text-align: left;
                    font-weight: 600;
                    text-transform: uppercase;
                    font-size: 0.7rem;
                    letter-spacing: 0.5px;
                    white-space: nowrap;
                }}
                td {{
                    padding: 0.6rem 0.8rem;
                    border-bottom: 1px solid #e5e7eb;
                    font-size: 0.75rem;
                    white-space: nowrap;
                }}
                tbody tr:hover {{
                    background: #f0fdf4;
                    transition: background 0.2s ease;
                }}
                .btn-mini {{
                    display: inline-block;
                    padding: 0.3rem 0.6rem;
                    border-radius: 5px;
                    text-decoration: none;
                    font-size: 0.7rem;
                    font-weight: 600;
                    transition: all 0.2s ease;
                    margin: 0 0.1rem;
                    white-space: nowrap;
                }}
                .btn-view {{
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    color: white;
                }}
                .btn-view:hover {{
                    transform: translateY(-1px);
                    box-shadow: 0 2px 6px rgba(17, 153, 142, 0.3);
                }}
                .btn-edit {{
                    background: linear-gradient(135deg, #f39c12 0%, #f1c40f 100%);
                    color: white;
                }}
                .btn-edit:hover {{
                    transform: translateY(-1px);
                    box-shadow: 0 2px 6px rgba(243, 156, 18, 0.3);
                }}
                .btn-delete {{
                    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                    color: white;
                }}
                .btn-delete:hover {{
                    transform: translateY(-1px);
                    box-shadow: 0 2px 6px rgba(231, 76, 60, 0.3);
                }}
                .btn-cancel {{
                    background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
                    color: white;
                }}
                .btn-cancel:hover {{
                    transform: translateY(-1px);
                    box-shadow: 0 2px 6px rgba(149, 165, 166, 0.3);
                }}
                .footer {{
                    background: rgba(255,255,255,0.98);
                    border-top: 3px solid #11998e;
                    padding: 0.8rem 1.5rem;
                    flex-shrink: 0;
                    display: flex;
                    justify-content: center;
                    gap: 0.8rem;
                    flex-wrap: wrap;
                    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
                }}
                .btn {{
                    display: inline-block;
                    padding: 0.6rem 1.3rem;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 700;
                    font-size: 0.8rem;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                    border: none;
                    cursor: pointer;
                    white-space: nowrap;
                }}
                .btn-primary {{
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    color: white;
                }}
                .btn-primary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
                }}
                .btn-secondary {{
                    background: linear-gradient(135deg, #868f96 0%, #596164 100%);
                    color: white;
                }}
                .btn-secondary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(134, 143, 150, 0.4);
                }}
                .btn-success {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .btn-success:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                }}
                .empty-state {{
                    text-align: center;
                    color: #999;
                    padding: 2rem;
                    font-style: italic;
                }}
                ::-webkit-scrollbar {{
                    width: 8px;
                    height: 8px;
                }}
                ::-webkit-scrollbar-track {{
                    background: #f1f1f1;
                    border-radius: 4px;
                }}
                ::-webkit-scrollbar-thumb {{
                    background: #11998e;
                    border-radius: 4px;
                }}
                ::-webkit-scrollbar-thumb:hover {{
                    background: #38ef7d;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>� Registros del Sistema</h1>
                    <p>Visualización de los últimos registros de cada categoría</p>
                </div>
                
                <div class="info-banner">
                    <p>💡 <strong>Vista personalizable:</strong> Ajustá la cantidad de registros que querés ver en cada tabla. Los datos se muestran ordenados del más reciente al más antiguo.</p>
                </div>
                
                <form class="controls-bar" method="get" action="/admin/db_details">
                    <label>📋 Registros por tabla:</label>
                    <input type="number" name="limit" min="1" max="50" value="{limit}" />
                    <button type="submit">🔄 Actualizar Vista</button>
                </form>
                
                <div class="main-content">
                    <div class="content-wrapper">
                        <div class="table-section">
                            <h2>👥 Dueños Registrados (últimos {limit})</h2>
                            <div class="table-wrapper">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Nombre</th>
                                            <th>Teléfono</th>
                                            <th>Email</th>
                                            <th style="text-align: center;">Acciones</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {owners_rows if owners_rows else '<tr><td colspan="5" class="empty-state">No hay dueños registrados en el sistema</td></tr>'}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        
                        <div class="table-section">
                            <h2>🐾 Mascotas Registradas (últimas {limit})</h2>
                            <div class="table-wrapper">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Nombre</th>
                                            <th>Especie</th>
                                            <th>Raza</th>
                                            <th>Dueño</th>
                                            <th style="text-align: center;">Acciones</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {pets_rows if pets_rows else '<tr><td colspan="6" class="empty-state">No hay mascotas registradas en el sistema</td></tr>'}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        
                        <div class="table-section">
                            <h2>📅 Turnos Programados (últimos {limit})</h2>
                            <div class="table-wrapper">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Fecha y Hora</th>
                                            <th>Motivo</th>
                                            <th>Estado</th>
                                            <th>Mascota</th>
                                            <th style="text-align: center;">Acciones</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {appts_rows if appts_rows else '<tr><td colspan="6" class="empty-state">No hay turnos registrados en el sistema</td></tr>'}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        
                        <div class="table-section">
                            <h2>💉 Vacunaciones Aplicadas (últimas {limit})</h2>
                            <div class="table-wrapper">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Vacuna</th>
                                            <th>Fecha Aplicación</th>
                                            <th>Próxima Dosis</th>
                                            <th>Estado</th>
                                            <th>Mascota</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {vaccs_rows if vaccs_rows else '<tr><td colspan="6" class="empty-state">No hay vacunaciones registradas en el sistema</td></tr>'}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="footer">
                    <a href="/" class="btn btn-success">🏠 IR A INICIO</a>
                    <a href="/admin/db_counts_form" class="btn btn-primary">📊 Ver Totales</a>
                    <a href="/ui" class="btn btn-secondary">⬅️ Volver al Panel</a>
                </div>
            </div>
        </body>
        </html>
        """

        return HTMLResponse(content=html)


@router.get("/admin/api_docs_friendly", response_class=HTMLResponse, tags=["admin"])
def api_docs_friendly():
        """Página amigable que explica la documentación de la API para usuarios no técnicos."""
        html = """
        <!doctype html>
        <html lang="es">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>📖 Documentación de la API - Veterinaria Inteligente</title>
            <style>
                * { box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 2rem;
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    min-height: 100vh;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background: #fff;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    overflow: hidden;
                    animation: slideIn 0.5s ease-out;
                }
                @keyframes slideIn {
                    from { opacity: 0; transform: translateY(-30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .header {
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    padding: 2.5rem;
                    text-align: center;
                }
                .header h1 {
                    margin: 0;
                    font-size: 2.5rem;
                    font-weight: bold;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                }
                .header p {
                    margin: 0.5rem 0 0 0;
                    font-size: 1.1rem;
                    opacity: 0.95;
                }
                .content {
                    padding: 2.5rem;
                }
                .intro-box {
                    background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
                    border-radius: 15px;
                    padding: 2rem;
                    margin-bottom: 2rem;
                    border-left: 5px solid #00bcd4;
                }
                .intro-box h2 {
                    margin: 0 0 1rem 0;
                    color: #00838f;
                    font-size: 1.5rem;
                }
                .intro-box p {
                    margin: 0.5rem 0;
                    color: #333;
                    font-size: 1rem;
                    line-height: 1.6;
                }
                .section {
                    margin-bottom: 2.5rem;
                }
                .section h2 {
                    color: #333;
                    font-size: 1.8rem;
                    margin-bottom: 1rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                .cards-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 1.5rem;
                    margin-top: 1.5rem;
                }
                .card {
                    background: #f8f9fa;
                    border-radius: 15px;
                    padding: 1.5rem;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                    transition: all 0.3s ease;
                    border-left: 5px solid var(--card-color);
                }
                .card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                }
                .card.owners { --card-color: #667eea; }
                .card.pets { --card-color: #11998e; }
                .card.appointments { --card-color: #fa709a; }
                .card.vaccinations { --card-color: #30cfd0; }
                .card.records { --card-color: #f093fb; }
                .card h3 {
                    margin: 0 0 1rem 0;
                    color: #333;
                    font-size: 1.3rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                .card p {
                    margin: 0.5rem 0;
                    color: #666;
                    font-size: 0.95rem;
                    line-height: 1.5;
                }
                .card ul {
                    margin: 1rem 0 0 0;
                    padding-left: 1.5rem;
                }
                .card li {
                    margin: 0.5rem 0;
                    color: #555;
                    font-size: 0.9rem;
                }
                .highlight-box {
                    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                    border-radius: 10px;
                    padding: 1.5rem;
                    margin: 2rem 0;
                    border-left: 5px solid #ffc107;
                }
                .highlight-box h3 {
                    margin: 0 0 1rem 0;
                    color: #856404;
                    font-size: 1.3rem;
                }
                .highlight-box p {
                    margin: 0.5rem 0;
                    color: #333;
                    font-size: 1rem;
                    line-height: 1.6;
                }
                .buttons {
                    display: flex;
                    gap: 1rem;
                    justify-content: center;
                    margin-top: 2.5rem;
                    flex-wrap: wrap;
                }
                .btn {
                    display: inline-block;
                    padding: 1rem 2rem;
                    border-radius: 50px;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 1rem;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                }
                .btn-primary {
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                }
                .btn-primary:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
                }
                .btn-success {
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    color: white;
                }
                .btn-success:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 6px 20px rgba(17, 153, 142, 0.4);
                }
                .btn-secondary {
                    background: linear-gradient(135deg, #868f96 0%, #596164 100%);
                    color: white;
                }
                .btn-secondary:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 6px 20px rgba(134, 143, 150, 0.4);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📖 Documentación de la API</h1>
                    <p>Guía completa para entender y usar el sistema</p>
                </div>
                
                <div class="content">
                    <div class="intro-box">
                        <h2>👋 ¿Qué es la API?</h2>
                        <p><strong>API</strong> significa "Interfaz de Programación de Aplicaciones". En términos simples, es el sistema que permite que diferentes partes del programa se comuniquen entre sí.</p>
                        <p>Esta documentación te muestra todas las funcionalidades disponibles en el sistema de Veterinaria Inteligente: cómo crear, ver, modificar y eliminar información sobre dueños, mascotas, turnos y vacunaciones.</p>
                        <p>💡 <strong>No necesitás ser programador para usar el sistema.</strong> Esta página es solo informativa. Usá las interfaces web amigables del Panel de Recepción para trabajar normalmente.</p>
                    </div>
                    
                    <div class="section">
                        <h2>🔧 Funcionalidades del Sistema</h2>
                        
                        <div class="cards-grid">
                            <div class="card owners">
                                <h3>👥 Gestión de Dueños</h3>
                                <p>Administración completa de los propietarios de mascotas.</p>
                                <ul>
                                    <li>✅ Crear nuevos dueños con sus datos de contacto</li>
                                    <li>👁️ Ver listado completo de todos los dueños</li>
                                    <li>✏️ Editar información de contacto</li>
                                    <li>🗑️ Eliminar dueños (incluye todas sus mascotas)</li>
                                    <li>🔍 Buscar dueños específicos</li>
                                </ul>
                            </div>
                            
                            <div class="card pets">
                                <h3>🐾 Gestión de Mascotas</h3>
                                <p>Control de pacientes animales y sus características.</p>
                                <ul>
                                    <li>✅ Registrar nuevas mascotas (nombre, especie, raza, fecha nacimiento)</li>
                                    <li>👁️ Ver listado de todas las mascotas registradas</li>
                                    <li>✏️ Editar datos de las mascotas</li>
                                    <li>🗑️ Eliminar mascotas (incluye historial clínico)</li>
                                    <li>📋 Ver historia clínica completa</li>
                                </ul>
                            </div>
                            
                            <div class="card appointments">
                                <h3>📅 Gestión de Turnos</h3>
                                <p>Sistema de agendamiento y seguimiento de citas.</p>
                                <ul>
                                    <li>✅ Crear turnos con fecha, hora y motivo</li>
                                    <li>👁️ Ver agenda completa de turnos</li>
                                    <li>❌ Cancelar turnos con registro de motivo</li>
                                    <li>📊 Estados: Programado, Atendido, Cancelado</li>
                                    <li>🔍 Filtrar por fecha y estado</li>
                                </ul>
                            </div>
                            
                            <div class="card vaccinations">
                                <h3>💉 Gestión de Vacunas</h3>
                                <p>Control del calendario de vacunación.</p>
                                <ul>
                                    <li>✅ Registrar vacunas aplicadas</li>
                                    <li>📅 Programar próximas dosis</li>
                                    <li>⏰ Alertas de vacunas pendientes</li>
                                    <li>📋 Historial completo de vacunación</li>
                                    <li>⚠️ Notificaciones de vacunas vencidas</li>
                                </ul>
                            </div>
                            
                            <div class="card records">
                                <h3>📋 Historia Clínica</h3>
                                <p>Registro médico detallado de cada mascota.</p>
                                <ul>
                                    <li>✅ Crear registros de visitas veterinarias</li>
                                    <li>👁️ Ver historial completo</li>
                                    <li>📝 Incluir diagnósticos, tratamientos y notas</li>
                                    <li>📊 Seguimiento de evolución del paciente</li>
                                    <li>🔍 Búsqueda por mascota o fecha</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="highlight-box">
                        <h3>🤖 Funciones Inteligentes del Sistema</h3>
                        <p><strong>Análisis de Sentimiento:</strong> El sistema analiza automáticamente los comentarios y notas para detectar situaciones que requieren atención especial.</p>
                        <p><strong>Predicción de No-Show:</strong> Algoritmo que predice la probabilidad de que un paciente no asista a su turno, basándose en patrones históricos.</p>
                        <p><strong>Clasificación de Intenciones:</strong> Identifica automáticamente el tipo de consulta o servicio requerido al analizar las solicitudes.</p>
                        <p><strong>Extracción de Palabras Clave:</strong> Detecta términos importantes en textos largos para facilitar búsquedas y análisis.</p>
                    </div>
                    
                    <div class="section">
                        <h2>🎯 ¿Cómo usar el sistema?</h2>
                        <div class="intro-box">
                            <p><strong>Para usuarios recepcionistas:</strong></p>
                            <p>1. Usá el <strong>Panel de Recepción</strong> (botón en la parte superior)</p>
                            <p>2. Allí encontrarás formularios simples para crear dueños, mascotas y turnos</p>
                            <p>3. Los botones "Ver dueños", "Ver mascotas" y "Ver turnos" te muestran listados organizados</p>
                            <p>4. En cada listado tenés botones para Ver, Editar o Eliminar cada registro</p>
                            <br>
                            <p><strong>Para veterinarios:</strong></p>
                            <p>1. Usá el <strong>Panel Veterinario</strong></p>
                            <p>2. Allí podés ver turnos del día, crear historias clínicas y registrar vacunas</p>
                            <p>3. El sistema te muestra predicciones y análisis inteligentes automáticamente</p>
                        </div>
                    </div>
                    
                    <div class="buttons">
                        <a href="/admin/api_docs_visual" class="btn btn-primary">📖 Ver Documentación Técnica Completa</a>
                        <a href="/admin/db_details" class="btn btn-success">📊 Ver Datos del Sistema</a>
                        <a href="/ui" class="btn btn-secondary">⬅️ Volver al Panel</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HTMLResponse(content=html)


@router.get("/admin/api_docs_visual", response_class=HTMLResponse, tags=["admin"])
def api_docs_visual(db: Session = Depends(get_db)):
    """Documentación visual y amigable de todos los endpoints del sistema."""
    
    # Obtener algunos datos de ejemplo para mostrar
    owners_count = db.query(models.Owner).count()
    pets_count = db.query(models.Pet).count()
    appointments_count = db.query(models.Appointment).count()
    
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📚 Guía Visual del Sistema - Veterinaria Inteligente</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 2rem;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 3rem 2rem;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                font-weight: 700;
            }
            
            .header p {
                font-size: 1.1rem;
                opacity: 0.95;
            }
            
            .content {
                padding: 2rem;
            }
            
            .info-banner {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                text-align: center;
            }
            
            .info-banner h2 {
                font-size: 1.5rem;
                margin-bottom: 0.5rem;
            }
            
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-bottom: 2rem;
            }
            
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .stat-card .number {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }
            
            .stat-card .label {
                font-size: 1rem;
                opacity: 0.9;
            }
            
            .section {
                margin-bottom: 2rem;
            }
            
            .section-title {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 12px 12px 0 0;
                font-size: 1.3rem;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .section-content {
                border: 2px solid #667eea;
                border-top: none;
                border-radius: 0 0 12px 12px;
                padding: 1.5rem;
                background: #f8f9fa;
            }
            
            .endpoint {
                background: white;
                border-left: 4px solid #667eea;
                padding: 1.5rem;
                margin-bottom: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                transition: all 0.3s;
            }
            
            .endpoint:hover {
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
                transform: translateX(5px);
            }
            
            .endpoint-header {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1rem;
            }
            
            .method {
                padding: 0.4rem 0.8rem;
                border-radius: 6px;
                font-weight: 700;
                font-size: 0.85rem;
                text-transform: uppercase;
            }
            
            .method.get {
                background: #4caf50;
                color: white;
            }
            
            .method.post {
                background: #2196f3;
                color: white;
            }
            
            .method.put {
                background: #ff9800;
                color: white;
            }
            
            .method.delete {
                background: #f44336;
                color: white;
            }
            
            .endpoint-path {
                font-family: 'Courier New', monospace;
                font-size: 1.1rem;
                color: #667eea;
                font-weight: 600;
            }
            
            .endpoint-description {
                color: #555;
                line-height: 1.6;
                margin-bottom: 1rem;
            }
            
            .endpoint-example {
                background: #e8eaf6;
                padding: 1rem;
                border-radius: 6px;
                border-left: 3px solid #667eea;
            }
            
            .endpoint-example strong {
                color: #667eea;
                display: block;
                margin-bottom: 0.5rem;
            }
            
            .endpoint-example code {
                font-family: 'Courier New', monospace;
                color: #333;
                display: block;
                margin-top: 0.5rem;
            }
            
            .use-case {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 1rem;
                margin-top: 1rem;
                border-radius: 6px;
            }
            
            .use-case strong {
                color: #856404;
            }
            
            .buttons {
                display: flex;
                gap: 1rem;
                margin-top: 2rem;
                flex-wrap: wrap;
            }
            
            .btn {
                flex: 1;
                min-width: 200px;
                padding: 1rem 1.5rem;
                border-radius: 10px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1rem;
                transition: all 0.3s;
                display: inline-block;
                text-align: center;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .btn-primary:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            
            .btn-success {
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
            }
            
            .btn-success:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(17, 153, 142, 0.4);
            }
            
            .btn-warning {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            }
            
            .btn-warning:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(240, 147, 251, 0.4);
            }
            
            .btn-secondary {
                background: #6c757d;
                color: white;
            }
            
            .btn-secondary:hover {
                background: #5a6268;
                transform: translateY(-3px);
            }
            
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 1.8rem;
                }
                
                .buttons {
                    flex-direction: column;
                }
                
                .btn {
                    width: 100%;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Guía Visual del Sistema</h1>
                <p>Documentación completa y amigable de todas las funcionalidades del sistema</p>
            </div>
            
            <div class="content">
                <div class="info-banner">
                    <h2>🎯 Sistema de Gestión Veterinaria Inteligente</h2>
                    <p>Esta guía te muestra todas las operaciones que puedes realizar en el sistema de manera visual y fácil de entender</p>
                </div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="number">""" + str(owners_count) + """</div>
                        <div class="label">👥 Dueños registrados</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">""" + str(pets_count) + """</div>
                        <div class="label">🐾 Mascotas en sistema</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">""" + str(appointments_count) + """</div>
                        <div class="label">📅 Turnos totales</div>
                    </div>
                </div>
                
                <!-- SECCIÓN: GESTIÓN DE DUEÑOS -->
                <div class="section">
                    <div class="section-title">
                        <span>👥</span> Gestión de Dueños
                    </div>
                    <div class="section-content">
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">VER</span>
                                <span class="endpoint-path">/owners/view</span>
                            </div>
                            <div class="endpoint-description">
                                Ver el listado completo de todos los dueños registrados en el sistema. Muestra nombre, teléfono, email y cantidad de mascotas.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> La recepcionista quiere ver todos los clientes registrados para buscar el teléfono de un dueño.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method post">CREAR</span>
                                <span class="endpoint-path">/owners/form</span>
                            </div>
                            <div class="endpoint-description">
                                Registrar un nuevo dueño en el sistema. Permite ingresar nombre, teléfono y correo electrónico.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Llega un cliente nuevo con su mascota. La recepcionista registra sus datos antes de crear el turno.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method put">EDITAR</span>
                                <span class="endpoint-path">/owners/{id}/edit</span>
                            </div>
                            <div class="endpoint-description">
                                Modificar los datos de un dueño existente. Útil cuando cambia el teléfono o correo electrónico.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Un cliente cambió su número de teléfono y la recepcionista actualiza su información.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method delete">ELIMINAR</span>
                                <span class="endpoint-path">/owners/{id}/delete</span>
                            </div>
                            <div class="endpoint-description">
                                Eliminar un dueño del sistema. Esta acción también elimina todas sus mascotas y turnos asociados.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Un cliente se mudó de ciudad y ya no atenderá sus mascotas en la clínica.
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- SECCIÓN: GESTIÓN DE MASCOTAS -->
                <div class="section">
                    <div class="section-title">
                        <span>🐾</span> Gestión de Mascotas
                    </div>
                    <div class="section-content">
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">VER</span>
                                <span class="endpoint-path">/pets/view</span>
                            </div>
                            <div class="endpoint-description">
                                Ver listado de todas las mascotas con su información básica: nombre, especie, raza y dueño.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> El veterinario quiere buscar el historial de "Rocky" antes de la consulta.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method post">CREAR</span>
                                <span class="endpoint-path">/pets/form</span>
                            </div>
                            <div class="endpoint-description">
                                Registrar una nueva mascota asociada a un dueño. Incluye nombre, especie, raza, fecha de nacimiento y notas.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Un cliente trae una nueva mascota que acaba de adoptar y se registra en el sistema.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">VER DETALLE</span>
                                <span class="endpoint-path">/pets/{id}/view</span>
                            </div>
                            <div class="endpoint-description">
                                Ver información completa de una mascota específica, incluyendo su historial médico y turnos.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> El veterinario necesita revisar el historial completo de vacunas antes de aplicar una nueva.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">HISTORIAL</span>
                                <span class="endpoint-path">/pets/{id}/clinical-history</span>
                            </div>
                            <div class="endpoint-description">
                                Ver el historial clínico completo de una mascota con todas sus consultas y tratamientos.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> La mascota tiene un problema recurrente y el veterinario revisa consultas anteriores.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method put">EDITAR</span>
                                <span class="endpoint-path">/pets/{id}/edit</span>
                            </div>
                            <div class="endpoint-description">
                                Modificar información de una mascota (nombre, raza, notas, etc.).
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> El dueño descubrió que la mascota es de otra raza y actualiza la información.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method delete">ELIMINAR</span>
                                <span class="endpoint-path">/pets/{id}/delete</span>
                            </div>
                            <div class="endpoint-description">
                                Eliminar una mascota del sistema junto con todo su historial médico y turnos.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Lamentablemente la mascota falleció y se elimina su registro del sistema activo.
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- SECCIÓN: GESTIÓN DE TURNOS -->
                <div class="section">
                    <div class="section-title">
                        <span>📅</span> Gestión de Turnos
                    </div>
                    <div class="section-content">
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">VER</span>
                                <span class="endpoint-path">/appointments/view</span>
                            </div>
                            <div class="endpoint-description">
                                Ver todos los turnos programados con información de fecha, hora, mascota y estado.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> La recepcionista revisa la agenda del día para confirmar las citas.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method post">CREAR</span>
                                <span class="endpoint-path">/appointments/form</span>
                            </div>
                            <div class="endpoint-description">
                                Agendar un nuevo turno para una mascota. Permite elegir fecha, hora y agregar notas.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Un cliente llama para pedir un turno para vacunación antirrábica de su perro.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">VER DETALLE</span>
                                <span class="endpoint-path">/appointments/{id}/view</span>
                            </div>
                            <div class="endpoint-description">
                                Ver información completa de un turno específico, incluyendo todos los detalles de la mascota y dueño.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Antes de la consulta, el veterinario revisa el motivo de la visita y las notas.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method post">CANCELAR</span>
                                <span class="endpoint-path">/appointments/{id}/cancel-form</span>
                            </div>
                            <div class="endpoint-description">
                                Cancelar un turno con motivo. Permite seleccionar la razón de cancelación para estadísticas.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> El cliente cancela porque la mascota ya se siente mejor. Se registra el motivo.
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- SECCIÓN: REGISTROS CLÍNICOS -->
                <div class="section">
                    <div class="section-title">
                        <span>🏥</span> Registros Clínicos
                    </div>
                    <div class="section-content">
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method post">CREAR</span>
                                <span class="endpoint-path">/records/</span>
                            </div>
                            <div class="endpoint-description">
                                Crear un nuevo registro clínico después de una consulta. Incluye diagnóstico, tratamiento y observaciones.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Después de atender a una mascota, el veterinario registra el diagnóstico y tratamiento.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">VER</span>
                                <span class="endpoint-path">/records/{pet_id}</span>
                            </div>
                            <div class="endpoint-description">
                                Ver todos los registros clínicos de una mascota específica.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Revisar el historial médico completo antes de una cirugía programada.
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- SECCIÓN: VACUNACIONES -->
                <div class="section">
                    <div class="section-title">
                        <span>💉</span> Control de Vacunaciones
                    </div>
                    <div class="section-content">
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">VER</span>
                                <span class="endpoint-path">/vaccinations/view</span>
                            </div>
                            <div class="endpoint-description">
                                Ver todas las vacunas registradas en el sistema con su estado (aplicada, pendiente, vencida).
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Revisar qué mascotas tienen vacunas pendientes este mes.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method post">CREAR</span>
                                <span class="endpoint-path">/vaccinations/form</span>
                            </div>
                            <div class="endpoint-description">
                                Registrar una nueva vacuna aplicada o programada para una mascota.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Después de aplicar la vacuna antirrábica, se registra en el sistema con la fecha.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">ALERTAS</span>
                                <span class="endpoint-path">/vaccinations/alerts</span>
                            </div>
                            <div class="endpoint-description">
                                Ver alertas de vacunas próximas a vencer o vencidas que requieren atención.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> La recepcionista llama a clientes para recordar vacunas que están por vencer.
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- SECCIÓN: INTELIGENCIA ARTIFICIAL -->
                <div class="section">
                    <div class="section-title">
                        <span>🤖</span> Funciones Inteligentes
                    </div>
                    <div class="section-content">
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method post">ANÁLISIS</span>
                                <span class="endpoint-path">/ai/intent</span>
                            </div>
                            <div class="endpoint-description">
                                Analiza automáticamente el mensaje de un cliente para entender qué necesita (turno, consulta, emergencia).
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Cliente escribe "mi perro tiene fiebre" y el sistema detecta que es una posible emergencia.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method post">SENTIMIENTO</span>
                                <span class="endpoint-path">/ai/sentiment</span>
                            </div>
                            <div class="endpoint-description">
                                Analiza el tono emocional de un mensaje (positivo, negativo, neutral) para priorizar atención.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Detecta que un mensaje tiene tono negativo y alerta para dar atención prioritaria.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method post">PREDICCIÓN</span>
                                <span class="endpoint-path">/ai/predict-noshow</span>
                            </div>
                            <div class="endpoint-description">
                                Predice la probabilidad de que un cliente no asista a su turno basándose en patrones históricos.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Sistema detecta 80% de probabilidad de inasistencia y sugiere confirmación telefónica.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method post">PALABRAS CLAVE</span>
                                <span class="endpoint-path">/ai/keywords</span>
                            </div>
                            <div class="endpoint-description">
                                Extrae las palabras más importantes de un texto para resúmenes rápidos.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> De un mensaje largo extrae: "vómito", "fiebre", "urgente" para diagnóstico rápido.
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- SECCIÓN: REPORTES Y ESTADÍSTICAS -->
                <div class="section">
                    <div class="section-title">
                        <span>📊</span> Reportes y Estadísticas
                    </div>
                    <div class="section-content">
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">REPORTES</span>
                                <span class="endpoint-path">/reports/</span>
                            </div>
                            <div class="endpoint-description">
                                Genera reportes personalizados con estadísticas del sistema (turnos, ingresos, mascotas atendidas).
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> El administrador genera un reporte mensual de turnos atendidos vs. cancelados.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">TOTALES</span>
                                <span class="endpoint-path">/admin/db_counts_form</span>
                            </div>
                            <div class="endpoint-description">
                                Ver contadores totales del sistema: dueños, mascotas, turnos programados, atendidos y cancelados.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Revisar rápidamente cuántos clientes activos tiene la veterinaria.
                            </div>
                        </div>
                        
                        <div class="endpoint">
                            <div class="endpoint-header">
                                <span class="method get">DETALLES</span>
                                <span class="endpoint-path">/admin/db_details</span>
                            </div>
                            <div class="endpoint-description">
                                Ver listados completos de todos los datos del sistema organizados por tablas.
                            </div>
                            <div class="use-case">
                                <strong>💡 Caso de uso:</strong> Auditoría de datos para verificar información antes de un respaldo.
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="buttons">
                    <a href="/docs" target="_blank" class="btn btn-warning">🔧 Ver Documentación Técnica (Desarrolladores)</a>
                    <a href="/admin/api_docs_friendly" class="btn btn-primary">📖 Volver a Guía Simple</a>
                    <a href="/admin/db_details" class="btn btn-success">📊 Ver Datos del Sistema</a>
                    <a href="/ui" class="btn btn-secondary">⬅️ Panel Principal</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html)


@router.get("/admin/presentation", response_class=HTMLResponse, tags=["admin"])
def project_presentation():
    """Presentación completa del proyecto Veterinaria Inteligente - IFTS-12."""
    
    # Leer el archivo markdown
    presentation_path = Path(__file__).parent.parent.parent.parent / "docs" / "Presentacion_Proyecto.md"
    
    try:
        with open(presentation_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        markdown_content = "# Error\n\nNo se pudo encontrar el documento de presentación."
    
    # Convertir markdown a HTML (conversión básica)
    html_content = markdown_content.replace('\n### ', '\n<h3>').replace('\n## ', '\n<h2>').replace('\n# ', '\n<h1>')
    html_content = html_content.replace('### ', '<h3>').replace('## ', '<h2>').replace('# ', '<h1>')
    html_content = html_content.replace('\n\n', '</p><p>').replace('\n', '<br>')
    html_content = html_content.replace('**', '<strong>').replace('</strong>', '</strong>', 1)
    
    # Procesar listas
    lines = markdown_content.split('\n')
    processed_html = []
    in_list = False
    in_code_block = False
    in_table = False
    
    for i, line in enumerate(lines):
        # Code blocks
        if line.startswith('```'):
            if not in_code_block:
                processed_html.append('<pre><code>')
                in_code_block = True
            else:
                processed_html.append('</code></pre>')
                in_code_block = False
            continue
        
        if in_code_block:
            processed_html.append(line)
            continue
        
        # Títulos
        if line.startswith('# '):
            processed_html.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            processed_html.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            processed_html.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('#### '):
            processed_html.append(f'<h4>{line[5:]}</h4>')
        
        # Listas
        elif line.startswith('- ') or line.startswith('* ') or line.startswith('+ '):
            if not in_list:
                processed_html.append('<ul>')
                in_list = True
            content = line[2:].strip()
            # Procesar bold
            content = content.replace('**', '<strong>').replace('**', '</strong>')
            content = content.replace('`', '<code>').replace('`', '</code>')
            processed_html.append(f'<li>{content}</li>')
        elif in_list and line.strip() == '':
            processed_html.append('</ul>')
            in_list = False
        
        # Tablas
        elif '|' in line and not line.startswith('```'):
            if not in_table:
                processed_html.append('<table>')
                in_table = True
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if i > 0 and '---' in line:
                continue
            elif i > 0 and lines[i+1].strip().startswith('|---'):
                processed_html.append('<thead><tr>')
                for cell in cells:
                    processed_html.append(f'<th>{cell}</th>')
                processed_html.append('</tr></thead><tbody>')
            else:
                processed_html.append('<tr>')
                for cell in cells:
                    cell = cell.replace('**', '<strong>').replace('**', '</strong>')
                    cell = cell.replace('`', '<code>').replace('`', '</code>')
                    processed_html.append(f'<td>{cell}</td>')
                processed_html.append('</tr>')
        elif in_table and line.strip() == '':
            processed_html.append('</tbody></table>')
            in_table = False
        
        # Texto normal
        elif line.strip() and not line.startswith('#'):
            content = line.strip()
            # Procesar bold
            import re
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            # Procesar código inline
            content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
            # Procesar enlaces
            content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
            # Procesar emojis y símbolos
            processed_html.append(f'<p>{content}</p>')
        
        elif line.strip() == '':
            if in_list:
                processed_html.append('</ul>')
                in_list = False
            if in_table:
                processed_html.append('</tbody></table>')
                in_table = False
    
    # Cerrar listas/tablas abiertas
    if in_list:
        processed_html.append('</ul>')
    if in_table:
        processed_html.append('</tbody></table>')
    
    final_html = '\n'.join(processed_html)
    
    # Template HTML completo
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📚 Presentación del Proyecto - Veterinaria Inteligente IFTS-12</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.8;
                color: #333;
                background: #f5f5f5;
                font-size: 16px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                box-shadow: 0 0 30px rgba(0,0,0,0.1);
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem 2rem 1rem 2rem;
                text-align: center;
                position: sticky;
                top: 0;
                z-index: 1000;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }}
            
            .header h1 {{
                font-size: 2rem;
                margin: 0 0 0.5rem 0;
                font-weight: 700;
            }}
            
            .header .subtitle {{
                font-size: 1rem;
                margin: 0 0 1rem 0;
                opacity: 0.95;
                font-weight: 400;
            }}
            
            .header-buttons {{
                display: flex;
                gap: 0.8rem;
                justify-content: center;
                flex-wrap: wrap;
                margin-top: 0.8rem;
            }}
            
            .content {{
                padding: 3rem;
                font-size: 16px;
            }}
            
            h1 {{
                color: #667eea;
                border-bottom: 3px solid #667eea;
                padding-bottom: 0.5rem;
                margin: 2rem 0 1rem;
                font-size: 1.75rem;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            h2 {{
                color: #764ba2;
                border-left: 5px solid #764ba2;
                padding-left: 1rem;
                margin: 2rem 0 1rem;
                font-size: 1.5rem;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            h3 {{
                color: #555;
                margin: 1.5rem 0 1rem;
                font-size: 1.25rem;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            h4 {{
                color: #666;
                margin: 1rem 0 0.5rem;
                font-size: 1.1rem;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            p {{
                margin: 1rem 0;
                text-align: justify;
                font-size: 16px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            ul {{
                margin: 1rem 0 1rem 2rem;
            }}
            
            li {{
                margin: 0.5rem 0;
                font-size: 16px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            code {{
                background: #f4f4f4;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 2px 6px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                color: #c7254e;
            }}
            
            pre {{
                background: #282c34;
                color: #abb2bf;
                padding: 1.5rem;
                border-radius: 8px;
                overflow-x: auto;
                margin: 1rem 0;
                font-family: 'Courier New', monospace;
                line-height: 1.5;
                font-size: 14px;
            }}
            
            pre code {{
                background: none;
                border: none;
                color: #abb2bf;
                padding: 0;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 1.5rem 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                font-size: 16px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            th {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1rem;
                text-align: left;
                font-weight: 600;
                font-size: 16px;
            }}
            
            td {{
                padding: 0.8rem 1rem;
                border-bottom: 1px solid #e0e0e0;
                font-size: 16px;
            }}
            
            tr:nth-child(even) {{
                background: #f9f9f9;
            }}
            
            tr:hover {{
                background: #f0f0f0;
            }}
            
            strong {{
                color: #667eea;
                font-weight: 600;
            }}
            
            a {{
                color: #667eea;
                text-decoration: none;
                border-bottom: 1px dotted #667eea;
            }}
            
            a:hover {{
                color: #764ba2;
                border-bottom: 1px solid #764ba2;
            }}
            
            .nav-buttons {{
                display: none;
            }}
            
            .btn {{
                padding: 0.6rem 1.2rem;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 600;
                font-size: 0.9rem;
                transition: all 0.3s;
                display: inline-block;
                text-align: center;
                border: none;
                cursor: pointer;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            .btn-primary {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            
            .btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }}
            
            .btn-secondary {{
                background: #6c757d;
                color: white;
            }}
            
            .btn-secondary:hover {{
                background: #5a6268;
                transform: translateY(-2px);
            }}
            
            .toc {{
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 2rem;
                margin: 2rem 0;
                border-radius: 8px;
            }}
            
            .toc h2 {{
                border: none;
                padding: 0;
                margin-bottom: 1rem;
            }}
            
            .toc ul {{
                margin-left: 1rem;
            }}
            
            @media print {{
                .header-buttons {{
                    display: none;
                }}
                
                .header {{
                    background: #667eea;
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }}
            }}
            
            @media (max-width: 768px) {{
                .content {{
                    padding: 1.5rem;
                }}
                
                h1 {{
                    font-size: 1.5rem;
                }}
                
                h2 {{
                    font-size: 1.3rem;
                }}
                
                table {{
                    font-size: 14px;
                }}
                
                .header h1 {{
                    font-size: 1.5rem;
                }}
                
                .header .subtitle {{
                    font-size: 0.9rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Proyecto IFTS-12 Veterinaria-Inteligente</h1>
                <p class="subtitle">Integrantes: A. Mercado, S. Paniagua, F. Hernández, A. Torchia</p>
                <div class="header-buttons">
                    <a href="/" class="btn btn-primary">🏠 INICIO</a>
                    <a href="/ui" class="btn btn-primary">👥 PANEL DE RECEPCIÓN</a>
                    <a href="/vet/" class="btn btn-primary">🩺 PANEL VETERINARIO</a>
                    <a href="/docs" class="btn btn-primary">📖 API DOCS</a>
                    <button onclick="window.print()" class="btn btn-secondary">🖨️ IMPRIMIR/PDF</button>
                </div>
            </div>
            
            <div class="content">
                {final_html}
            </div>
            
            <div style="background: #f8f9fa; padding: 2rem; text-align: center; border-top: 2px solid #667eea;">
                <p><strong>📚 Veterinaria Inteligente - IFTS-12</strong></p>
                <p>Documento de Presentación del Proyecto</p>
                <p>© 2025 - Desarrollado como proyecto educativo</p>
                <div style="margin-top: 1rem;">
                    <a href="/" class="btn btn-primary">⬅️ Volver al Inicio</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html)
