from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


HTML_HOME = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>🐾 Veterinaria Inteligente - IFTS-12</title>
  <style>
    * { 
      box-sizing: border-box; 
      margin: 0;
      padding: 0;
    }
    
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }
    
    /* Fondo con gradiente animado */
    .background {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: -1;
      background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%),
                  url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"><text x="100" y="150" font-size="120" opacity="0.05">🐕</text><text x="800" y="200" font-size="100" opacity="0.05">🐈</text><text x="300" y="500" font-size="110" opacity="0.05">🐇</text><text x="900" y="600" font-size="95" opacity="0.05">🐦</text><text x="150" y="700" font-size="105" opacity="0.05">🐾</text><text x="600" y="400" font-size="90" opacity="0.05">🐕‍🦺</text><text x="1000" y="150" font-size="100" opacity="0.05">🐈‍⬛</text></svg>');
      background-size: cover;
      background-position: center;
    }
    
    .container {
      width: 100%;
      max-width: 1600px;
      height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 0;
      padding: 1.5rem 2rem;
    }
    
    /* Header compacto */
    header {
      text-align: center;
      padding: 0.5rem 0;
      background: rgba(255, 255, 255, 0.98);
      border-radius: 16px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      backdrop-filter: blur(10px);
    }
    
    .main-icon {
      font-size: 2.5rem;
      display: inline-block;
      margin-right: 0.5rem;
      vertical-align: middle;
    }
    
    header h1 {
      font-size: 1.8rem;
      color: #2d3748;
      font-weight: 800;
      margin: 0;
      display: inline;
      line-height: 1;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    header h1 .highlight {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    .subtitle {
      font-size: 0.85rem;
      color: #4a5568;
      font-weight: 600;
      margin: 0.3rem 0 0;
      line-height: 1.2;
    }
    
    /* Grid de botones principales - Layout horizontal compacto */
    .panels-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.5rem;
      padding: 1.5rem 0;
      align-content: center;
    }
    
    .panel-card {
      background: rgba(255, 255, 255, 0.98);
      border: 3px solid #e2e8f0;
      border-radius: 20px;
      padding: 1.5rem 1rem;
      text-decoration: none;
      color: inherit;
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      backdrop-filter: blur(10px);
    }
    
    .panel-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      opacity: 0;
      transition: opacity 0.3s;
      z-index: 0;
    }
    
    .panel-card:hover::before {
      opacity: 1;
    }
    
    .panel-card:hover {
      transform: translateY(-8px) scale(1.03);
      box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
      border-color: #667eea;
    }
    
    .panel-card > * {
      position: relative;
      z-index: 1;
      transition: all 0.3s;
    }
    
    .panel-card:hover > * {
      color: #fff !important;
    }
    
    .panel-card .icon {
      font-size: 3.5rem;
      display: block;
      margin-bottom: 0.8rem;
      filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.1));
    }
    
    .panel-card h2 {
      font-size: 1.3rem;
      color: #2d3748;
      margin: 0 0 0.5rem;
      font-weight: 700;
      line-height: 1.2;
    }
    
    .panel-card p {
      font-size: 0.85rem;
      color: #4a5568;
      margin: 0;
      line-height: 1.4;
    }
    
    /* Panel especial para IA */
    .panel-card.ai-panel {
      background: rgba(254, 243, 199, 0.98);
      border-color: #fbbf24;
    }
    
    .panel-card.ai-panel::before {
      background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    /* Footer compacto con links en 2 filas */
    .footer-links {
      background: rgba(255, 255, 255, 0.98);
      border-radius: 16px;
      padding: 1rem;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      backdrop-filter: blur(10px);
    }
    
    .footer-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
    }
    
    .footer-row:first-child {
      margin-bottom: 0.5rem;
    }
    
    .footer-links a {
      padding: 0.5rem 1rem;
      background: #f7fafc;
      color: #4a5568;
      text-decoration: none;
      border-radius: 8px;
      font-size: 0.8rem;
      transition: all 0.3s;
      border: 2px solid #e2e8f0;
      font-weight: 600;
      white-space: nowrap;
    }
    
    .footer-links a:hover {
      background: #667eea;
      color: #fff;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
      border-color: #667eea;
    }
    
    .footer-links a.btn-presentation {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-color: #667eea;
      flex: 1 1 100%;
      max-width: 600px;
    }
    
    .footer-links a.btn-presentation:hover {
      transform: translateY(-2px) scale(1.02);
      box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Responsive */
    @media (max-width: 1200px) {
      .panels-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
      }
      
      .panel-card {
        padding: 1.2rem 1rem;
      }
      
      .panel-card .icon {
        font-size: 3rem;
      }
      
      .panel-card h2 {
        font-size: 1.2rem;
      }
    }
  </style>
</head>
<body>
  <div class="background"></div>
  
  <div class="container">
    <header>
      <div>
        <span class="main-icon">🐾</span>
        <h1>Proyecto <span class="highlight">IFTS-12</span> Veterinaria-Inteligente</h1>
      </div>
      <p class="subtitle">Integrantes: A. Mercado, S. Paniagua, F. Hernández, A. Torchia</p>
    </header>

    <div class="panels-grid">
      <!-- Panel Recepcionista -->
      <a href="/ui" class="panel-card">
        <span class="icon">👥</span>
        <h2>Panel Recepcionista</h2>
        <p>Gestión de dueños, mascotas y turnos</p>
      </a>

      <!-- Panel Veterinario -->
      <a href="/vet" class="panel-card">
        <span class="icon">🩺</span>
        <h2>Panel Veterinario</h2>
        <p>Atención clínica y récords médicos</p>
      </a>

      <!-- Panel IA - Predicción de Afluencia -->
      <a href="/ai-dashboard" class="panel-card ai-panel">
        <span class="icon">🤖</span>
        <h2>Predicción de Turnos</h2>
        <p>Análisis inteligente de cumplimiento</p>
      </a>
    </div>

    <div class="footer-links">
      <div class="footer-row">
        <a href="/admin/api_docs_friendly">📖 Documentación API</a>
        <a href="/admin/db_details" target="_blank">📊 Base de Datos</a>
        <a href="/admin/db_counts_form" target="_blank">🔢 Estadísticas</a>
      </div>
      <div class="footer-row">
        <a href="/admin/presentation" class="btn-presentation">📚 Documento de Presentación del Proyecto Veterinaria Inteligente IFTS 12</a>
      </div>
    </div>
  </div>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def home_page():
    """Página de inicio principal del sistema Veterinaria Inteligente"""
    return HTMLResponse(content=HTML_HOME)
