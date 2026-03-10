from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


HTML_PAGE = """
<!doctype html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>🐾 Veterinaria Inteligente</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
      border-bottom: 2px solid #667eea;
      flex-shrink: 0;
    }
    
    .top-header .team-info {
      font-size: 0.8rem;
      color: #4a5568;
      font-weight: 600;
    }
    
    .top-header .btn-home {
      padding: 0.4rem 1rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      text-decoration: none;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.85rem;
      transition: all 0.3s;
      box-shadow: 0 2px 6px rgba(102, 126, 234, 0.3);
    }
    
    .top-header .btn-home:hover {
      transform: translateY(-1px);
      box-shadow: 0 3px 10px rgba(102, 126, 234, 0.4);
    }
    
    /* Contenedor principal con scroll interno */
    .content-wrapper {
      flex: 1;
      overflow-y: auto;
      padding: 1rem 1.5rem;
    }
    
    .container {
      max-width: 1400px;
      margin: 0 auto;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 15px 40px rgba(0,0,0,0.25);
      padding: 1.25rem;
      height: 100%;
      display: flex;
      flex-direction: column;
    }
    
    /* Header interno compacto */
    header {
      text-align: center;
      padding-bottom: 0.75rem;
      border-bottom: 2px solid #f0f0f0;
      flex-shrink: 0;
    }
    header h1 {
      font-size: 1.6rem;
      color: #333;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      margin-bottom: 0.25rem;
    }
    header h1 .emoji {
      font-size: 1.8rem;
    }
    header p {
      color: #666;
      font-size: 0.85rem;
    }
    
    /* Links compactos */
    .links {
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      justify-content: center;
      margin: 0.75rem 0;
      flex-shrink: 0;
    }
    .links a {
      padding: 0.35rem 0.7rem;
      background: #f0f4ff;
      color: #4a5568;
      text-decoration: none;
      border-radius: 6px;
      font-size: 0.75rem;
      transition: all 0.2s;
      border: 1px solid #e2e8f0;
    }
    .links a:hover {
      background: #667eea;
      color: #fff;
      transform: translateY(-1px);
    }
    
    /* Grid de formularios en 3 columnas */
    .wrap {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      flex: 1;
      overflow-y: auto;
      margin-top: 0.75rem;
    }
    
    form {
      background: #fff;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 3px 5px rgba(0,0,0,0.08);
      border: 2px solid #e2e8f0;
      transition: all 0.3s;
      display: flex;
      flex-direction: column;
      height: fit-content;
    }
    form:hover {
      box-shadow: 0 8px 20px rgba(0,0,0,0.12);
      border-color: #667eea;
    }
    
    fieldset {
      border: none;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      flex: 1;
    }
    
    legend {
      font-weight: 700;
      font-size: 1.05rem;
      padding: 0.6rem 1rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: #fff;
      margin: -1rem -1rem 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    legend .icon {
      font-size: 1.2rem;
    }
    
    label {
      display: block;
      margin: 0.4rem 0 0.2rem;
      font-size: 0.8rem;
      font-weight: 600;
      color: #4a5568;
    }
    
    input, select, textarea {
      width: 100%;
      padding: 0.45rem 0.6rem;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      font-size: 0.8rem;
      transition: all 0.2s;
      font-family: inherit;
    }
    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: #667eea;
      box-shadow: 0 0 0 2px rgba(102,126,234,0.1);
    }
    
    textarea {
      resize: vertical;
      min-height: 50px;
    }
    
    button {
      margin-top: 0.75rem;
      padding: 0.6rem 1rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: #fff;
      border: 0;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      font-size: 0.85rem;
      width: 100%;
      transition: all 0.3s;
      box-shadow: 0 3px 8px rgba(102,126,234,0.3);
    }
    button:hover {
      transform: translateY(-1px);
      box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }
    
    small {
      display: block;
      margin-top: 0.4rem;
      color: #718096;
      font-size: 0.7rem;
      line-height: 1.3;
    }
    small a {
      color: #667eea;
      text-decoration: none;
    }
    small a:hover {
      text-decoration: underline;
    }
    
    /* Scrollbar personalizada */
    .content-wrapper::-webkit-scrollbar,
    .wrap::-webkit-scrollbar {
      width: 8px;
    }
    .content-wrapper::-webkit-scrollbar-track,
    .wrap::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: 10px;
    }
    .content-wrapper::-webkit-scrollbar-thumb,
    .wrap::-webkit-scrollbar-thumb {
      background: #667eea;
      border-radius: 10px;
    }
    .content-wrapper::-webkit-scrollbar-thumb:hover,
    .wrap::-webkit-scrollbar-thumb:hover {
      background: #764ba2;
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
      <h1><span class=\"emoji\">🐾</span> Veterinaria Inteligente</h1>
      <p>Panel de recepción · Carga rápida de datos</p>
    </header>

    <div class=\"links\">
      <a href=\"/vet\">🩺 Panel Veterinario</a>
      <a href=\"/owners/view\" target=\"_blank\">📋 Ver dueños</a>
      <a href=\"/pets/view\" target=\"_blank\">🐶 Ver mascotas</a>
      <a href=\"/appointments/view\" target=\"_blank\">📅 Ver turnos</a>
      <a href=\"/admin/db_details\" target=\"_blank\">📊 Detalle de datos</a>
      <a href=\"/admin/db_counts_form\" target=\"_blank\">🔢 Totales</a>
      <a href=\"/admin/api_docs_friendly\" target=\"_blank\">📖 API Docs</a>
    </div>

    <div class=\"wrap\">
      <form method=\"post\" action=\"/owners/form\">
        <fieldset>
          <legend><span class=\"icon\">👤</span> Nuevo dueño</legend>
          <label>Nombre completo</label>
          <input name=\"name\" placeholder=\"Ej: Juan Pérez\" required />
          <label>Teléfono</label>
          <input name=\"phone\" placeholder=\"Ej: 11-1234-5678\" />
          <label>Email</label>
          <input type=\"email\" name=\"email\" placeholder=\"juan@ejemplo.com\" />
          <button type=\"submit\">✅ Crear dueño</button>
          <small>Al enviar, se abrirá una página con los datos guardados en formato JSON.</small>
        </fieldset>
      </form>

      <form method=\"post\" action=\"/pets/form\">
        <fieldset>
          <legend><span class=\"icon\">🐕</span> Nueva mascota</legend>
          <label>Nombre de la mascota</label>
          <input name=\"name\" placeholder=\"Ej: Firulais\" required />
          <label>Especie</label>
          <input name=\"species\" placeholder=\"Ej: perro, gato\" required />
          <label>Raza</label>
          <input name=\"breed\" placeholder=\"Ej: mestizo, golden retriever\" />
          <label>Fecha de nacimiento</label>
          <input type=\"date\" name=\"birth_date\" />
          <label>Notas adicionales</label>
          <textarea name=\"notes\" placeholder=\"Ej: vacunas al día, castrado\"></textarea>
          <label>ID del dueño</label>
          <input type=\"number\" min=\"1\" name=\"owner_id\" placeholder=\"1\" required />
          <button type=\"submit\">✅ Crear mascota</button>
          <small>Recordá que el dueño ya debe existir. Podés consultar la lista en <a href=\"/owners/view\" target=\"_blank\">Ver dueños</a>.</small>
        </fieldset>
      </form>

      <form method=\"post\" action=\"/appointments/form\">
        <fieldset>
          <legend><span class=\"icon\">📅</span> Nuevo turno</legend>
          <label>Fecha y hora</label>
          <input name=\"date\" placeholder=\"Ej: 2025-11-11T15:00:00\" required />
          <label>Motivo de la consulta</label>
          <input name=\"reason\" placeholder=\"Ej: control anual, vacunación\" required />
          <label>ID de la mascota</label>
          <input type=\"number\" min=\"1\" name=\"pet_id\" placeholder=\"1\" required />
          <button type=\"submit\">✅ Crear turno</button>
          <small>La mascota debe existir en el sistema. Consultá la lista en <a href=\"/pets/view\" target=\"_blank\">Ver mascotas</a>.</small>
        </fieldset>
      </form>
    </div>
  </div>
  </div>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def ui_home():
    return HTMLResponse(content=HTML_PAGE)
