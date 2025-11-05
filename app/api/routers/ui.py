from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


HTML_PAGE = """
<!doctype html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Veterinaria Inteligente · UI simple</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 1.5rem; }
    .wrap { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1rem; }
    fieldset { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; }
    legend { font-weight: 700; }
    label { display: block; margin: .35rem 0 .15rem; font-size: .95rem; }
    input, select, textarea { width: 100%; padding: .5rem .6rem; border: 1px solid #ccc; border-radius: 6px; }
    button { margin-top: .75rem; padding: .6rem 1rem; background: #1f7aec; color: #fff; border: 0; border-radius: 6px; cursor: pointer; }
    button:hover { background: #1666c6; }
    .links { margin: 1rem 0; }
    .links a { margin-right: .75rem; }
    small { color: #666; }
    .note { background: #f6f8fa; border: 1px solid #e4e7ea; padding: .75rem; border-radius: 6px; }
  </style>
</head>
<body>
  <h1>Veterinaria Inteligente · Carga rápida</h1>
  <p class=\"note\">Esta es una UI mínima para cargar datos. Las APIs completas están en <a href=\"/docs\">/docs</a>.</p>

  <div class=\"links\">
    <a href=\"/owners\" target=\"_blank\">Ver dueños (JSON)</a>
    <a href=\"/pets\" target=\"_blank\">Ver mascotas (JSON)</a>
    <a href=\"/appointments\" target=\"_blank\">Ver turnos (JSON)</a>
    <a href=\"/redoc\" target=\"_blank\">ReDoc</a>
  </div>

  <div class=\"wrap\">
    <form method=\"post\" action=\"/owners/form\">
      <fieldset>
        <legend>Nuevo dueño</legend>
        <label>Nombre</label>
        <input name=\"name\" placeholder=\"Juan Pérez\" required />
        <label>Teléfono</label>
        <input name=\"phone\" placeholder=\"123456\" />
        <label>Email</label>
        <input type=\"email\" name=\"email\" placeholder=\"juan@example.com\" />
        <button type=\"submit\">Crear dueño</button>
        <small>Se abrirá una respuesta JSON con el registro creado.</small>
      </fieldset>
    </form>

    <form method=\"post\" action=\"/pets/form\">
      <fieldset>
        <legend>Nueva mascota</legend>
        <label>Nombre</label>
        <input name=\"name\" placeholder=\"Firulais\" required />
        <label>Especie</label>
        <input name=\"species\" placeholder=\"perro\" required />
        <label>Raza</label>
        <input name=\"breed\" placeholder=\"mestizo\" />
        <label>Fecha de nacimiento</label>
        <input type=\"date\" name=\"birth_date\" />
        <label>Notas</label>
        <textarea name=\"notes\" placeholder=\"vacunas al día\"></textarea>
        <label>ID del dueño</label>
        <input type=\"number\" min=\"1\" name=\"owner_id\" placeholder=\"1\" required />
        <button type=\"submit\">Crear mascota</button>
        <small>Usá el <em>ID</em> de un dueño existente.</small>
      </fieldset>
    </form>

    <form method=\"post\" action=\"/appointments/form\">
      <fieldset>
        <legend>Nuevo turno</legend>
        <label>Fecha y hora</label>
        <input name=\"date\" placeholder=\"2025-11-05T15:00:00\" required />
        <label>Motivo</label>
        <input name=\"reason\" placeholder=\"control anual\" required />
        <label>ID de mascota</label>
        <input type=\"number\" min=\"1\" name=\"pet_id\" placeholder=\"1\" required />
        <button type=\"submit\">Crear turno</button>
        <small>Debe existir la mascota (ver <a href=\"/pets\" target=\"_blank\">/pets</a>).</small>
      </fieldset>
    </form>
  </div>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def ui_home():
    return HTMLResponse(content=HTML_PAGE)
