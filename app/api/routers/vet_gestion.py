from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from datetime import date

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def vet_gestion_home():
    """Panel de Gestión Veterinaria - Control completo de la veterinaria"""
    today = date.today().isoformat()
    
    return HTMLResponse(content=f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>📊 Panel de Gestión Veterinaria</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    
    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      height: 100vh;
      overflow: hidden;
    }}
    
    .container {{
      height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    
    /* Header */
    header {{
      text-align: center;
      padding: 0.5rem 1rem;
      background: rgba(255,255,255,0.98);
      border-bottom: 2px solid #e2e8f0;
      flex-shrink: 0;
    }}
    
    header h1 {{
      margin: 0;
      font-size: 1.4rem;
      color: #333;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }}
    
    header h1 .emoji {{
      font-size: 1.6rem;
    }}
    
    header p {{
      margin: 0.2rem 0 0;
      color: #666;
      font-size: 0.75rem;
    }}
    
    .nav-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      justify-content: center;
      padding: 0.5rem 1rem;
      background: rgba(255,255,255,0.95);
      border-bottom: 1px solid #e2e8f0;
      flex-shrink: 0;
    }}
    
    .nav-links a {{
      padding: 0.35rem 0.7rem;
      background: #f0f4ff;
      color: #4a5568;
      text-decoration: none;
      border-radius: 6px;
      font-size: 0.7rem;
      transition: all 0.2s;
      border: 1px solid #e2e8f0;
      white-space: nowrap;
    }}
    
    .nav-links a:hover {{
      background: #667eea;
      color: #fff;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(102,126,234,0.4);
    }}
    
    /* Main Content */
    .main-content {{
      flex: 1;
      padding: 1rem;
      overflow-y: auto;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 1rem;
      background: rgba(255,255,255,0.95);
    }}
    
    /* Cards */
    .card {{
      background: white;
      border-radius: 8px;
      padding: 1rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      border: 1px solid #e2e8f0;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    
    .card-header {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.8rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid #f0f0f0;
    }}
    
    .card-icon {{
      font-size: 1.5rem;
    }}
    
    .card-title {{
      font-size: 0.9rem;
      font-weight: 700;
      color: #333;
      line-height: 1.2;
    }}
    
    .card-body {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
      overflow-y: auto;
    }}
    
    .card-description {{
      color: #666;
      font-size: 0.75rem;
      margin-bottom: 0.3rem;
      display: none;
    }}
    
    /* Stats Grid (Dashboard) */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.5rem;
      flex: 1;
    }}
    
    .stat-card {{
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 0.6rem;
      border-radius: 6px;
      text-align: center;
      color: white;
      display: flex;
      flex-direction: column;
      justify-content: center;
      transition: transform 0.2s;
      cursor: pointer;
      text-decoration: none;
      min-height: 60px;
    }}
    
    .stat-card:hover {{
      transform: scale(1.05);
    }}
    
    .stat-number {{
      font-size: 2rem;
      margin-bottom: 0.2rem;
    }}
    
    .stat-label {{
      font-size: 0.7rem;
      font-weight: 600;
      opacity: 0.95;
      line-height: 1.1;
    }}
    
    /* Form Elements */
    .form-group {{
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }}
    
    .form-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.8rem;
    }}
    
    label {{
      font-size: 0.75rem;
      font-weight: 600;
      color: #555;
    }}
    
    input, select {{
      padding: 0.4rem;
      border: 2px solid #e0e0e0;
      border-radius: 4px;
      font-size: 0.75rem;
      transition: border-color 0.2s;
    }}
    
    input:focus, select:focus {{
      outline: none;
      border-color: #667eea;
    }}
    
    /* Buttons */
    .btn {{
      padding: 0.5rem 0.8rem;
      border: none;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      text-decoration: none;
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
    
    .btn-success {{
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
      color: white;
    }}
    
    .btn-success:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
    }}
    
    .btn-danger {{
      background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
      color: white;
    }}
    
    .btn-danger:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(235, 51, 73, 0.4);
    }}
    
    .btn-group {{
      display: flex;
      gap: 0.5rem;
      margin-top: auto;
    }}
    
    .btn-group .btn {{
      flex: 1;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
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
    <!-- Header -->
    <header>
      <h1><span class="emoji">📊</span> Panel de Gestión Veterinaria</h1>
      <p>Control completo de la veterinaria - Gestión integral</p>
    </header>
    
    <!-- Navigation Links -->
    <div class="nav-links">
      <a href="/">🏠 INICIO</a>
      <a href="/ui">📋 PANEL RECEPCIÓN</a>
      <a href="/vet/clinica/">🩺 ATENCIÓN CLÍNICA</a>
      <a href="/vet/">👨‍⚕️ PANEL PRINCIPAL DEL VETERINARIO</a>
      <a href="/pets/view">🔍 BÚSQUEDA MASCOTAS</a>
      <a href="/admin/api_docs_friendly" target="_blank">📚 API DOCS</a>
    </div>
    
    <!-- Main Content - Grid 2x2 -->
    <div class="main-content">
      
      <!-- Card 1: Dashboard del Día -->
      <div class="card">
        <div class="card-header">
          <div class="card-icon">📅</div>
          <div class="card-title">AGENDA DEL DÍA<br>(Resumen de turnos de hoy)</div>
        </div>
        <div class="card-body">
          <p class="card-description">Resumen de turnos de hoy</p>
          <div class="stats-grid">
            <a href="/schedule/daily?date={today}" target="_blank" class="stat-card">
              <div class="stat-number">📅</div>
              <div class="stat-label">VER AGENDA<br>DE HOY</div>
            </a>
            <a href="/appointments/view?status=attended&date={today}" target="_blank" class="stat-card">
              <div class="stat-number">✅</div>
              <div class="stat-label">TURNOS<br>ATENDIDOS</div>
            </a>
            <a href="/appointments/view?status=scheduled&date={today}" target="_blank" class="stat-card">
              <div class="stat-number">⏳</div>
              <div class="stat-label">TURNOS<br>PENDIENTES</div>
            </a>
            <a href="/appointments/view?status=canceled&date={today}" target="_blank" class="stat-card">
              <div class="stat-number">❌</div>
              <div class="stat-label">TURNOS<br>CANCELADOS</div>
            </a>
          </div>
        </div>
      </div>
      
      <!-- Card 2: Gestión de Vacunas -->
      <div class="card">
        <div class="card-header">
          <div class="card-icon">💉</div>
          <div class="card-title">CONTROL DE VACUNAS<br>(Alertas de vacunación)</div>
        </div>
        <div class="card-body">
          <p class="card-description">Alertas de vacunación</p>
          
          <div class="form-group">
            <label>Días de anticipación</label>
            <input type="number" id="vacc-days" value="30" min="1" max="90" placeholder="30">
          </div>
          
          <div class="btn-group">
            <a href="/vaccinations/view?days=30" target="_blank" class="btn btn-success" id="vacc-upcoming-link">
              💉 Próximas a Vencer
            </a>
            <a href="/vaccinations/view?type=overdue" target="_blank" class="btn btn-danger">
              ⚠️ Vencidas
            </a>
          </div>
        </div>
      </div>
      
      <!-- Card 3: Consultar Agenda -->
      <div class="card">
        <div class="card-header">
          <div class="card-icon">📆</div>
          <div class="card-title">CONSULTAR AGENDA<br>(Ver turnos de cualquier día)</div>
        </div>
        <div class="card-body">
          <p class="card-description">Ver turnos de cualquier día</p>
          
          <div class="form-group">
            <label>Seleccionar fecha</label>
            <input type="date" id="agenda-date" value="{today}">
          </div>
          
          <div class="btn-group">
            <button onclick="viewAgenda()" class="btn btn-primary">
              📅 Ver Agenda del Día
            </button>
          </div>
        </div>
      </div>
      
      <!-- Card 4: Búsqueda Avanzada -->
      <div class="card">
        <div class="card-header">
          <div class="card-icon">🔍</div>
          <div class="card-title">BÚSQUEDA DE TURNOS<br>(Filtrar por rango y estado)</div>
        </div>
        <div class="card-body">
          <p class="card-description">Filtrar turnos por rango y estado</p>
          
          <div class="form-row">
            <div class="form-group">
              <label>Desde</label>
              <input type="date" id="search-from" value="{today}">
            </div>
            <div class="form-group">
              <label>Hasta</label>
              <input type="date" id="search-to" value="{today}">
            </div>
          </div>
          
          <div class="form-group">
            <label>Estado del turno</label>
            <select id="search-status">
              <option value="">Todos los estados</option>
              <option value="scheduled">Agendados</option>
              <option value="attended">Atendidos</option>
              <option value="canceled">Cancelados</option>
            </select>
          </div>
          
          <div class="btn-group">
            <button onclick="searchAppointments()" class="btn btn-primary">
              🔍 Buscar Turnos
            </button>
          </div>
        </div>
      </div>
      
    </div>
  </div>
  
  <script>
    // Actualizar link de vacunas cuando cambia el input
    document.getElementById('vacc-days').addEventListener('input', function() {{
      const days = this.value || 30;
      document.getElementById('vacc-upcoming-link').href = '/vaccinations/view?days=' + days;
    }});
    
    // Ver agenda del día seleccionado
    function viewAgenda() {{
      const date = document.getElementById('agenda-date').value;
      if (!date) {{
        alert('Por favor selecciona una fecha');
        return;
      }}
      window.open('/schedule/daily?date=' + date, '_blank');
    }}
    
    // Búsqueda avanzada de turnos
    function searchAppointments() {{
      const from = document.getElementById('search-from').value;
      const to = document.getElementById('search-to').value;
      const status = document.getElementById('search-status').value;
      
      if (!from || !to) {{
        alert('Por favor selecciona las fechas desde y hasta');
        return;
      }}
      
      let url = '/appointments/search?from=' + from + '&to=' + to;
      if (status) {{
        url += '&status=' + status;
      }}
      
      window.open(url, '_blank');
    }}
  </script>
</body>
</html>
""")
