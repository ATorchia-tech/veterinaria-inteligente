from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


HTML_VET_LANDING = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>🩺 Panel Veterinario - Veterinaria Inteligente</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    
    /* Encabezado compacto */
    .top-header {
      background: rgba(255, 255, 255, 0.98);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      padding: 0.5rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #11998e;
      flex-shrink: 0;
    }
    
    .top-header .team-info {
      font-size: 0.8rem;
      color: #4a5568;
      font-weight: 600;
    }
    
    .top-header .btn-home {
      padding: 0.4rem 1rem;
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
      color: white;
      text-decoration: none;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.85rem;
      transition: all 0.3s;
      box-shadow: 0 2px 6px rgba(17, 153, 142, 0.3);
    }
    
    .top-header .btn-home:hover {
      transform: translateY(-1px);
      box-shadow: 0 3px 10px rgba(17, 153, 142, 0.4);
    }
    
    /* Contenedor principal con altura fija */
    .content-wrapper {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      overflow: hidden;
    }
    
    .container {
      max-width: 1000px;
      width: 100%;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 15px 40px rgba(0,0,0,0.25);
      padding: 1.5rem;
      text-align: center;
      display: flex;
      flex-direction: column;
      max-height: 100%;
    }
    
    header h1 {
      font-size: 2rem;
      color: #333;
      font-weight: 700;
      margin-bottom: 0.5rem;
    }
    header h1 .emoji {
      font-size: 2.2rem;
      vertical-align: middle;
    }
    header p {
      color: #666;
      font-size: 0.95rem;
      margin-bottom: 1.5rem;
    }
    
    /* Grid de paneles - 2 columnas */
    .panels-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      margin-bottom: 1.25rem;
      flex: 1;
    }
    
    .panel-card {
      background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
      border: 3px solid #81e6d9;
      border-radius: 12px;
      padding: 2rem 1.5rem;
      text-decoration: none;
      color: inherit;
      transition: all 0.3s;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
    .panel-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 25px rgba(17,153,142,0.4);
      border-color: #11998e;
    }
    .panel-card .icon {
      font-size: 3.5rem;
      display: block;
      margin-bottom: 0.75rem;
    }
    .panel-card h2 {
      font-size: 1.4rem;
      color: #11998e;
      margin: 0 0 0.5rem;
      font-weight: 700;
    }
    .panel-card p {
      font-size: 0.85rem;
      color: #2c7a7b;
      margin: 0;
      line-height: 1.4;
    }
    
    /* Links de navegación compactos */
    .nav-links {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
      padding-top: 1rem;
      border-top: 2px solid #f0f0f0;
      flex-shrink: 0;
    }
    .nav-links a {
      padding: 0.4rem 0.9rem;
      background: #e6f7f5;
      color: #2c7a7b;
      text-decoration: none;
      border-radius: 6px;
      font-size: 0.75rem;
      transition: all 0.2s;
      border: 1px solid #b2f5ea;
    }
    .nav-links a:hover {
      background: #11998e;
      color: #fff;
      transform: translateY(-1px);
    }
  </style>
</head>
<body>
  <!-- Encabezado fijo -->
  <div class="top-header">
    <div class="team-info">IFTS-12, A.Mercado, S.Paniagua, F.Hernández, A.Torchia</div>
    <a href="http://127.0.0.1:8000/" class="btn-home">🏠 Ir a Inicio</a>
  </div>
  
  <div class="content-wrapper">
  <div class="container">
    <header>
      <h1><span class="emoji">🩺</span> Panel Veterinario</h1>
      <p>Seleccioná el módulo según tu actividad</p>
    </header>

    <div class="panels-grid">
      <a href="/vet/clinica" class="panel-card">
        <span class="icon">🩺</span>
        <h2>Atención Clínica</h2>
        <p>Consultas, diagnósticos, tratamientos, récords clínicos y fichas completas de mascotas.</p>
      </a>

      <a href="/vet/gestion" class="panel-card">
        <span class="icon">📊</span>
        <h2>Gestión Veterinaria</h2>
        <p>Dashboard diario, agenda de turnos, vacunas próximas a vencer y búsqueda avanzada.</p>
      </a>
    </div>

    <div class="nav-links">
      <a href="/ui">👥 Panel de Recepción</a>
      <a href="/admin/db_details" target="_blank">📊 Detalle de datos</a>
      <a href="/admin/db_counts_form" target="_blank">🔢 Totales</a>
      <a href="/admin/api_docs_friendly" target="_blank">📖 API Docs</a>
    </div>
  </div>
  </div>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def vet_ui_home():
    return HTMLResponse(content=HTML_VET_LANDING)
