from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.owner import OwnerCreate, OwnerRead

router = APIRouter()


@router.post("/", response_model=OwnerRead)
def create_owner(payload: OwnerCreate, db: Session = Depends(get_db)):
    owner = models.Owner(name=payload.name, phone=payload.phone, email=payload.email)
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


@router.post("/form", response_class=HTMLResponse)
def create_owner_form(
    name: str = Form(...),
    phone: str | None = Form(None),
    email: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """Crear un dueño desde formulario HTML y mostrar confirmación."""
    owner = models.Owner(name=name, phone=phone, email=email)
    db.add(owner)
    db.commit()
    db.refresh(owner)
    
    phone_display = phone if phone else '<span style="color: #999; font-style: italic;">No especificado</span>'
    email_display = email if email else '<span style="color: #999; font-style: italic;">No especificado</span>'
    
    # Generar HTML de confirmación
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>✅ Dueño Registrado - Veterinaria Inteligente</title>
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
          max-width: 700px;
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
        .owner-card {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 2rem;
          border-radius: 12px;
          margin-bottom: 2rem;
          text-align: center;
        }}
        .owner-icon {{
          font-size: 4rem;
          margin-bottom: 1rem;
        }}
        .owner-name {{
          font-size: 2rem;
          font-weight: 700;
          margin: 0 0 0.5rem;
        }}
        .owner-id {{
          font-size: 1.2rem;
          opacity: 0.95;
          background: rgba(255, 255, 255, 0.2);
          display: inline-block;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-weight: 600;
        }}
        .contact-info {{
          background: #f8f9fa;
          border-radius: 12px;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }}
        .contact-row {{
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 1rem;
          background: white;
          border-radius: 8px;
          margin-bottom: 1rem;
          border-left: 4px solid #11998e;
        }}
        .contact-row:last-child {{
          margin-bottom: 0;
        }}
        .contact-icon {{
          font-size: 2rem;
          min-width: 40px;
        }}
        .contact-label {{
          font-weight: 700;
          color: #555;
          margin-bottom: 0.25rem;
          font-size: 0.9rem;
        }}
        .contact-value {{
          color: #333;
          font-size: 1.1rem;
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
          <h1>¡Dueño Registrado!</h1>
          <p>El dueño se agregó exitosamente al sistema</p>
        </div>
        
        <div class="content">
          <div class="owner-card">
            <div class="owner-icon">👤</div>
            <h2 class="owner-name">{owner.name}</h2>
            <span class="owner-id">ID: #{owner.id}</span>
          </div>
          
          <div class="contact-info">
            <div class="contact-row">
              <div class="contact-icon">📞</div>
              <div>
                <div class="contact-label">Teléfono</div>
                <div class="contact-value">{phone_display}</div>
              </div>
            </div>
            <div class="contact-row">
              <div class="contact-icon">📧</div>
              <div>
                <div class="contact-label">Email</div>
                <div class="contact-value">{email_display}</div>
              </div>
            </div>
          </div>
          
          <div class="next-steps">
            <h3>🎯 Próximos Pasos</h3>
            <div class="step">
              <div class="step-number">1</div>
              <div class="step-text">
                <strong>Registrar una mascota:</strong> Ahora puedes agregar las mascotas de este dueño usando el ID #{owner.id}
              </div>
            </div>
            <div class="step">
              <div class="step-number">2</div>
              <div class="step-text">
                <strong>Programar turnos:</strong> Una vez que las mascotas estén registradas, podrás agendar consultas
              </div>
            </div>
            <div class="step">
              <div class="step-number">3</div>
              <div class="step-text">
                <strong>Gestionar la información:</strong> Consulta y actualiza los datos cuando sea necesario
              </div>
            </div>
          </div>
          
          <div class="timestamp">
            <p>📅 Registrado el {owner.created_at.strftime('%d/%m/%Y a las %H:%M:%S')}</p>
          </div>
          
          <div class="actions">
            <a href="/owners/{owner.id}/view" class="btn btn-primary" target="_blank">
              👁️ Ver detalles del dueño
            </a>
            <a href="/ui" class="btn btn-success">
              ➕ Registrar otra persona
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


@router.get("/", response_model=List[OwnerRead])
def list_owners(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(models.Owner).order_by(models.Owner.id.asc())
    return q.offset((page - 1) * page_size).limit(page_size).all()


@router.get("/view", response_class=HTMLResponse)
def list_owners_view(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Vista HTML amigable de todos los dueños."""
    q = db.query(models.Owner).order_by(models.Owner.id.desc())
    total_count = q.count()
    owners = q.offset((page - 1) * page_size).limit(page_size).all()
    
    total_pages = (total_count + page_size - 1) // page_size
    
    # Generar filas de la tabla
    owner_rows = ""
    for owner in owners:
        phone_display = owner.phone if owner.phone else '<span style="color: #999;">-</span>'
        email_display = owner.email if owner.email else '<span style="color: #999;">-</span>'
        created_display = owner.created_at.strftime('%d/%m/%Y %H:%M') if owner.created_at else '-'
        
        owner_rows += f"""
        <tr>
            <td style="text-align: center; font-weight: 600;">#{owner.id}</td>
            <td><strong>{owner.name}</strong></td>
            <td>{phone_display}</td>
            <td>{email_display}</td>
            <td style="text-align: center; color: #666; font-size: 0.9rem;">{created_display}</td>
            <td style="text-align: center;">
                <div style="display: flex; gap: 0.5rem; justify-content: center;">
                    <a href="/owners/{owner.id}/view" class="btn-view" target="_blank">👁️ Ver</a>
                    <a href="/owners/{owner.id}/edit" class="btn-edit" target="_blank">✏️ Editar</a>
                    <a href="/owners/{owner.id}/delete" class="btn-delete" onclick="return confirm('¿Estás seguro de eliminar este dueño? Se eliminarán también sus mascotas y turnos.')">🗑️ Eliminar</a>
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
            <a href="/owners/view?page={prev_page}&page_size={page_size}" class="btn-page" {prev_disabled}>← Anterior</a>
            <span class="page-info">Página {page} de {total_pages} | Total: {total_count} dueños</span>
            <a href="/owners/view?page={next_page}&page_size={page_size}" class="btn-page" {next_disabled}>Siguiente →</a>
        </div>
        """
    else:
        pagination = f'<div class="pagination"><span class="page-info">Total: {total_count} dueños</span></div>'
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>👥 Listado de Dueños - Veterinaria Inteligente</title>
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
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
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
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
          box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
        }}
        .btn-edit {{
          background: linear-gradient(135deg, #f39c12 0%, #f1c40f 100%);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 6px;
          text-decoration: none;
          font-size: 0.9rem;
          font-weight: 600;
          transition: all 0.2s;
          display: inline-block;
        }}
        .btn-edit:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(243, 156, 18, 0.4);
        }}
        .btn-delete {{
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
        .btn-delete:hover {{
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
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          text-decoration: none;
          border-radius: 8px;
          font-weight: 600;
          transition: all 0.2s;
        }}
        .btn-page:hover:not([disabled]) {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
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
          <h1>👥 Listado de Dueños</h1>
          <p>Gestión de propietarios de mascotas</p>
        </header>
        
        <div class="actions">
          <a href="/ui" class="btn btn-primary">➕ Registrar nuevo dueño</a>
          <a href="/owners/search/view" class="btn btn-secondary">🔍 Búsqueda avanzada</a>
          <a href="/" class="btn btn-secondary">🏠 Ir al inicio</a>
        </div>
        
        <div class="summary">
          <div>
            <div class="count">{total_count}</div>
            <div>Dueños registrados</div>
          </div>
          <div style="text-align: right;">
            <div>Página {page} de {total_pages}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Mostrando {len(owners)} registros</div>
          </div>
        </div>
        
        {f'''
        <table>
          <thead>
            <tr>
              <th style="text-align: center;">ID</th>
              <th>Nombre</th>
              <th>Teléfono</th>
              <th>Email</th>
              <th style="text-align: center;">Registrado</th>
              <th style="text-align: center;">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {owner_rows}
          </tbody>
        </table>
        ''' if owners else '''
        <div class="empty-state">
          <div class="icon">📋</div>
          <h2>No hay dueños registrados</h2>
          <p>Comienza registrando el primer dueño en el sistema</p>
          <a href="/ui" class="btn btn-primary" style="margin-top: 1rem;">➕ Registrar dueño</a>
        </div>
        '''}
        
        {pagination}
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/search/view", response_class=HTMLResponse)
def search_owners_view(
    name: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Vista HTML de búsqueda de dueños con filtros."""
    # Construir query
    query = db.query(models.Owner)
    
    # Filtrar por nombre
    if name:
        query = query.filter(models.Owner.name.ilike(f"%{name}%"))
    
    # Filtrar por teléfono
    if phone:
        query = query.filter(models.Owner.phone.ilike(f"%{phone}%"))
    
    # Filtrar por email
    if email:
        query = query.filter(models.Owner.email.ilike(f"%{email}%"))
    
    owners = query.order_by(models.Owner.name.asc()).all()
    
    # Construir descripción de filtros
    filter_parts = []
    if name:
        filter_parts.append(f"Nombre: {name}")
    if phone:
        filter_parts.append(f"Teléfono: {phone}")
    if email:
        filter_parts.append(f"Email: {email}")
    
    filter_text = " | ".join(filter_parts) if filter_parts else "Sin filtros"
    
    # Generar HTML
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>👤 Búsqueda de Dueños - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          padding: 2rem;
          border-radius: 12px;
          margin-bottom: 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 1rem;
        }}
        .summary .count {{
          font-size: 2.5rem;
          font-weight: 700;
        }}
        .summary .info {{
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
          color: #11998e;
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
        .owners-grid {{
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
          gap: 1.5rem;
          margin-bottom: 2rem;
        }}
        .owner-card {{
          background: #f8f9fa;
          border-left: 5px solid #11998e;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          transition: transform 0.2s, box-shadow 0.2s;
        }}
        .owner-card:hover {{
          transform: translateY(-4px);
          box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        .owner-header {{
          display: flex;
          align-items: center;
          gap: 1rem;
          margin-bottom: 1rem;
          padding-bottom: 1rem;
          border-bottom: 2px solid #e0e0e0;
        }}
        .owner-icon {{
          font-size: 3rem;
        }}
        .owner-name {{
          font-size: 1.8rem;
          font-weight: 700;
          color: #333;
          margin: 0;
        }}
        .owner-id {{
          color: #11998e;
          font-size: 0.9rem;
          font-weight: 600;
          margin: 0.25rem 0 0;
        }}
        .contact-info {{
          display: grid;
          gap: 0.75rem;
          margin-bottom: 1rem;
        }}
        .contact-row {{
          display: flex;
          gap: 0.5rem;
          align-items: center;
        }}
        .contact-icon {{
          font-size: 1.2rem;
          min-width: 30px;
        }}
        .contact-value {{
          color: #333;
          font-size: 1rem;
        }}
        .pets-section {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1rem;
          border-radius: 8px;
          margin-top: 1rem;
        }}
        .pets-section h4 {{
          margin: 0 0 0.75rem;
          font-size: 1.1rem;
        }}
        .pet-item {{
          background: rgba(255, 255, 255, 0.2);
          padding: 0.5rem;
          border-radius: 6px;
          margin-bottom: 0.5rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }}
        .pet-item:last-child {{
          margin-bottom: 0;
        }}
        .actions {{
          display: flex;
          gap: 0.5rem;
          margin-top: 1rem;
        }}
        .btn {{
          padding: 0.5rem 1rem;
          border-radius: 6px;
          text-decoration: none;
          font-size: 0.9rem;
          font-weight: 600;
          transition: all 0.2s;
          display: inline-block;
          text-align: center;
          flex: 1;
        }}
        .btn-primary {{
          background: #11998e;
          color: white;
        }}
        .btn-primary:hover {{
          background: #38ef7d;
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
          <h1>👤 Búsqueda de Dueños</h1>
          <p>Resultados de la búsqueda</p>
        </header>
        
        <div class="summary">
          <div>
            <div class="count">{len(owners)}</div>
            <div>dueños encontrados</div>
          </div>
          <div class="info">
            <button class="toggle-filters" onclick="toggleFilters()">
              📋 Ver filtros aplicados
            </button>
            <div id="filters-detail" style="display: none; margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.2); border-radius: 8px; text-align: left;">
              <strong style="display: block; margin-bottom: 0.5rem;">Filtros aplicados:</strong>
              <p style="margin: 0.25rem 0;">{filter_text}</p>
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
        
        <div class="owners-grid">
    """
    
    if owners:
        for owner in owners:
            phone_display = owner.phone if owner.phone is not None else 'No especificado'
            email_display = owner.email if owner.email is not None else 'No especificado'
            
            # Obtener mascotas del dueño
            pets = owner.pets if owner.pets else []
            
            html_content += f"""
          <div class="owner-card">
            <div class="owner-header">
              <div class="owner-icon">👤</div>
              <div>
                <h2 class="owner-name">{owner.name}</h2>
                <p class="owner-id">ID: #{owner.id}</p>
              </div>
            </div>
            
            <div class="contact-info">
              <div class="contact-row">
                <span class="contact-icon">📞</span>
                <span class="contact-value">{phone_display}</span>
              </div>
              <div class="contact-row">
                <span class="contact-icon">📧</span>
                <span class="contact-value">{email_display}</span>
              </div>
            </div>
            
            <div class="pets-section">
              <h4>🐾 Mascotas ({len(pets)})</h4>
              {f'''{''.join([f'<div class="pet-item"><span>{pet.name}</span><span>{pet.species}</span></div>' for pet in pets[:5]])}''' if pets else '<p style="margin: 0; opacity: 0.8;">Sin mascotas registradas</p>'}
              {f'<p style="margin: 0.5rem 0 0; font-size: 0.9rem; opacity: 0.8;">... y {len(pets) - 5} más</p>' if len(pets) > 5 else ''}
            </div>
            
            <div class="actions">
              <a href="/owners/{owner.id}/view" class="btn btn-primary">Ver detalles completos</a>
            </div>
          </div>
            """
    else:
        html_content += """
          <div class="no-results" style="grid-column: 1 / -1;">
            <div class="no-results-icon">🔍</div>
            <p>No se encontraron dueños con los filtros seleccionados.</p>
            <p style="font-size: 1rem; color: #999;">Intenta ajustar los criterios de búsqueda.</p>
          </div>
        """
    
    html_content += """
        </div>
        
        <div style="text-align: center;">
          <a href="/vet/clinica" class="back-link">⬅️ Volver a Atención Clínica</a>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/{owner_id}/view", response_class=HTMLResponse)
def get_owner_view(owner_id: int, db: Session = Depends(get_db)):
    """Vista HTML detallada de un dueño con todas sus mascotas."""
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    phone_display = owner.phone if owner.phone else '<span style="color: #999;">No especificado</span>'
    email_display = owner.email if owner.email else '<span style="color: #999;">No especificado</span>'
    
    pets = owner.pets if owner.pets else []
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>👤 {owner.name} - Detalles del Dueño</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
        .header-id {{
          background: rgba(255, 255, 255, 0.3);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          display: inline-block;
          font-weight: 600;
        }}
        .content {{
          padding: 2rem;
        }}
        .section {{
          margin-bottom: 2rem;
        }}
        .section-title {{
          font-size: 1.5rem;
          font-weight: 700;
          color: #333;
          margin: 0 0 1.5rem;
          padding-bottom: 0.5rem;
          border-bottom: 3px solid #11998e;
        }}
        .info-grid {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1.5rem;
          margin-bottom: 2rem;
        }}
        .info-card {{
          background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
          border-left: 5px solid #11998e;
          border-radius: 8px;
          padding: 1.5rem;
        }}
        .info-label {{
          font-size: 0.9rem;
          color: #666;
          font-weight: 600;
          margin-bottom: 0.5rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }}
        .info-icon {{
          font-size: 1.5rem;
        }}
        .info-value {{
          font-size: 1.3rem;
          color: #333;
          font-weight: 700;
        }}
        .pets-grid {{
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
          gap: 1.5rem;
        }}
        .pet-card {{
          background: #f8f9fa;
          border-left: 5px solid #667eea;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          transition: transform 0.2s, box-shadow 0.2s;
        }}
        .pet-card:hover {{
          transform: translateY(-4px);
          box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        .pet-header {{
          display: flex;
          align-items: center;
          gap: 1rem;
          margin-bottom: 1rem;
          padding-bottom: 1rem;
          border-bottom: 2px solid #e0e0e0;
        }}
        .pet-icon {{
          font-size: 2.5rem;
        }}
        .pet-name {{
          font-size: 1.5rem;
          font-weight: 700;
          color: #333;
          margin: 0;
        }}
        .pet-id {{
          color: #667eea;
          font-size: 0.85rem;
          font-weight: 600;
        }}
        .pet-details {{
          display: grid;
          gap: 0.5rem;
          margin-bottom: 1rem;
        }}
        .pet-detail-row {{
          display: flex;
          justify-content: space-between;
          padding: 0.5rem;
          background: white;
          border-radius: 4px;
        }}
        .pet-detail-label {{
          color: #666;
          font-weight: 600;
        }}
        .pet-detail-value {{
          color: #333;
        }}
        .pet-actions {{
          display: flex;
          gap: 0.5rem;
        }}
        .btn {{
          padding: 0.5rem 1rem;
          border-radius: 6px;
          text-decoration: none;
          font-size: 0.9rem;
          font-weight: 600;
          transition: all 0.2s;
          display: inline-block;
          text-align: center;
          flex: 1;
        }}
        .btn-primary {{
          background: #667eea;
          color: white;
        }}
        .btn-primary:hover {{
          background: #764ba2;
        }}
        .btn-secondary {{
          background: #11998e;
          color: white;
        }}
        .btn-secondary:hover {{
          background: #38ef7d;
        }}
        .no-pets {{
          text-align: center;
          padding: 3rem;
          color: #666;
          background: #f8f9fa;
          border-radius: 8px;
        }}
        .no-pets-icon {{
          font-size: 4rem;
          margin-bottom: 1rem;
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
          border-radius: 8px;
          text-align: center;
        }}
        .stat-value {{
          font-size: 3rem;
          font-weight: 700;
          margin: 0;
        }}
        .stat-label {{
          margin: 0.5rem 0 0;
          opacity: 0.9;
        }}
        .back-link {{
          display: inline-block;
          margin-top: 2rem;
          padding: 0.75rem 1.5rem;
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          text-decoration: none;
          border-radius: 8px;
          font-weight: 600;
          transition: transform 0.2s;
        }}
        .back-link:hover {{
          transform: translateY(-2px);
        }}
        .timestamp {{
          color: #999;
          font-size: 0.85rem;
          text-align: center;
          margin-top: 2rem;
          padding-top: 1rem;
          border-top: 1px solid #e0e0e0;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="header-icon">👤</div>
          <h1>{owner.name}</h1>
          <span class="header-id">ID: #{owner.id}</span>
        </div>
        
        <div class="content">
          <div class="section">
            <h2 class="section-title">📋 Información de Contacto</h2>
            <div class="info-grid">
              <div class="info-card">
                <div class="info-label">
                  <span class="info-icon">📞</span>
                  Teléfono
                </div>
                <div class="info-value">{phone_display}</div>
              </div>
              
              <div class="info-card">
                <div class="info-label">
                  <span class="info-icon">📧</span>
                  Email
                </div>
                <div class="info-value">{email_display}</div>
              </div>
            </div>
          </div>
          
          <div class="section">
            <h2 class="section-title">📊 Estadísticas</h2>
            <div class="stats">
              <div class="stat-card">
                <div class="stat-value">{len(pets)}</div>
                <div class="stat-label">Mascotas</div>
              </div>
            </div>
          </div>
          
          <div class="section">
            <h2 class="section-title">🐾 Mascotas</h2>
    """
    
    if pets:
        html_content += '<div class="pets-grid">'
        for pet in pets:
            breed_display = pet.breed if pet.breed else 'No especificado'
            age_display = f"{pet.age} años" if pet.age is not None else 'No especificado'
            
            html_content += f"""
            <div class="pet-card">
              <div class="pet-header">
                <div class="pet-icon">{'🐕' if pet.species == 'perro' else '🐱' if pet.species == 'gato' else '🐾'}</div>
                <div>
                  <h3 class="pet-name">{pet.name}</h3>
                  <div class="pet-id">ID: #{pet.id}</div>
                </div>
              </div>
              
              <div class="pet-details">
                <div class="pet-detail-row">
                  <span class="pet-detail-label">Especie:</span>
                  <span class="pet-detail-value">{pet.species.title()}</span>
                </div>
                <div class="pet-detail-row">
                  <span class="pet-detail-label">Raza:</span>
                  <span class="pet-detail-value">{breed_display}</span>
                </div>
                <div class="pet-detail-row">
                  <span class="pet-detail-label">Edad:</span>
                  <span class="pet-detail-value">{age_display}</span>
                </div>
              </div>
              
              <div class="pet-actions">
                <a href="/pets/{pet.id}/view" class="btn btn-primary">Ver Detalles</a>
                <a href="/pets/{pet.id}/clinical-history" class="btn btn-secondary">Historia Clínica</a>
              </div>
            </div>
            """
        html_content += '</div>'
    else:
        html_content += """
          <div class="no-pets">
            <div class="no-pets-icon">🐾</div>
            <p style="font-size: 1.2rem; margin: 0;">Este dueño no tiene mascotas registradas</p>
            <p style="color: #999; margin: 0.5rem 0 0;">Puedes agregar mascotas desde el panel de administración</p>
          </div>
        """
    
    html_content += f"""
          </div>
          
          <div class="timestamp">
            <p>📅 Registrado: {owner.created_at.strftime('%d/%m/%Y %H:%M') if owner.created_at else 'N/A'}</p>
            <p>🔄 Última actualización: {owner.updated_at.strftime('%d/%m/%Y %H:%M') if owner.updated_at else 'N/A'}</p>
          </div>
          
          <div style="text-align: center;">
            <a href="/owners/search/view" class="back-link">⬅️ Volver a la búsqueda</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/{owner_id}", response_model=OwnerRead)
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner


@router.get("/{owner_id}/edit", response_class=HTMLResponse)
def edit_owner_form(owner_id: int, db: Session = Depends(get_db)):
    """Formulario HTML para editar un dueño."""
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>✏️ Editar Dueño - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #f39c12 0%, #f1c40f 100%);
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
          background: linear-gradient(135deg, #f39c12 0%, #f1c40f 100%);
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
        .form-group {{
          margin-bottom: 1.5rem;
        }}
        label {{
          display: block;
          font-weight: 600;
          margin-bottom: 0.5rem;
          color: #333;
        }}
        input[type="text"],
        input[type="tel"],
        input[type="email"] {{
          width: 100%;
          padding: 0.75rem;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 1rem;
          transition: border-color 0.3s;
        }}
        input:focus {{
          outline: none;
          border-color: #f39c12;
        }}
        .required {{
          color: #e74c3c;
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
        }}
        .btn-primary {{
          background: linear-gradient(135deg, #f39c12 0%, #f1c40f 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(243, 156, 18, 0.4);
        }}
        .btn-secondary {{
          background: #6c757d;
          color: white;
        }}
        .btn-secondary:hover {{
          background: #5a6268;
          transform: translateY(-2px);
        }}
        .info-box {{
          background: #fff3cd;
          border-left: 4px solid #f39c12;
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 1.5rem;
        }}
        .info-box p {{
          margin: 0;
          color: #856404;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>✏️ Editar Dueño</h1>
          <p>ID: #{owner.id} - {owner.name}</p>
        </div>
        
        <div class="content">
          <div class="info-box">
            <p><strong>📝 Instrucciones:</strong> Modifica los datos que necesites actualizar y presiona "Guardar Cambios".</p>
          </div>
          
          <form method="POST" action="/owners/{owner.id}/update">
            <div class="form-group">
              <label>Nombre Completo <span class="required">*</span></label>
              <input type="text" name="name" value="{owner.name}" required />
            </div>
            
            <div class="form-group">
              <label>Teléfono</label>
              <input type="tel" name="phone" value="{owner.phone or ''}" placeholder="Ej: +54 11 1234-5678" />
            </div>
            
            <div class="form-group">
              <label>Email</label>
              <input type="email" name="email" value="{owner.email or ''}" placeholder="ejemplo@correo.com" />
            </div>
            
            <div class="actions">
              <button type="submit" class="btn btn-primary">💾 Guardar Cambios</button>
              <a href="/owners/view" class="btn btn-secondary" style="text-align: center; text-decoration: none; display: flex; align-items: center; justify-content: center;">❌ Cancelar</a>
            </div>
          </form>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.post("/{owner_id}/update", response_class=HTMLResponse)
def update_owner(
    owner_id: int,
    name: str = Form(...),
    phone: str | None = Form(None),
    email: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """Actualizar un dueño desde formulario HTML."""
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    # Actualizar campos
    owner.name = name
    owner.phone = phone if phone else None
    owner.email = email if email else None
    
    db.commit()
    db.refresh(owner)
    
    # Página de confirmación
    phone_display = phone if phone else '<span style="color: #999;">No especificado</span>'
    email_display = email if email else '<span style="color: #999;">No especificado</span>'
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>✅ Dueño Actualizado - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
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
          background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
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
        .content {{
          padding: 2rem;
        }}
        .owner-card {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 2rem;
          border-radius: 12px;
          margin-bottom: 2rem;
          text-align: center;
        }}
        .owner-name {{
          font-size: 2rem;
          font-weight: 700;
          margin: 0 0 0.5rem;
        }}
        .owner-id {{
          background: rgba(255, 255, 255, 0.2);
          display: inline-block;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-weight: 600;
        }}
        .contact-info {{
          background: #f8f9fa;
          border-radius: 12px;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }}
        .contact-row {{
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 1rem;
          background: white;
          border-radius: 8px;
          margin-bottom: 1rem;
          border-left: 4px solid #27ae60;
        }}
        .contact-row:last-child {{ margin-bottom: 0; }}
        .contact-label {{
          font-weight: 700;
          color: #555;
          margin-bottom: 0.25rem;
          font-size: 0.9rem;
        }}
        .contact-value {{
          color: #333;
          font-size: 1.1rem;
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
          <div class="success-icon">✅</div>
          <h1>¡Dueño Actualizado!</h1>
          <p>Los cambios se guardaron exitosamente</p>
        </div>
        
        <div class="content">
          <div class="owner-card">
            <div class="owner-icon" style="font-size: 4rem;">👤</div>
            <h2 class="owner-name">{owner.name}</h2>
            <span class="owner-id">ID: #{owner.id}</span>
          </div>
          
          <div class="contact-info">
            <div class="contact-row">
              <div style="font-size: 2rem;">📞</div>
              <div>
                <div class="contact-label">Teléfono</div>
                <div class="contact-value">{phone_display}</div>
              </div>
            </div>
            <div class="contact-row">
              <div style="font-size: 2rem;">📧</div>
              <div>
                <div class="contact-label">Email</div>
                <div class="contact-value">{email_display}</div>
              </div>
            </div>
          </div>
          
          <div class="actions">
            <a href="/owners/{owner.id}/view" class="btn btn-primary">👁️ Ver detalles</a>
            <a href="/owners/view" class="btn btn-secondary">📋 Listado de dueños</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/{owner_id}/delete", response_class=HTMLResponse)
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    """Eliminar un dueño y todos sus registros relacionados."""
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    # Contar registros relacionados
    pets_count = len(owner.pets) if owner.pets else 0
    
    # Guardar info antes de eliminar
    owner_name = owner.name
    owner_id_saved = owner.id
    
    # Eliminar (cascade eliminará mascotas, turnos, etc.)
    db.delete(owner)
    db.commit()
    
    # Página de confirmación
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>🗑️ Dueño Eliminado - Veterinaria Inteligente</title>
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
          animation: slideIn 0.5s ease-out;
        }}
        @keyframes slideIn {{
          from {{ opacity: 0; transform: translateY(-30px); }}
          to {{ opacity: 1; transform: translateY(0); }}
        }}
        .header {{
          background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
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
        .warning-box {{
          background: #fff3cd;
          border-left: 4px solid #f39c12;
          padding: 1.5rem;
          border-radius: 8px;
          margin-bottom: 2rem;
        }}
        .warning-box h3 {{
          margin: 0 0 1rem;
          color: #856404;
        }}
        .warning-box ul {{
          margin: 0;
          padding-left: 1.5rem;
          color: #856404;
        }}
        .deleted-info {{
          background: #f8f9fa;
          padding: 1.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
        }}
        .deleted-info h3 {{
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
        .btn {{
          width: 100%;
          padding: 1rem 1.5rem;
          border-radius: 10px;
          text-decoration: none;
          font-weight: 600;
          font-size: 1rem;
          transition: all 0.2s;
          display: inline-block;
          text-align: center;
          background: #6c757d;
          color: white;
        }}
        .btn:hover {{
          background: #5a6268;
          transform: translateY(-3px);
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="icon">🗑️</div>
          <h1>Dueño Eliminado</h1>
          <p>El registro se eliminó permanentemente del sistema</p>
        </div>
        
        <div class="content">
          <div class="warning-box">
            <h3>⚠️ Registros Eliminados</h3>
            <ul>
              <li>Dueño: {owner_name}</li>
              <li>Mascotas asociadas: {pets_count}</li>
              <li>Todos los turnos y registros clínicos relacionados</li>
            </ul>
          </div>
          
          <div class="deleted-info">
            <h3>📋 Información del Registro Eliminado</h3>
            <div class="info-row">
              <strong>ID:</strong>
              <span>#{owner_id_saved}</span>
            </div>
            <div class="info-row">
              <strong>Nombre:</strong>
              <span>{owner_name}</span>
            </div>
            <div class="info-row">
              <strong>Mascotas:</strong>
              <span>{pets_count}</span>
            </div>
          </div>
          
          <a href="/owners/view" class="btn">📋 Volver al listado de dueños</a>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content

