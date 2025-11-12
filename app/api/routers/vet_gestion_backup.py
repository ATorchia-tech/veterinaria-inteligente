from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from datetime import date

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def vet_gestion_home():
    """Panel de Gestión Veterinaria - Control completo de la veterinaria"""
    today = date.today().isoformat()
    
    html_content = f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>📊 Gestión Veterinaria - Veterinaria Inteligente</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 0;
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
      height: 100vh;
      overflow: hidden;
    }
    .container {
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    header {
      flex-shrink: 0;
      text-align: center;
      padding: 0.8rem 1rem;
      background: rgba(255,255,255,0.98);
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    header h1 {
      margin: 0;
      font-size: 1.8rem;
      color: #333;
      font-weight: 700;
    }
    header h1 .emoji {
      font-size: 2rem;
      vertical-align: middle;
    }
    header p {
      margin: 0.3rem 0 0;
      color: #666;
      font-size: 0.85rem;
    }
    .nav-links {
      flex-shrink: 0;
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
      padding: 0.6rem;
      background: rgba(255,255,255,0.95);
      box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    .nav-links a {
      padding: 0.4rem 0.8rem;
      background: #e6f7f5;
      color: #2c7a7b;
      text-decoration: none;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      transition: all 0.2s;
      border: 1px solid #b2f5ea;
      white-space: nowrap;
    }
    .nav-links a:hover {
      background: #11998e;
      color: #fff;
      transform: translateY(-1px);
      box-shadow: 0 3px 8px rgba(17,153,142,0.3);
    }
    .main-content {
      flex: 1;
      overflow-y: auto;
      padding: 0.8rem;
      background: rgba(255,255,255,0.95);
    }
    .content-wrapper {
      max-width: 1400px;
      margin: 0 auto;
    }
    .sections {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }
    .section {
      background: #fff;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 2px 6px rgba(0,0,0,0.08);
      border: 2px solid #e2e8f0;
      transition: all 0.2s;
      min-height: 280px;
    }
    .section:hover {
      box-shadow: 0 4px 12px rgba(0,0,0,0.12);
      border-color: #11998e;
    }
    .section-header {
      font-weight: 700;
      font-size: 1.1rem;
      color: #fff;
      padding: 0.9rem 1.2rem;
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .section-header .icon {
      font-size: 1.4rem;
    }
    .section-content {
      padding: 1rem;
    }
    .section-content p {
      margin: 0 0 0.8rem;
      color: #666;
      font-size: 0.85rem;
      line-height: 1.4;
    }
    label {
      display: block;
      margin: 0.6rem 0 0.3rem;
      font-size: 0.85rem;
      font-weight: 600;
      color: #4a5568;
    }
    input, select, textarea {
      width: 100%;
      padding: 0.5rem 0.7rem;
      border: 2px solid #e2e8f0;
      border-radius: 6px;
      font-size: 0.85rem;
      transition: all 0.2s;
      font-family: inherit;
    }
    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: #11998e;
      box-shadow: 0 0 0 2px rgba(17,153,142,0.1);
    }
    textarea {
      resize: vertical;
      min-height: 60px;
    }
    button {
      margin-top: 0.7rem;
      padding: 0.6rem 1.1rem;
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
      color: #fff;
      border: 0;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      font-size: 0.85rem;
      transition: all 0.2s;
      box-shadow: 0 2px 6px rgba(17,153,142,0.3);
      width: 100%;
    }
    button:hover {
      transform: translateY(-1px);
      box-shadow: 0 3px 10px rgba(17,153,142,0.4);
    }
    button:active {
      transform: translateY(0);
    }
    small {
      display: block;
      margin-top: 0.4rem;
      color: #718096;
      font-size: 0.75rem;
      line-height: 1.4;
    }
    small a {
      color: #11998e;
      text-decoration: none;
    }
    small a:hover {
      text-decoration: underline;
    }
    .info-box {
      background: #e6fffa;
      border: 2px solid #81e6d9;
      padding: 0.6rem 0.8rem;
      border-radius: 8px;
      margin-bottom: 0.8rem;
      color: #234e52;
      font-size: 0.75rem;
    }
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.7rem;
    }
    .stats-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 0.7rem;
      margin: 0.8rem 0;
    }
    .stat-card {
      background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
      border: 2px solid #81e6d9;
      border-radius: 8px;
      padding: 0.8rem;
      text-align: center;
      transition: all 0.2s;
    }
    .stat-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(17,153,142,0.25);
    }
    .stat-card .number {
      font-size: 2.2rem;
      font-weight: 700;
      color: #11998e;
      margin: 0 0 0.3rem;
    }
    .stat-card .label {
      font-size: 0.75rem;
      color: #2c7a7b;
      margin-top: 0.3rem;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      font-weight: 600;
    }
      font-size: 1.8rem;
      font-weight: 700;
      color: #11998e;
      margin: 0;
    }
    .stat-card .label {
      font-size: 0.65rem;
      color: #2c7a7b;
      margin-top: 0.2rem;
      text-transform: uppercase;
      letter-spacing: 0.3px;
      font-weight: 600;
    }
    @media (max-width: 768px) {
      .sections {
        grid-template-columns: 1fr;
      }
      .grid-2 {
        grid-template-columns: 1fr;
      }
      .stats-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1><span class="emoji">📊</span> Gestión Veterinaria</h1>
      <p>Panel del Veterinario - Módulo de Gestión y Estadísticas</p>
    </header>

    <div class="nav-links">
      <a href="/">🏠 IR A INICIO</a>
      <a href="/vet">🩺 PANEL PRINCIPAL DEL VETERINARIO</a>
      <a href="/vet/clinica">🏥 ATENCION CLINICA</a>
      <a href="/ui">👥 PANEL RECEPCION</a>
      <a href="/admin/db_details" target="_blank">📊 DETALLE DE DATOS</a>
      <a href="/admin/db_counts_form" target="_blank">🔢 TOTALES</a>
      <a href="/admin/api_docs_friendly" target="_blank">📖 API DOCS</a>
    </div>

    <div class="main-content">
      <div class="content-wrapper">
        <div class="info-box">
          📈 Módulo dedicado a la gestión operativa: dashboard, agenda, vacunaciones y reportes.
        </div>

        <div class="sections">
          <!-- Sección 1: Dashboard del Día -->
          <div class="section">
            <div class="section-header">
              <span class="icon">📊</span> DASHBOARD DEL DIA
            </div>
            <div class="section-content">
              <p>Vista rápida de las estadísticas de hoy para planificar tu jornada.</p>
              
              <div class="stats-grid">
                <div class="stat-card">
                  <div class="number">📅</div>
                  <div class="label">TURNOS HOY</div>
                  <small style="display:block; margin-top:0.4rem;">
                    <a href="/schedule/daily?date={{TODAY}}" target="_blank">Ver Agenda</a>
                  </small>
                </div>
                <div class="stat-card">
                  <div class="number">✅</div>
                  <div class="label">ATENDIDOS</div>
                  <small style="display:block; margin-top:0.4rem;">
                    <a href="/appointments/view?status=attended&date={{TODAY}}" target="_blank">Ver lista</a>
                  </small>
                </div>
                <div class="stat-card">
                  <div class="number">⏳</div>
                  <div class="label">PENDIENTES</div>
                  <small style="display:block; margin-top:0.4rem;">
                    <a href="/appointments/view?status=scheduled&date={{TODAY}}" target="_blank">Ver</a>
                  </small>
                </div>
                <div class="stat-card">
                  <div class="number">❌</div>
                  <div class="label">CANCELADOS</div>
                  <small style="display:block; margin-top:0.4rem;">
                    <a href="/appointments/view?status=canceled&date={{TODAY}}" target="_blank">Ver</a>
                  </small>
                </div>
              </div>

              </div>
            </div>
          </div>

          <!-- Sección 2: Vacunas Próximas a Vencer -->
          <div class="section">
            <div class="section-header">
              <span class="icon">⚠️</span> VACUNAS PROXIMAS A VENCER
            </div>
            <div class="section-content">
              <p>Alertas de vacunaciones próximas para contactar a los dueños y programar turnos.</p>
              
              <label>Días de anticipación</label>
              <input type="number" id="vacc-days" min="1" max="90" value="30" placeholder="30" />
              <button onclick="viewUpcomingVaccinations()">💉 Ver vacunas próximas</button>
              <small>Vacunas que vencen en los próximos días seleccionados. Por defecto: 30 días.</small>

              <button onclick="viewOverdueVaccinations()" style="background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%); margin-top: 0.6rem;">
                🚨 Ver vacunas vencidas
              </button>
              <small>Vacunas que ya pasaron la fecha de vencimiento y requieren atención urgente.</small>
            </div>
          </div>

          <!-- Sección 3: Visualización de la Agenda Diaria -->
          <div class="section">
            <div class="section-header">
              <span class="icon">📅</span> VISUALIZACION DE LA AGENDA DIARIA
            </div>
            <div class="section-content">
              <p>Consulta todas las citas programadas para planificar tu jornada de manera eficiente.</p>

              <label>Fecha</label>
              <input type="date" id="agenda-date" />
              <button onclick="viewDailySchedule()">📅 Ver agenda del día</button>
              <small>Lista de turnos del día seleccionado en <a href="/schedule/daily" target="_blank">/schedule/daily</a>.</small>
            </div>
          </div>

          <!-- Sección 4: Búsqueda Avanzada de Turnos -->
          <div class="section">
            <div class="section-header">
              <span class="icon">🔍</span> BUSQUEDA AVANZADA DE TURNOS
            </div>
            <div class="section-content">
              <p>Filtra turnos por estado (agendados, atendidos, cancelados) y rango de fechas.</p>

              <div class="grid-2">
                <div>
                  <label>Desde fecha</label>
                  <input type="date" id="appt-from" />
                </div>
                <div>
                  <label>Hasta fecha</label>
                  <input type="date" id="appt-to" />
                </div>
              </div>

              <label>Estado del turno</label>
              <select id="appt-status">
                <option value="">Todos</option>
                <option value="scheduled">Agendados</option>
                <option value="attended">Atendidos</option>
                <option value="canceled">Cancelados</option>
              </select>

              <button onclick="searchAppointments()">🔍 Buscar turnos</button>
              <small>Resultados en vista organizada por fecha con información completa.</small>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
  
  
  <script>
    // Funciones de Vacunas
    function viewUpcomingVaccinations() {
      const days = document.getElementById('vacc-days').value || 30;
      window.open('/vaccinations/upcoming?days=' + days, '_blank');
    }
    
    function viewExpiredVaccinations() {
      window.open('/vaccinations/expired', '_blank');
    }
    
    // Función de Agenda Diaria
    function viewDailySchedule() {
      const date = document.getElementById('agenda-date').value;
      if (!date) {
        alert('Por favor selecciona una fecha');
        return;
      }
      window.open('/schedule/daily?date=' + encodeURIComponent(date), '_blank');
    }
    
    // Función de Búsqueda Avanzada
    function searchAppointments() {
      const from = document.getElementById('appt-from').value;
      const to = document.getElementById('appt-to').value;
      const status = document.getElementById('appt-status').value;
      
      if (!from || !to) {
        alert('Por favor selecciona las fechas desde y hasta');
        return;
      }
      
      let url = '/appointments/search?';
      if (from) url += 'from=' + encodeURIComponent(from) + '&';
      if (to) url += 'to=' + encodeURIComponent(to) + '&';
      if (status) url += 'status=' + encodeURIComponent(status) + '&';
      
      window.open(url, '_blank');
    }
  </script>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def vet_gestion_home():
    # Obtener fecha actual en formato YYYY-MM-DD
    today = date.today().isoformat()
    
    # Reemplazar las URLs dinámicamente en el HTML
    html_content = HTML_VET_GESTION.replace('{{TODAY}}', today)
    
    return HTMLResponse(content=html_content)
