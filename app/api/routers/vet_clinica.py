from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


HTML_VET_CLINICA = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>🩺 Atención Clínica - Veterinaria Inteligente</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
      text-align: center;
      padding: 0.5rem 1rem;
      background: rgba(255,255,255,0.98);
      border-bottom: 2px solid #e2e8f0;
      flex-shrink: 0;
    }
    header h1 {
      margin: 0;
      font-size: 1.4rem;
      color: #333;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }
    header h1 .emoji {
      font-size: 1.6rem;
    }
    header p {
      margin: 0.2rem 0 0;
      color: #666;
      font-size: 0.75rem;
    }
    .nav-links {
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      justify-content: center;
      padding: 0.5rem 1rem;
      background: rgba(255,255,255,0.95);
      border-bottom: 1px solid #e2e8f0;
      flex-shrink: 0;
    }
    .nav-links a {
      padding: 0.35rem 0.7rem;
      background: #f0f4ff;
      color: #4a5568;
      text-decoration: none;
      border-radius: 6px;
      font-size: 0.7rem;
      transition: all 0.2s;
      border: 1px solid #e2e8f0;
      white-space: nowrap;
    }
    .nav-links a:hover {
      background: #667eea;
      color: #fff;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(102,126,234,0.4);
    }
    .main-content {
      flex: 1;
      overflow-y: auto;
      padding: 0.8rem;
      background: rgba(255,255,255,0.95);
    }
    .sections {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.8rem;
      max-width: 1400px;
      margin: 0 auto;
    }
    .section {
      background: #fff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      border: 1px solid #e2e8f0;
      transition: all 0.2s;
    }
    .section:hover {
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      border-color: #667eea;
    }
    .section-header {
      font-weight: 600;
      font-size: 0.9rem;
      color: #fff;
      padding: 0.6rem 0.8rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .section-header .icon {
      font-size: 1rem;
    }
    .section-content {
      padding: 0.8rem;
    }
    .section-content > p:first-child {
      margin-top: 0;
      color: #666;
      font-size: 0.7rem;
      margin-bottom: 0.6rem;
    }
    label {
      display: block;
      margin: 0.5rem 0 0.2rem;
      font-size: 0.7rem;
      font-weight: 600;
      color: #4a5568;
    }
    input, select, textarea {
      width: 100%;
      padding: 0.4rem 0.6rem;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      font-size: 0.75rem;
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
      margin-top: 0.5rem;
      padding: 0.45rem 0.9rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: #fff;
      border: 0;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      font-size: 0.75rem;
      transition: all 0.2s;
      box-shadow: 0 2px 6px rgba(102,126,234,0.3);
    }
    button:hover {
      transform: translateY(-1px);
      box-shadow: 0 3px 10px rgba(102,126,234,0.4);
    }
    button:active {
      transform: translateY(0);
    }
    small {
      display: block;
      margin-top: 0.3rem;
      color: #718096;
      font-size: 0.65rem;
      line-height: 1.3;
    }
    small a {
      color: #667eea;
      text-decoration: none;
    }
    small a:hover {
      text-decoration: underline;
    }
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.6rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1><span class="emoji">🩺</span> Atención Clínica</h1>
      <p>Panel del Veterinario - Módulo de Atención de Mascotas</p>
    </header>

    <div class="nav-links">
      <a href="/">🏠 IR A INICIO</a>
      <a href="/vet">🩺 PANEL PRINCIPAL DEL VETERINARIO</a>
      <a href="/vet/gestion">📊 GESTIÓN VETERINARIA</a>
      <a href="/ui">👥 PANEL RECEPCIÓN</a>
      <a href="/admin/db_details" target="_blank">📊 DETALLE DE DATOS</a>
      <a href="/admin/db_counts_form" target="_blank">🔢 TOTALES</a>
      <a href="/admin/api_docs_friendly" target="_blank">📖 API DOCS</a>
    </div>

    <div class="main-content">
      <div class="sections">
        <!-- Sección 1: Consulta de Historial Clínico -->
        <div class="section">
          <div class="section-header">
            <span class="icon">📋</span> Consulta de Historial Clínico
          </div>
          <div class="section-content">
            <p>Buscá el historial de una mascota por nombre o dueño.</p>
            
            <div class="grid-2">
              <div>
                <label>Nombre de mascota</label>
                <input type="text" id="search-pet" placeholder="Ej: Firulais" />
                <button onclick="searchByPet()">🔍 Buscar</button>
              </div>
              <div>
                <label>Nombre de dueño</label>
                <input type="text" id="search-owner" placeholder="Ej: Juan Pérez" />
                <button onclick="searchByOwner()">🔍 Buscar</button>
              </div>
            </div>

            <script>
              function searchByPet() {
                const name = document.getElementById('search-pet').value.trim();
                if (!name) {
                  alert('Por favor ingresá el nombre de la mascota');
                  return;
                }
                window.open('/pets/search/view?name=' + encodeURIComponent(name), '_blank');
              }
              function searchByOwner() {
                const name = document.getElementById('search-owner').value.trim();
                if (!name) {
                  alert('Por favor ingresá el nombre del dueño');
                  return;
                }
                window.open('/owners/search/view?name=' + encodeURIComponent(name), '_blank');
              }
            </script>
          </div>
        </div>

        <!-- Sección 2: Registro de Atención Médica -->
        <div class="section">
          <div class="section-header">
            <span class="icon">📝</span> Registro de Atención Médica
          </div>
          <div class="section-content">
            <p>Registrá una consulta médica.</p>
            
            <form method="post" action="/records/form">
              <label>ID mascota</label>
              <input type="number" name="pet_id" min="1" placeholder="1" required />

              <label>Síntomas</label>
              <textarea name="symptoms" placeholder="Ej: Tos, falta apetito"></textarea>

              <label>Diagnóstico</label>
              <textarea name="diagnosis" placeholder="Ej: Bronquitis leve" required></textarea>

              <label>Tratamiento</label>
              <textarea name="treatment" placeholder="Ej: Reposo, nebulizaciones"></textarea>

              <label>Medicamentos</label>
              <textarea name="medications" placeholder="Ej: Amoxicilina 250mg cada 12hs"></textarea>

              <button type="submit">✅ Registrar</button>
            </form>
          </div>
        </div>

        <!-- Sección 3: Récords Clínicos por Mascota -->
        <div class="section">
          <div class="section-header">
            <span class="icon">🗂️</span> Récords Clínicos
          </div>
          <div class="section-content">
            <p>Consultá atenciones médicas de una mascota.</p>

            <label>ID mascota</label>
            <input type="number" id="records-pet-id" min="1" placeholder="1" />
            <button onclick="viewPetRecords()">📋 Ver récords</button>

            <script>
              function viewPetRecords() {
                const petId = document.getElementById('records-pet-id').value;
                if (!petId || petId < 1) {
                  alert('Por favor ingresá un ID válido');
                  return;
                }
                window.open('/records/view?pet_id=' + encodeURIComponent(petId), '_blank');
              }
            </script>
          </div>
        </div>

        <!-- Sección 4: Ficha Completa de Mascota -->
        <div class="section">
          <div class="section-header">
            <span class="icon">🐕‍🦺</span> Ficha Completa
          </div>
          <div class="section-content">
            <p>Consultá toda la información de una mascota.</p>

            <label>ID mascota</label>
            <input type="number" id="full-pet-id" min="1" placeholder="1" />
            
            <div class="grid-2">
              <button onclick="viewPetInfo()">📄 Info</button>
              <button onclick="viewPetRecordsFull()">📋 Récords</button>
            </div>
            <div class="grid-2">
              <button onclick="viewPetAppointments()">📅 Turnos</button>
              <button onclick="viewPetVaccinations()">💉 Vacunas</button>
            </div>

            <script>
              function viewPetInfo() {
                const petId = document.getElementById('full-pet-id').value;
                if (!petId || petId < 1) {
                  alert('Por favor ingresá un ID válido');
                  return;
                }
                window.open('/pets/' + encodeURIComponent(petId) + '/view', '_blank');
              }
              function viewPetRecordsFull() {
                const petId = document.getElementById('full-pet-id').value;
                if (!petId || petId < 1) {
                  alert('Por favor ingresá un ID válido');
                  return;
                }
                window.open('/records/view?pet_id=' + encodeURIComponent(petId), '_blank');
              }
              function viewPetAppointments() {
                const petId = document.getElementById('full-pet-id').value;
                if (!petId || petId < 1) {
                  alert('Por favor ingresá un ID válido');
                  return;
                }
                window.open('/appointments/view?pet_id=' + encodeURIComponent(petId), '_blank');
              }
              function viewPetVaccinations() {
                const petId = document.getElementById('full-pet-id').value;
                if (!petId || petId < 1) {
                  alert('Por favor ingresá un ID válido');
                  return;
                }
                window.open('/vaccinations/view?pet_id=' + encodeURIComponent(petId), '_blank');
              }
            </script>
          </div>
        </div>

      </div>
    </div>
  </div>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def vet_clinica_home():
    return HTMLResponse(content=HTML_VET_CLINICA)
