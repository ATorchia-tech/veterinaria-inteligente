from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Form
from fastapi.responses import HTMLResponse
from datetime import date
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


@router.post("/form", response_class=HTMLResponse)
def create_pet_form(
    name: str = Form(...),
    species: str = Form(...),
    breed: str | None = Form(None),
    birth_date: date | None = Form(None),
    notes: str | None = Form(None),
    owner_id: int = Form(...),
    db: Session = Depends(get_db),
):
    """Crear una mascota desde formulario HTML y mostrar confirmación."""
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    pet = models.Pet(
        name=name,
        species=species,
        breed=breed,
        birth_date=birth_date,
        notes=notes,
        owner_id=owner_id,
    )
    db.add(pet)
    db.commit()
    db.refresh(pet)
    
    # Emoji según especie
    species_lower = species.lower()
    if 'perro' in species_lower or 'dog' in species_lower:
        species_emoji = '🐕'
    elif 'gato' in species_lower or 'cat' in species_lower:
        species_emoji = '🐈'
    elif 'ave' in species_lower or 'pájaro' in species_lower or 'bird' in species_lower:
        species_emoji = '🦜'
    elif 'conejo' in species_lower or 'rabbit' in species_lower:
        species_emoji = '🐰'
    elif 'hámster' in species_lower or 'hamster' in species_lower:
        species_emoji = '🐹'
    else:
        species_emoji = '🐾'
    
    breed_display = breed if breed else '<span style="color: #999; font-style: italic;">No especificado</span>'
    birth_display = birth_date.strftime('%d/%m/%Y') if birth_date else '<span style="color: #999; font-style: italic;">No especificado</span>'
    notes_display = notes if notes else '<span style="color: #999; font-style: italic;">Sin notas adicionales</span>'
    
    # Generar HTML de confirmación
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>✅ Mascota Registrada - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 2rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        .pet-card {{
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          padding: 2rem;
          border-radius: 12px;
          margin-bottom: 2rem;
          display: flex;
          align-items: center;
          gap: 2rem;
        }}
        .pet-icon {{
          font-size: 6rem;
        }}
        .pet-info {{
          flex: 1;
        }}
        .pet-name {{
          font-size: 2.5rem;
          font-weight: 700;
          margin: 0 0 0.5rem;
        }}
        .pet-species {{
          font-size: 1.2rem;
          opacity: 0.95;
          margin: 0 0 1rem;
        }}
        .pet-id {{
          background: rgba(255, 255, 255, 0.2);
          display: inline-block;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-weight: 600;
        }}
        .details-grid {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1rem;
          margin-bottom: 2rem;
        }}
        .detail-card {{
          background: #f8f9fa;
          border-left: 4px solid #667eea;
          border-radius: 8px;
          padding: 1.5rem;
        }}
        .detail-label {{
          font-weight: 700;
          color: #555;
          margin-bottom: 0.5rem;
          font-size: 0.9rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }}
        .detail-icon {{
          font-size: 1.3rem;
        }}
        .detail-value {{
          color: #333;
          font-size: 1.1rem;
          line-height: 1.6;
        }}
        .owner-section {{
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
          padding: 1.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
        }}
        .owner-section h3 {{
          margin: 0 0 1rem;
          font-size: 1.5rem;
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
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
          <h1>¡Mascota Registrada!</h1>
          <p>La mascota se agregó exitosamente al sistema</p>
        </div>
        
        <div class="content">
          <div class="pet-card">
            <div class="pet-icon">{species_emoji}</div>
            <div class="pet-info">
              <h2 class="pet-name">{pet.name}</h2>
              <p class="pet-species">{pet.species.title()}</p>
              <span class="pet-id">ID: #{pet.id}</span>
            </div>
          </div>
          
          <div class="details-grid">
            <div class="detail-card">
              <div class="detail-label">
                <span class="detail-icon">🏷️</span>
                Raza
              </div>
              <div class="detail-value">{breed_display}</div>
            </div>
            <div class="detail-card">
              <div class="detail-label">
                <span class="detail-icon">🎂</span>
                Fecha de Nacimiento
              </div>
              <div class="detail-value">{birth_display}</div>
            </div>
          </div>
          
          <div class="detail-card" style="margin-bottom: 2rem;">
            <div class="detail-label">
              <span class="detail-icon">📝</span>
              Notas Adicionales
            </div>
            <div class="detail-value">{notes_display}</div>
          </div>
          
          <div class="owner-section">
            <h3>👤 Dueño</h3>
            <div class="owner-info">
              <div><strong>Nombre:</strong> {owner.name}</div>
              <div><strong>ID:</strong> #{owner.id}</div>
              {f'<div><strong>Teléfono:</strong> {owner.phone}</div>' if owner.phone else ''}
              {f'<div><strong>Email:</strong> {owner.email}</div>' if owner.email else ''}
            </div>
          </div>
          
          <div class="next-steps">
            <h3>🎯 Próximos Pasos</h3>
            <div class="step">
              <div class="step-number">1</div>
              <div class="step-text">
                <strong>Programar turnos:</strong> Ahora puedes agendar consultas veterinarias para {pet.name}
              </div>
            </div>
            <div class="step">
              <div class="step-number">2</div>
              <div class="step-text">
                <strong>Registrar atenciones:</strong> Lleva un historial clínico completo de cada visita
              </div>
            </div>
            <div class="step">
              <div class="step-number">3</div>
              <div class="step-text">
                <strong>Gestionar vacunas:</strong> Mantén al día el calendario de vacunación
              </div>
            </div>
          </div>
          
          <div class="timestamp">
            <p>📅 Registrado el {pet.created_at.strftime('%d/%m/%Y a las %H:%M:%S')}</p>
          </div>
          
          <div class="actions">
            <a href="/pets/{pet.id}/view" class="btn btn-primary" target="_blank">
              👁️ Ver detalles de {pet.name}
            </a>
            <a href="/ui" class="btn btn-success">
              ➕ Registrar otra mascota
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


@router.get("/", response_model=List[PetRead])
def list_pets(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(models.Pet).order_by(models.Pet.id.asc())
    return q.offset((page - 1) * page_size).limit(page_size).all()


@router.get("/view", response_class=HTMLResponse)
def list_pets_view(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Vista HTML amigable de todas las mascotas."""
    q = db.query(models.Pet).order_by(models.Pet.id.desc())
    total_count = q.count()
    pets = q.offset((page - 1) * page_size).limit(page_size).all()
    
    total_pages = (total_count + page_size - 1) // page_size
    
    # Generar filas de la tabla
    pet_rows = ""
    for pet in pets:
        # Emoji según especie
        species_lower = pet.species.lower()
        if 'perro' in species_lower or 'dog' in species_lower:
            species_emoji = '🐕'
        elif 'gato' in species_lower or 'cat' in species_lower:
            species_emoji = '🐈'
        elif 'ave' in species_lower or 'pájaro' in species_lower or 'bird' in species_lower:
            species_emoji = '🦜'
        elif 'conejo' in species_lower or 'rabbit' in species_lower:
            species_emoji = '🐰'
        elif 'hámster' in species_lower or 'hamster' in species_lower:
            species_emoji = '🐹'
        else:
            species_emoji = '🐾'
        
        breed_display = pet.breed if pet.breed else '<span style="color: #999;">-</span>'
        birth_display = pet.birth_date.strftime('%d/%m/%Y') if pet.birth_date else '<span style="color: #999;">-</span>'
        owner_name = pet.owner.name if pet.owner else '<span style="color: #999;">Sin dueño</span>'
        
        pet_rows += f"""
        <tr>
            <td style="text-align: center; font-weight: 600;">#{pet.id}</td>
            <td><span style="font-size: 1.5rem; margin-right: 0.5rem;">{species_emoji}</span><strong>{pet.name}</strong></td>
            <td>{pet.species.title()}</td>
            <td>{breed_display}</td>
            <td style="text-align: center;">{birth_display}</td>
            <td>{owner_name}</td>
            <td style="text-align: center;">
                <div style="display: flex; gap: 0.5rem; justify-content: center;">
                    <a href="/pets/{pet.id}/view" class="btn-view" target="_blank">👁️ Ver</a>
                    <a href="/pets/{pet.id}/edit" class="btn-edit" target="_blank">✏️ Editar</a>
                    <a href="/pets/{pet.id}/delete" class="btn-delete" onclick="return confirm('¿Estás seguro de eliminar esta mascota? Se eliminarán también sus turnos y registros clínicos.')">🗑️ Eliminar</a>
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
            <a href="/pets/view?page={prev_page}&page_size={page_size}" class="btn-page" {prev_disabled}>← Anterior</a>
            <span class="page-info">Página {page} de {total_pages} | Total: {total_count} mascotas</span>
            <a href="/pets/view?page={next_page}&page_size={page_size}" class="btn-page" {next_disabled}>Siguiente →</a>
        </div>
        """
    else:
        pagination = f'<div class="pagination"><span class="page-info">Total: {total_count} mascotas</span></div>'
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>🐾 Listado de Mascotas - Veterinaria Inteligente</title>
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          text-decoration: none;
          border-radius: 8px;
          font-weight: 600;
          transition: all 0.2s;
        }}
        .btn-page:hover:not([disabled]) {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
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
          <h1>🐾 Listado de Mascotas</h1>
          <p>Gestión de pacientes veterinarios</p>
        </header>
        
        <div class="actions">
          <a href="/ui" class="btn btn-primary">➕ Registrar nueva mascota</a>
          <a href="/pets/search/view" class="btn btn-secondary">🔍 Búsqueda avanzada</a>
          <a href="/" class="btn btn-secondary">🏠 Ir al inicio</a>
        </div>
        
        <div class="summary">
          <div>
            <div class="count">{total_count}</div>
            <div>Mascotas registradas</div>
          </div>
          <div style="text-align: right;">
            <div>Página {page} de {total_pages}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Mostrando {len(pets)} registros</div>
          </div>
        </div>
        
        {f'''
        <table>
          <thead>
            <tr>
              <th style="text-align: center;">ID</th>
              <th>Nombre</th>
              <th>Especie</th>
              <th>Raza</th>
              <th style="text-align: center;">Nacimiento</th>
              <th>Dueño</th>
              <th style="text-align: center;">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {pet_rows}
          </tbody>
        </table>
        ''' if pets else '''
        <div class="empty-state">
          <div class="icon">🐾</div>
          <h2>No hay mascotas registradas</h2>
          <p>Comienza registrando la primera mascota en el sistema</p>
          <a href="/ui" class="btn btn-primary" style="margin-top: 1rem;">➕ Registrar mascota</a>
        </div>
        '''}
        
        {pagination}
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/search/view", response_class=HTMLResponse)
def search_pets_view(
    name: Optional[str] = Query(None),
    species: Optional[str] = Query(None),
    owner_name: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Vista HTML de búsqueda de mascotas con filtros."""
    # Construir query
    query = db.query(models.Pet)
    
    # Filtrar por nombre de mascota
    if name:
        query = query.filter(models.Pet.name.ilike(f"%{name}%"))
    
    # Filtrar por especie
    if species:
        query = query.filter(models.Pet.species.ilike(f"%{species}%"))
    
    # Filtrar por nombre de dueño
    if owner_name:
        query = query.join(models.Owner).filter(models.Owner.name.ilike(f"%{owner_name}%"))
    
    pets = query.order_by(models.Pet.name.asc()).all()
    
    # Construir descripción de filtros
    filter_parts = []
    if name:
        filter_parts.append(f"Nombre: {name}")
    if species:
        filter_parts.append(f"Especie: {species}")
    if owner_name:
        filter_parts.append(f"Dueño: {owner_name}")
    
    filter_text = " | ".join(filter_parts) if filter_parts else "Sin filtros"
    
    # Generar HTML
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>🐾 Búsqueda de Mascotas - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 0;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          height: 100vh;
          overflow: hidden;
        }}
        .container {{
          height: 100vh;
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }}
        header {{
          text-align: center;
          padding: 0.8rem 1rem;
          background: rgba(255,255,255,0.98);
          border-bottom: 2px solid #e2e8f0;
          flex-shrink: 0;
        }}
        header h1 {{
          margin: 0;
          font-size: 2rem;
          color: #333;
          font-weight: 700;
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
        }}
        header p {{
          margin: 0.3rem 0 0;
          color: #666;
          font-size: 0.95rem;
        }}
        .summary {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1rem 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-shrink: 0;
        }}
        .summary .count {{
          font-size: 2.5rem;
          font-weight: 700;
        }}
        .summary .label {{
          font-size: 1rem;
        }}
        .main-content {{
          flex: 1;
          overflow-y: auto;
          padding: 1rem;
          background: rgba(255,255,255,0.95);
        }}
        .pets-grid {{
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
          gap: 1rem;
          max-width: 1400px;
          margin: 0 auto;
        }}
        .pet-card {{
          background: #f8f9fa;
          border-left: 4px solid #667eea;
          border-radius: 8px;
          padding: 1rem;
          box-shadow: 0 2px 6px rgba(0,0,0,0.1);
          transition: transform 0.2s, box-shadow 0.2s;
        }}
        .pet-card:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .pet-header {{
          display: flex;
          align-items: center;
          gap: 0.8rem;
          margin-bottom: 0.8rem;
          padding-bottom: 0.8rem;
          border-bottom: 2px solid #e0e0e0;
        }}
        .pet-icon {{
          font-size: 2.5rem;
        }}
        .pet-name {{
          font-size: 1.4rem;
          font-weight: 700;
          color: #333;
          margin: 0;
        }}
        .pet-species {{
          color: #667eea;
          font-size: 0.9rem;
          font-weight: 600;
          margin: 0.2rem 0 0;
        }}
        .pet-info {{
          display: grid;
          gap: 0.5rem;
          margin-bottom: 0.8rem;
        }}
        .info-row {{
          display: flex;
          gap: 0.5rem;
          align-items: flex-start;
          font-size: 0.85rem;
        }}
        .info-label {{
          font-weight: 600;
          color: #555;
          min-width: 75px;
        }}
        .info-value {{
          color: #333;
        }}
        .owner-section {{
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          padding: 0.8rem;
          border-radius: 6px;
          margin-bottom: 0.8rem;
          font-size: 0.85rem;
        }}
        .owner-section h4 {{
          margin: 0 0 0.4rem;
          font-size: 1rem;
        }}
        .owner-section p {{
          margin: 0.25rem 0;
        }}
        .actions {{
          display: flex;
          gap: 0.5rem;
        }}
        .btn {{
          padding: 0.5rem 0.9rem;
          border-radius: 6px;
          text-decoration: none;
          font-size: 0.85rem;
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
        .btn-success {{
          background: #11998e;
          color: white;
        }}
        .btn-success:hover {{
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
        .footer {{
          text-align: center;
          padding: 0.8rem;
          background: rgba(255,255,255,0.95);
          border-top: 1px solid #e2e8f0;
          flex-shrink: 0;
        }}
        .back-link {{
          display: inline-block;
          padding: 0.6rem 1.5rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          text-decoration: none;
          border-radius: 8px;
          font-weight: 600;
          font-size: 0.95rem;
          transition: transform 0.2s;
        }}
        .back-link:hover {{
          transform: translateY(-1px);
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <header>
          <h1>🐾 Búsqueda de Mascotas</h1>
          <p>Resultados de la búsqueda</p>
        </header>
        
        <div class="summary">
          <div>
            <div class="count">{len(pets)}</div>
            <div class="label">mascotas encontradas</div>
          </div>
        </div>
        
        <div class="main-content">
          <div class="pets-grid">
    """
    
    if pets:
        for pet in pets:
            # Emoji de especie
            species_lower = pet.species.lower()
            if 'perro' in species_lower or 'dog' in species_lower:
                species_emoji = '🐕'
            elif 'gato' in species_lower or 'cat' in species_lower:
                species_emoji = '🐈'
            elif 'ave' in species_lower or 'pájaro' in species_lower or 'bird' in species_lower:
                species_emoji = '🦜'
            elif 'conejo' in species_lower or 'rabbit' in species_lower:
                species_emoji = '🐰'
            elif 'hámster' in species_lower or 'hamster' in species_lower:
                species_emoji = '🐹'
            else:
                species_emoji = '🐾'
            
            # Calcular edad si hay fecha de nacimiento
            age_text = ""
            if pet.birth_date is not None:
                from datetime import datetime
                today = datetime.now().date()
                age_years = (today - pet.birth_date).days // 365
                age_text = f" - {age_years} años" if age_years >= 1 else " - Menos de 1 año"
            
            breed_text = pet.breed if pet.breed is not None else "No especificado"
            notes_html = f'<div class="info-row"><span class="info-label">📝 Notas:</span><span class="info-value">{pet.notes}</span></div>' if pet.notes is not None else ''
            
            owner_phone = pet.owner.phone if pet.owner.phone else 'No especificado'
            owner_email = pet.owner.email if pet.owner.email else 'No especificado'
            
            html_content += f"""
            <div class="pet-card">
              <div class="pet-header">
                <div class="pet-icon">{species_emoji}</div>
                <div>
                  <h2 class="pet-name">{pet.name}</h2>
                  <p class="pet-species">{pet.species} - {breed_text}</p>
                </div>
              </div>
              
              <div class="pet-info">
                <div class="info-row">
                  <span class="info-label">🆔 ID:</span>
                  <span class="info-value">#{pet.id}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">🎂 Nacimiento:</span>
                  <span class="info-value">{pet.birth_date.strftime('%d/%m/%Y') if pet.birth_date is not None else 'No especificado'}{age_text}</span>
                </div>
                {notes_html}
              </div>
              
              <div class="owner-section">
                <h4>👤 Dueño: {pet.owner.name}</h4>
                <p><strong>📞 Teléfono:</strong> {owner_phone}</p>
                <p><strong>📧 Email:</strong> {owner_email}</p>
              </div>
              
              <div class="actions">
                <a href="/pets/{pet.id}/view" class="btn btn-primary" target="_blank">👁️ Ver detalles</a>
                <a href="/pets/{pet.id}/clinical-history" class="btn btn-success" target="_blank">📋 Historia clínica</a>
              </div>
            </div>
            """
    else:
        html_content += """
            <div class="no-results" style="grid-column: 1 / -1;">
              <div class="no-results-icon">🔍</div>
              <p>No se encontraron mascotas con los filtros seleccionados.</p>
              <p style="font-size: 0.95rem; color: #999;">Intenta ajustar los criterios de búsqueda.</p>
            </div>
        """
    
    html_content += """
          </div>
        </div>
        
        <div class="footer">
          <a href="/vet/clinica" class="back-link">⬅️ Volver a Atención Clínica</a>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/{pet_id}", response_model=PetRead)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.get("/{pet_id}/view", response_class=HTMLResponse)
def get_pet_view(pet_id: int, db: Session = Depends(get_db)):
    """Vista HTML detallada de una mascota."""
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    # Calcular edad
    if pet.birth_date is not None:
        from datetime import datetime
        today = datetime.now().date()
        age_years = (today - pet.birth_date).days // 365
        age_text = f"{age_years} años" if age_years >= 1 else "Menos de 1 año"
        birth_display = f"{pet.birth_date.strftime('%d/%m/%Y')} ({age_text})"
    else:
        birth_display = "No especificado"
    
    breed_display = pet.breed if pet.breed is not None else "No especificado"
    notes_display = pet.notes if pet.notes is not None else "Sin notas"
    
    # Emoji de especie
    species_lower = pet.species.lower()
    if 'perro' in species_lower or 'dog' in species_lower:
        species_emoji = '🐕'
    elif 'gato' in species_lower or 'cat' in species_lower:
        species_emoji = '🐈'
    elif 'ave' in species_lower or 'pájaro' in species_lower or 'bird' in species_lower:
        species_emoji = '🦜'
    elif 'conejo' in species_lower or 'rabbit' in species_lower:
        species_emoji = '🐰'
    elif 'hámster' in species_lower or 'hamster' in species_lower:
        species_emoji = '🐹'
    else:
        species_emoji = '🐾'
    
    # Obtener récords clínicos
    records = pet.clinical_records if pet.clinical_records else []
    
    # Obtener vacunas
    vaccinations = pet.vaccinations if pet.vaccinations else []
    
    # Obtener turnos
    appointments = pet.appointments if pet.appointments else []
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>{species_emoji} {pet.name} - Detalles - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 0;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          height: 100vh;
          overflow: hidden;
        }}
        .container {{
          height: 100vh;
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }}
        header {{
          text-align: center;
          padding: 0.8rem 1rem;
          background: rgba(255,255,255,0.98);
          border-bottom: 2px solid #e2e8f0;
          flex-shrink: 0;
        }}
        header h1 {{
          margin: 0;
          font-size: 2rem;
          color: #333;
          font-weight: 700;
        }}
        .pet-header {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1rem 1.5rem;
          display: flex;
          align-items: center;
          gap: 1rem;
          flex-shrink: 0;
        }}
        .pet-icon {{
          font-size: 3rem;
        }}
        .pet-info h2 {{
          margin: 0;
          font-size: 1.8rem;
        }}
        .pet-id {{
          opacity: 0.9;
          font-size: 0.85rem;
          margin-top: 0.2rem;
        }}
        .main-content {{
          flex: 1;
          overflow-y: auto;
          padding: 1rem;
          background: rgba(255,255,255,0.95);
        }}
        .info-grid {{
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1rem;
          margin-bottom: 1rem;
          max-width: 1200px;
          margin-left: auto;
          margin-right: auto;
        }}
        .info-card {{
          background: #f8f9fa;
          border-left: 4px solid #667eea;
          border-radius: 8px;
          padding: 1rem;
          box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }}
        .info-card h3 {{
          margin: 0 0 0.7rem;
          color: #667eea;
          font-size: 1.1rem;
        }}
        .info-row {{
          display: flex;
          gap: 0.4rem;
          margin-bottom: 0.5rem;
          align-items: flex-start;
          font-size: 0.85rem;
        }}
        .info-label {{
          font-weight: 600;
          color: #555;
          min-width: 90px;
        }}
        .info-value {{
          color: #333;
          flex: 1;
        }}
        .owner-section {{
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 1rem;
          max-width: 1200px;
          margin-left: auto;
          margin-right: auto;
        }}
        .owner-section h3 {{
          margin: 0 0 0.6rem;
          font-size: 1.1rem;
        }}
        .owner-section > div {{
          display: grid;
          gap: 0.4rem;
          font-size: 0.85rem;
        }}
        .section {{
          margin-bottom: 1rem;
          max-width: 1200px;
          margin-left: auto;
          margin-right: auto;
        }}
        .section h3 {{
          color: #333;
          font-size: 1.2rem;
          margin-bottom: 0.7rem;
          padding-bottom: 0.4rem;
          border-bottom: 2px solid #e0e0e0;
        }}
        .list-item {{
          background: #f8f9fa;
          padding: 0.8rem;
          border-radius: 8px;
          margin-bottom: 0.7rem;
          border-left: 4px solid #667eea;
          box-shadow: 0 2px 4px rgba(0,0,0,0.08);
          transition: all 0.2s;
        }}
        .list-item:hover {{
          transform: translateX(2px);
          box-shadow: 0 3px 8px rgba(0,0,0,0.12);
        }}
        .list-item-title {{
          font-weight: 700;
          color: #333;
          margin-bottom: 0.4rem;
          font-size: 0.95rem;
        }}
        .list-item-text {{
          color: #666;
          font-size: 0.8rem;
          line-height: 1.5;
        }}
        .badge {{
          display: inline-block;
          padding: 0.25rem 0.6rem;
          border-radius: 12px;
          font-size: 0.75rem;
          font-weight: 600;
          margin-right: 0.4rem;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .badge-success {{ 
          background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
          color: #155724;
        }}
        .badge-warning {{ 
          background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
          color: #856404;
        }}
        .badge-danger {{ 
          background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
          color: #721c24;
        }}
        .badge-info {{ 
          background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); 
          color: #0c5460;
        }}
        .empty-state {{
          text-align: center;
          padding: 1.5rem;
          color: #999;
          font-style: italic;
          font-size: 0.9rem;
        }}
        .footer {{
          text-align: center;
          padding: 0.8rem;
          background: rgba(255,255,255,0.95);
          border-top: 1px solid #e2e8f0;
          flex-shrink: 0;
        }}
        .actions {{
          display: flex;
          gap: 0.6rem;
          flex-wrap: wrap;
          justify-content: center;
        }}
        .btn {{
          padding: 0.5rem 1rem;
          border-radius: 6px;
          text-decoration: none;
          font-weight: 600;
          transition: all 0.2s;
          display: inline-block;
          text-align: center;
          font-size: 0.85rem;
        }}
        .btn-primary {{
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-1px);
          box-shadow: 0 3px 10px rgba(102, 126, 234, 0.4);
        }}
        .btn-secondary {{
          background: #6c757d;
          color: white;
        }}
        .btn-secondary:hover {{
          background: #5a6268;
          transform: translateY(-1px);
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <header>
          <h1>{species_emoji} Detalles de {pet.name}</h1>
        </header>
        
        <div class="pet-header">
          <div class="pet-icon">{species_emoji}</div>
          <div class="pet-info">
            <h2>{pet.name}</h2>
            <p class="pet-id">ID: #{pet.id} | {pet.species}</p>
          </div>
        </div>
        
        <div class="main-content">
          <div class="info-grid">
            <div class="info-card">
              <h3>📋 Información Básica</h3>
              <div class="info-row">
                <span class="info-label">Especie:</span>
                <span class="info-value">{pet.species}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Raza:</span>
                <span class="info-value">{breed_display}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Fecha de Nac.:</span>
                <span class="info-value">{birth_display}</span>
              </div>
            </div>
            
            <div class="info-card">
              <h3>📝 Notas</h3>
              <p style="margin: 0; color: #666; font-size: 0.85rem;">{notes_display}</p>
            </div>
          </div>
          
          <div class="owner-section">
            <h3>👤 Dueño: {pet.owner.name}</h3>
            <div>
              <div>📞 {pet.owner.phone if pet.owner.phone else 'No especificado'}</div>
              <div>📧 {pet.owner.email if pet.owner.email else 'No especificado'}</div>
            </div>
          </div>
          
          <div class="section">
            <h3>📋 Récords Clínicos</h3>
    """
    
    if records:
        for record in sorted(records, key=lambda r: r.visit_date, reverse=True):
            symptoms_html = f'<div class="list-item-text"><strong>Síntomas:</strong> {record.symptoms}</div>' if record.symptoms else ''
            treatment_html = f'<div class="list-item-text"><strong>Tratamiento:</strong> {record.treatment}</div>' if record.treatment else ''
            medications_html = f'<div class="list-item-text"><strong>Medicamentos:</strong> {record.medications}</div>' if record.medications else ''
            
            html_content += f"""
            <div class="list-item">
              <div class="list-item-title">🗓️ {record.visit_date.strftime('%d/%m/%Y')}</div>
              <div class="list-item-text"><strong>Diagnóstico:</strong> {record.diagnosis}</div>
              {symptoms_html}
              {treatment_html}
              {medications_html}
            </div>
            """
    else:
        html_content += '<div class="empty-state">Sin récords clínicos registrados</div>'
    
    html_content += """
          </div>
          
          <div class="section">
            <h3>💉 Vacunas</h3>
    """
    
    if vaccinations:
        from datetime import datetime
        today = datetime.now().date()
        for vaccination in sorted(vaccinations, key=lambda v: v.due_date, reverse=True):
            # Calcular días hasta vencimiento
            days_until_due = (vaccination.due_date - today).days
            
            # Determinar estado y estilo
            if days_until_due < 0:
                status_badge = '<span class="badge badge-danger">⚠️ Vencida</span>'
                border_color = '#f8d7da'
                days_text = f'<span style="color: #dc3545; font-weight: 600;">Vencida hace {abs(days_until_due)} días</span>'
            elif days_until_due <= 30:
                status_badge = '<span class="badge badge-warning">⏰ Próxima a vencer</span>'
                border_color = '#fff3cd'
                days_text = f'<span style="color: #856404; font-weight: 600;">Vence en {days_until_due} días</span>'
            else:
                status_badge = '<span class="badge badge-success">✅ Vigente</span>'
                border_color = '#d4edda'
                days_text = f'<span style="color: #155724; font-weight: 600;">Vence en {days_until_due} días</span>'
            
            notes_html = f'<div class="list-item-text">📝 <strong>Notas:</strong> {vaccination.notes}</div>' if vaccination.notes else ''
            
            html_content += f"""
            <div class="list-item" style="border-left-color: {border_color}; border-left-width: 5px;">
              <div class="list-item-title" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.4rem;">
                <span style="font-size: 0.95rem;">💉 {vaccination.vaccine_name}</span>
                {status_badge}
              </div>
              <div class="list-item-text" style="margin-top: 0.5rem; display: grid; gap: 0.4rem;">
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                  <div>📅 <strong>Aplicada:</strong> {vaccination.applied_date.strftime('%d/%m/%Y')}</div>
                  <div>⏰ <strong>Vencimiento:</strong> {vaccination.due_date.strftime('%d/%m/%Y')}</div>
                </div>
                <div>{days_text}</div>
              </div>
              {notes_html}
            </div>
            """
    else:
        html_content += '<div class="empty-state">Sin vacunas registradas</div>'
    
    html_content += """
          </div>
          
          <div class="section">
            <h3>📅 Turnos</h3>
    """
    
    if appointments:
        from datetime import datetime
        today = datetime.now()
        
        for appointment in sorted(appointments, key=lambda a: a.appointment_date, reverse=True):
            # Determinar si es pasado o futuro
            is_past = appointment.appointment_date < today
            
            # Estilo según estado
            if appointment.status == 'attended':
                status_badge = '<span class="badge badge-success">✅ Atendido</span>'
                border_color = '#d4edda'
            elif appointment.status == 'canceled':
                status_badge = '<span class="badge badge-danger">❌ Cancelado</span>'
                border_color = '#f8d7da'
            elif appointment.status == 'scheduled':
                if is_past:
                    status_badge = '<span class="badge badge-warning">⏰ Pendiente (pasado)</span>'
                    border_color = '#fff3cd'
                else:
                    status_badge = '<span class="badge badge-info">📅 Programado</span>'
                    border_color = '#d1ecf1'
            else:
                status_badge = f'<span class="badge badge-info">{appointment.status}</span>'
                border_color = '#e0e0e0'
            
            # Calcular tiempo relativo
            time_diff = appointment.appointment_date - today
            if time_diff.days > 0:
                time_text = f'En {time_diff.days} días'
            elif time_diff.days == 0:
                hours = time_diff.seconds // 3600
                if hours > 0:
                    time_text = f'Hoy en {hours} horas'
                else:
                    time_text = 'Hoy'
            elif time_diff.days == -1:
                time_text = 'Ayer'
            else:
                time_text = f'Hace {abs(time_diff.days)} días'
            
            notes_html = f'<div class="list-item-text" style="margin-top: 0.4rem;">📝 <strong>Notas:</strong> {appointment.notes}</div>' if appointment.notes else ''
            
            html_content += f"""
            <div class="list-item" style="border-left-color: {border_color}; border-left-width: 5px;">
              <div class="list-item-title" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.4rem;">
                <span style="font-size: 0.95rem;">🗓️ {appointment.appointment_date.strftime('%d/%m/%Y %H:%M')}</span>
                {status_badge}
              </div>
              <div class="list-item-text" style="margin-top: 0.5rem; display: grid; gap: 0.4rem;">
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                  <div><strong>Motivo:</strong> {appointment.reason}</div>
                  <div style="color: #666; font-style: italic;">({time_text})</div>
                </div>
              </div>
              {notes_html}
            </div>
            """
    else:
        html_content += '<div class="empty-state">Sin turnos registrados</div>'
    
    html_content += f"""
          </div>
        </div>
        
        <div class="footer">
          <div class="actions">
            <a href="/pets/{pet.id}/clinical-history" class="btn btn-primary">📋 Ver Historia Clínica Completa</a>
            <a href="/pets/search/view" class="btn btn-secondary">⬅️ Volver a búsqueda</a>
            <a href="/vet/clinica" class="btn btn-secondary">🏥 Panel Clínico</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/{pet_id}/clinical-history", response_class=HTMLResponse)
def get_pet_clinical_history(pet_id: int, db: Session = Depends(get_db)):
    """Vista HTML enfocada en la historia clínica completa de una mascota."""
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    # Emoji de especie
    species_lower = pet.species.lower()
    if 'perro' in species_lower or 'dog' in species_lower:
        species_emoji = '🐕'
    elif 'gato' in species_lower or 'cat' in species_lower:
        species_emoji = '🐈'
    elif 'ave' in species_lower or 'pájaro' in species_lower or 'bird' in species_lower:
        species_emoji = '🦜'
    elif 'conejo' in species_lower or 'rabbit' in species_lower:
        species_emoji = '🐰'
    elif 'hámster' in species_lower or 'hamster' in species_lower:
        species_emoji = '🐹'
    else:
        species_emoji = '🐾'
    
    # Obtener récords clínicos ordenados por fecha
    records = sorted(pet.clinical_records, key=lambda r: r.visit_date, reverse=True) if pet.clinical_records else []
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>{species_emoji} {pet.name} - Historia Clínica - Veterinaria Inteligente</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          margin: 0;
          padding: 0;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          height: 100vh;
          overflow: hidden;
        }}
        .container {{
          height: 100vh;
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }}
        header {{
          flex-shrink: 0;
          text-align: center;
          padding: 0.8rem 1rem;
          background: rgba(255,255,255,0.98);
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        header h1 {{
          margin: 0;
          font-size: 1.8rem;
          color: #333;
          font-weight: 700;
        }}
        .pet-header {{
          flex-shrink: 0;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1rem 1.5rem;
          display: flex;
          align-items: center;
          gap: 1.5rem;
          box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}
        .pet-icon {{
          font-size: 3rem;
          flex-shrink: 0;
        }}
        .pet-info h2 {{
          margin: 0 0 0.3rem;
          font-size: 1.8rem;
        }}
        .pet-details {{
          opacity: 0.95;
          font-size: 0.85rem;
        }}
        .summary {{
          flex-shrink: 0;
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
          padding: 0.8rem 1rem;
          text-align: center;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.8rem;
        }}
        .summary-count {{
          font-size: 2rem;
          font-weight: 700;
          margin: 0;
        }}
        .summary-label {{
          font-size: 0.9rem;
          margin: 0;
        }}
        .main-content {{
          flex: 1;
          overflow-y: auto;
          padding: 1rem;
          background: rgba(255,255,255,0.95);
        }}
        .content-wrapper {{
          max-width: 1200px;
          margin: 0 auto;
        }}
        .timeline {{
          position: relative;
          padding-left: 1.5rem;
        }}
        .timeline::before {{
          content: '';
          position: absolute;
          left: 0;
          top: 0;
          bottom: 0;
          width: 3px;
          background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }}
        .timeline-item {{
          position: relative;
          margin-bottom: 1rem;
          padding-left: 1.5rem;
        }}
        .timeline-item::before {{
          content: '📋';
          position: absolute;
          left: -1.8rem;
          top: 0;
          font-size: 1.3rem;
          background: white;
          padding: 0.2rem;
          border-radius: 50%;
        }}
        .record-card {{
          background: #f8f9fa;
          border-left: 4px solid #667eea;
          border-radius: 8px;
          padding: 1rem;
          box-shadow: 0 2px 6px rgba(0,0,0,0.08);
          transition: transform 0.2s, box-shadow 0.2s;
        }}
        .record-card:hover {{
          transform: translateX(3px);
          box-shadow: 0 3px 10px rgba(0,0,0,0.12);
        }}
        .record-date {{
          font-size: 1.1rem;
          font-weight: 700;
          color: #667eea;
          margin-bottom: 0.8rem;
        }}
        .record-section {{
          margin-bottom: 0.8rem;
        }}
        .record-label {{
          font-weight: 600;
          color: #555;
          margin-bottom: 0.2rem;
          display: block;
          font-size: 0.85rem;
        }}
        .record-value {{
          color: #333;
          line-height: 1.5;
          padding: 0.4rem 0.6rem;
          background: white;
          border-radius: 4px;
          font-size: 0.85rem;
        }}
        .empty-state {{
          text-align: center;
          padding: 2rem;
          color: #999;
        }}
        .empty-icon {{
          font-size: 3rem;
          margin-bottom: 0.8rem;
        }}
        .footer {{
          flex-shrink: 0;
          background: rgba(255,255,255,0.98);
          padding: 0.8rem;
          box-shadow: 0 -2px 8px rgba(0,0,0,0.1);
          text-align: center;
        }}
        .actions {{
          display: flex;
          gap: 0.6rem;
          justify-content: center;
          flex-wrap: wrap;
        }}
        .btn {{
          padding: 0.5rem 1rem;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 600;
          transition: all 0.2s;
          display: inline-block;
          text-align: center;
          font-size: 0.85rem;
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
      </style>
    </head>
    <body>
      <div class="container">
        <header>
          <h1>{species_emoji} Historia Clínica Completa de {pet.name}</h1>
        </header>
        
        <div class="pet-header">
          <div class="pet-icon">{species_emoji}</div>
          <div class="pet-info">
            <h2>{pet.name}</h2>
            <p class="pet-details">
              ID: #{pet.id} | {pet.species} | Dueño: {pet.owner.name}
            </p>
          </div>
        </div>
        
        <div class="summary">
          <div class="summary-count">{len(records)}</div>
          <div class="summary-label">Consultas médicas registradas</div>
        </div>
        
        <div class="main-content">
          <div class="content-wrapper">
    """
    
    if records:
        html_content += """
            <div class="timeline">
        """
        for record in records:
            symptoms_html = f"""
            <div class="record-section">
              <span class="record-label">🔍 Síntomas:</span>
              <div class="record-value">{record.symptoms}</div>
            </div>
            """ if record.symptoms else ""
            
            treatment_html = f"""
            <div class="record-section">
              <span class="record-label">💊 Tratamiento:</span>
              <div class="record-value">{record.treatment}</div>
            </div>
            """ if record.treatment else ""
            
            medications_html = f"""
            <div class="record-section">
              <span class="record-label">💉 Medicamentos:</span>
              <div class="record-value">{record.medications}</div>
            </div>
            """ if record.medications else ""
            
            html_content += f"""
              <div class="timeline-item">
                <div class="record-card">
                  <div class="record-date">🗓️ {record.visit_date.strftime('%d de %B de %Y')}</div>
                  
                  {symptoms_html}
                  
                  <div class="record-section">
                    <span class="record-label">🩺 Diagnóstico:</span>
                    <div class="record-value">{record.diagnosis}</div>
                  </div>
                  
                  {treatment_html}
                  {medications_html}
                </div>
              </div>
            """
        
        html_content += """
            </div>
        """
    else:
        html_content += """
            <div class="empty-state">
              <div class="empty-icon">📋</div>
              <h3>Sin historia clínica</h3>
              <p>Esta mascota aún no tiene consultas médicas registradas.</p>
            </div>
        """
    
    html_content += f"""
          </div>
        </div>
        
        <div class="footer">
          <div class="actions">
            <a href="/pets/{pet.id}/view" class="btn btn-primary">👁️ Ver detalles</a>
            <a href="/pets/search/view" class="btn btn-secondary">🔍 Búsqueda</a>
            <a href="/vet/clinica" class="btn btn-secondary">🏥 Panel Clínico</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/{pet_id}/edit", response_class=HTMLResponse)
def edit_pet_form(pet_id: int, db: Session = Depends(get_db)):
    """Formulario HTML para editar una mascota."""
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    # Emoji según especie
    species_emoji = {
        'perro': '🐕',
        'gato': '🐈',
        'ave': '🦜',
        'conejo': '🐰',
        'hamster': '🐹',
    }.get(str(pet.species).lower() if pet.species else '', '🐾')  # type: ignore
    
    birth_date_str = pet.birth_date.strftime('%Y-%m-%d') if pet.birth_date else ''  # type: ignore
    owner_name = pet.owner.name if pet.owner else 'N/A'
    
    # Valores para selected en options
    pet_species_str = str(pet.species) if pet.species else ''  # type: ignore
    
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>✏️ Editar Mascota - Veterinaria Inteligente</title>
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
        }}
        .header {{
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
        input[type="date"],
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
        input:focus,
        select:focus,
        textarea:focus {{
          outline: none;
          border-color: #11998e;
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
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
          background: #d1ecf1;
          border-left: 4px solid #0c5460;
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 1.5rem;
        }}
        .info-box p {{
          margin: 0;
          color: #0c5460;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>{species_emoji} Editar Mascota</h1>
          <p>ID: #{pet.id} - {pet.name} · Dueño: {owner_name}</p>
        </div>
        
        <div class="content">
          <div class="info-box">
            <p><strong>📝 Instrucciones:</strong> Modifica los datos que necesites actualizar y presiona "Guardar Cambios".</p>
          </div>
          
          <form method="POST" action="/pets/{pet.id}/update">
            <div class="form-group">
              <label>Nombre <span class="required">*</span></label>
              <input type="text" name="name" value="{pet.name}" required />
            </div>
            
            <div class="form-group">
              <label>Especie <span class="required">*</span></label>
              <select name="species" required>
                <option value="perro" {'selected' if pet_species_str == 'perro' else ''}>🐕 Perro</option>
                <option value="gato" {'selected' if pet_species_str == 'gato' else ''}>🐈 Gato</option>
                <option value="ave" {'selected' if pet_species_str == 'ave' else ''}>🦜 Ave</option>
                <option value="conejo" {'selected' if pet_species_str == 'conejo' else ''}>🐰 Conejo</option>
                <option value="hamster" {'selected' if pet_species_str == 'hamster' else ''}>🐹 Hamster</option>
                <option value="otro" {'selected' if pet_species_str not in ['perro', 'gato', 'ave', 'conejo', 'hamster'] else ''}>🐾 Otro</option>
              </select>
            </div>
            
            <div class="form-group">
              <label>Raza</label>
              <input type="text" name="breed" value="{pet.breed or ''}" placeholder="Ej: Mestizo, Golden Retriever" />
            </div>
            
            <div class="form-group">
              <label>Fecha de Nacimiento</label>
              <input type="date" name="birth_date" value="{birth_date_str}" />
            </div>
            
            <div class="form-group">
              <label>Notas Adicionales</label>
              <textarea name="notes" placeholder="Ej: Alergias, comportamiento, observaciones...">{pet.notes or ''}</textarea>
            </div>
            
            <div class="actions">
              <button type="submit" class="btn btn-primary">💾 Guardar Cambios</button>
              <a href="/pets/view" class="btn btn-secondary" style="text-align: center; text-decoration: none; display: flex; align-items: center; justify-content: center;">❌ Cancelar</a>
            </div>
          </form>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.post("/{pet_id}/update", response_class=HTMLResponse)
def update_pet(
    pet_id: int,
    name: str = Form(...),
    species: str = Form(...),
    breed: str | None = Form(None),
    birth_date: str | None = Form(None),
    notes: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """Actualizar datos de una mascota."""
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    # Actualizar campos
    setattr(pet, 'name', name)  # type: ignore
    setattr(pet, 'species', species)  # type: ignore
    if breed:
        setattr(pet, 'breed', breed)  # type: ignore
    if birth_date:
        from datetime import datetime
        try:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
            setattr(pet, 'birth_date', birth_date_obj)  # type: ignore
        except:
            pass
    if notes:
        setattr(pet, 'notes', notes)  # type: ignore
    
    db.commit()
    db.refresh(pet)
    
    # Emoji según especie
    species_emoji = {
        'perro': '🐕',
        'gato': '🐈',
        'ave': '🦜',
        'conejo': '🐰',
        'hamster': '🐹',
    }.get(species.lower(), '🐾')
    
    owner_name = pet.owner.name if pet.owner else 'N/A'
    birth_date_display = pet.birth_date.strftime('%d/%m/%Y') if pet.birth_date else 'No especificada'  # type: ignore
    
    # Página de confirmación
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>✅ Mascota Actualizada - Veterinaria Inteligente</title>
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
          animation: bounce 0.6s ease-out;
        }}
        @keyframes bounce {{
          0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
          40% {{ transform: translateY(-15px); }}
          60% {{ transform: translateY(-7px); }}
        }}
        .header {{
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
        .success-box {{
          background: #d4edda;
          border-left: 4px solid #28a745;
          padding: 1.5rem;
          border-radius: 8px;
          margin-bottom: 2rem;
        }}
        .success-box p {{
          margin: 0;
          color: #155724;
        }}
        .updated-info {{
          background: #f8f9fa;
          padding: 1.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
        }}
        .updated-info h3 {{
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
        .actions {{
          display: flex;
          gap: 1rem;
        }}
        .btn {{
          flex: 1;
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
          background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
          color: white;
        }}
        .btn-primary:hover {{
          transform: translateY(-3px);
          box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
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
          <div class="icon">✅</div>
          <h1>Mascota Actualizada</h1>
          <p>Los cambios se guardaron correctamente</p>
        </div>
        
        <div class="content">
          <div class="success-box">
            <p><strong>✅ Operación exitosa:</strong> Los datos de la mascota se actualizaron correctamente en el sistema.</p>
          </div>
          
          <div class="updated-info">
            <h3>{species_emoji} Datos Actualizados</h3>
            <div class="info-row">
              <strong>ID:</strong>
              <span>#{pet.id}</span>
            </div>
            <div class="info-row">
              <strong>Nombre:</strong>
              <span>{pet.name}</span>
            </div>
            <div class="info-row">
              <strong>Especie:</strong>
              <span>{species_emoji} {pet.species}</span>
            </div>
            <div class="info-row">
              <strong>Raza:</strong>
              <span>{pet.breed or 'No especificada'}</span>
            </div>
            <div class="info-row">
              <strong>Fecha de Nacimiento:</strong>
              <span>{birth_date_display}</span>
            </div>
            <div class="info-row">
              <strong>Dueño:</strong>
              <span>{owner_name}</span>
            </div>
          </div>
          
          <div class="actions">
            <a href="/pets/{pet.id}/view" class="btn btn-primary">👁️ Ver Detalles</a>
            <a href="/pets/view" class="btn btn-secondary">📋 Volver al Listado</a>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/{pet_id}/delete", response_class=HTMLResponse)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    """Eliminar una mascota y todos sus registros relacionados."""
    pet = db.get(models.Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    # Contar registros relacionados
    records_count = len(pet.clinical_records) if pet.clinical_records else 0
    appointments_count = len(pet.appointments) if pet.appointments else 0
    vaccinations_count = len(pet.vaccinations) if pet.vaccinations else 0
    
    # Emoji según especie
    species_emoji = {
        'perro': '🐕',
        'gato': '🐈',
        'ave': '🦜',
        'conejo': '🐰',
        'hamster': '🐹',
    }.get(str(pet.species).lower() if pet.species else '', '🐾')  # type: ignore
    
    # Guardar info antes de eliminar
    pet_name = pet.name
    pet_species = pet.species
    pet_id_saved = pet.id
    owner_name = pet.owner.name if pet.owner else 'N/A'
    
    # Eliminar (cascade eliminará turnos, registros clínicos, etc.)
    db.delete(pet)
    db.commit()
    
    # Página de confirmación
    html_content = f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>🗑️ Mascota Eliminada - Veterinaria Inteligente</title>
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
          <h1>Mascota Eliminada</h1>
          <p>El registro se eliminó permanentemente del sistema</p>
        </div>
        
        <div class="content">
          <div class="warning-box">
            <h3>⚠️ Registros Eliminados</h3>
            <ul>
              <li>Mascota: {species_emoji} {pet_name}</li>
              <li>Registros clínicos: {records_count}</li>
              <li>Turnos: {appointments_count}</li>
              <li>Vacunaciones: {vaccinations_count}</li>
            </ul>
          </div>
          
          <div class="deleted-info">
            <h3>📋 Información del Registro Eliminado</h3>
            <div class="info-row">
              <strong>ID:</strong>
              <span>#{pet_id_saved}</span>
            </div>
            <div class="info-row">
              <strong>Nombre:</strong>
              <span>{pet_name}</span>
            </div>
            <div class="info-row">
              <strong>Especie:</strong>
              <span>{species_emoji} {pet_species}</span>
            </div>
            <div class="info-row">
              <strong>Dueño:</strong>
              <span>{owner_name}</span>
            </div>
            <div class="info-row">
              <strong>Registros eliminados:</strong>
              <span>{records_count + appointments_count + vaccinations_count} en total</span>
            </div>
          </div>
          
          <a href="/pets/view" class="btn">🐾 Volver al listado de mascotas</a>
        </div>
      </div>
    </body>
    </html>
    """
    
    return html_content
