# 👥 Instrucciones para Colaboradores
## Proyecto Veterinaria Inteligente - IFTS-12 (2025)

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- ✅ **Git** (para clonar el repositorio)
- ✅ **Python 3.11** o superior
- ✅ **Visual Studio Code** (recomendado)

---

## 🚀 OPCIÓN 1: Clonar y Ejecutar (Pasos Completos)

### Paso 1: Clonar el Repositorio

Abre tu terminal (PowerShell, CMD o Git Bash) y ejecuta:

```bash
git clone https://github.com/ATorchia-tech/veterinaria-inteligente.git
```

**Nota:** Si te pide usuario y contraseña:
- **Usuario:** Tu nombre de usuario de GitHub
- **Contraseña:** Debes usar un **Personal Access Token** (no tu contraseña normal)
  - Crear token en: https://github.com/settings/tokens
  - Permisos necesarios: `repo` (acceso completo a repositorios)

### Paso 2: Entrar al Directorio del Proyecto

```bash
cd veterinaria-inteligente
```

### Paso 3: Crear Entorno Virtual (Recomendado)

**En Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**En Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 4: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 5: Crear la Base de Datos

```bash
alembic upgrade head
```

### Paso 6: (Opcional) Llenar la BD con Datos de Prueba

```bash
python -m app.db.seed
```

### Paso 7: Ejecutar el Servidor

```bash
uvicorn app.main:app --reload
```

### Paso 8: Abrir en el Navegador

Ir a: **http://127.0.0.1:8000**

---

## ⚡ OPCIÓN 2: Usar VS Code (MÁS FÁCIL)

Si tienes **Visual Studio Code** instalado:

### Paso 1: Clonar desde VS Code

1. Abrir VS Code
2. Presionar `Ctrl + Shift + P` (o `Cmd + Shift + P` en Mac)
3. Escribir: `Git: Clone`
4. Pegar la URL: `https://github.com/ATorchia-tech/veterinaria-inteligente.git`
5. Seleccionar dónde guardar el proyecto
6. Click en "Open" cuando pregunte si quieres abrir el repositorio

### Paso 2: Abrir Terminal Integrada

Presionar: `Ctrl + Ñ` (o `Ctrl + ~` en algunos teclados)

### Paso 3: Ejecutar Setup Automático

**En Windows (PowerShell):**
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos
alembic upgrade head

# Datos de prueba (opcional)
python -m app.db.seed
```

### Paso 4: Ejecutar con las Tareas Configuradas

VS Code ya tiene tareas configuradas. Presiona:

`Ctrl + Shift + P` → Escribir: `Tasks: Run Task` → Seleccionar: **"Run API"**

O simplemente:

**Presionar `F5`** para ejecutar en modo debug.

---

## 🔄 Mantener tu Copia Actualizada

Cuando el equipo haga cambios, actualiza tu copia local:

```bash
git pull origin main
```

Si hiciste cambios locales y quieres subirlos:

```bash
git add .
git commit -m "Descripción de tus cambios"
git push origin main
```

---

## 🌐 Acceder a las Secciones del Proyecto

Una vez que el servidor esté corriendo, puedes acceder a:

| Sección | URL |
|---------|-----|
| 🏠 **Inicio** | http://127.0.0.1:8000/ |
| 📋 **Panel de Recepción** | http://127.0.0.1:8000/ui |
| 🩺 **Panel Veterinario** | http://127.0.0.1:8000/vet/ |
| 🤖 **Dashboard IA** | http://127.0.0.1:8000/ai-dashboard/ |
| 📊 **Estadísticas DB** | http://127.0.0.1:8000/admin/db-counts |
| 📄 **Presentación Proyecto** | http://127.0.0.1:8000/admin/presentation |
| 📚 **Documentación API** | http://127.0.0.1:8000/docs |

---

## 🧪 Ejecutar Tests

```bash
pytest
```

O con más detalle:

```bash
pytest -v
```

---

## 🛠️ Tareas Disponibles en VS Code

El proyecto tiene configuradas estas tareas (presiona `Ctrl + Shift + P` → `Tasks: Run Task`):

- **Run API** - Inicia el servidor
- **Tests** - Ejecuta los tests
- **Format (black)** - Formatea el código
- **Lint (ruff)** - Verifica errores de estilo
- **Reset DB + Seed + Run (UI)** - Resetea BD, carga datos y ejecuta
- **Seed DB** - Solo carga datos de prueba
- **DB Upgrade (head)** - Aplica migraciones de BD
- **Train No-Show Model** - Entrena modelo de predicción
- **Train Sentiment Model** - Entrena modelo de sentimientos
- **Train Intent Model** - Entrena modelo de intenciones

---

## 🆘 Solución de Problemas

### Error: "Python no se reconoce como comando"

**Solución:** Instala Python desde https://www.python.org/downloads/

Asegúrate de marcar la opción **"Add Python to PATH"** durante la instalación.

### Error: "git no se reconoce como comando"

**Solución:** Instala Git desde https://git-scm.com/downloads

### Error: "No se puede ejecutar scripts en este sistema"

**Solución en PowerShell (solo primera vez):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "ModuleNotFoundError: No module named 'app'"

**Solución:** Asegúrate de estar en el directorio raíz del proyecto y que el entorno virtual esté activado.

### Error: "SQLite database is locked"

**Solución:** Cierra todas las instancias del servidor y elimina el archivo `.db-wal` si existe:
```bash
del veterinaria.db-wal
del veterinaria.db-shm
```

### Error al hacer `git push`: "Authentication failed"

**Solución:** Necesitas un Personal Access Token:

1. Ir a: https://github.com/settings/tokens
2. Click en "Generate new token (classic)"
3. Nombre: `veterinaria-inteligente-access`
4. Permisos: Marcar `repo` (todos los sub-items)
5. Click en "Generate token"
6. **COPIAR EL TOKEN** (solo se muestra una vez)
7. Usar ese token como contraseña cuando Git lo pida

---

## 📁 Estructura del Proyecto

```
veterinaria-inteligente/
├── app/                    # Código principal
│   ├── api/               # Endpoints de la API
│   │   └── routers/       # Rutas organizadas
│   ├── core/              # Configuración
│   ├── db/                # Base de datos y modelos
│   ├── ml/                # Modelos de Machine Learning
│   ├── schemas/           # Esquemas Pydantic
│   └── services/          # Lógica de negocio
├── alembic/               # Migraciones de BD
├── docs/                  # Documentación
├── scripts/               # Scripts de automatización
├── tests/                 # Tests unitarios
├── requirements.txt       # Dependencias Python
├── alembic.ini           # Configuración Alembic
└── pyproject.toml        # Configuración del proyecto
```

---

## 👥 Colaboradores

- **Adriana Mercado**
- **Sofía Paniagua**
- **Franco Hernández**
- **Aroldo Torchia**

**Docente:** [Nombre del profesor/a]

**Institución:** IFTS-12  
**Año:** 2025

---

## 📞 Contacto

Si tienes problemas o preguntas, contacta a cualquier miembro del equipo o abre un **Issue** en GitHub:

https://github.com/ATorchia-tech/veterinaria-inteligente/issues

---

## 📖 Recursos Adicionales

- **Documentación FastAPI:** https://fastapi.tiangolo.com/
- **Documentación SQLAlchemy:** https://docs.sqlalchemy.org/
- **Documentación Git:** https://git-scm.com/doc
- **Guía Python Virtual Environments:** https://docs.python.org/3/tutorial/venv.html

---

¡Bienvenido al equipo! 🎉
