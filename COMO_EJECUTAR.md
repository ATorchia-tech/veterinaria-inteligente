# 🚀 Cómo Ejecutar este Proyecto (Para Compañeros y Docente)

## ✨ Opción Más Fácil: GitHub Codespaces (RECOMENDADA)

**No necesitas instalar NADA en tu computadora. Todo funciona en el navegador.**

### 📋 Pasos Simples:

1. **Ve al repositorio:**
   ```
   https://github.com/ATorchia-tech/veterinaria-inteligente
   ```

2. **Haz click en el botón verde "Code"** (arriba a la derecha)

3. **Selecciona la pestaña "Codespaces"**

4. **Click en "Create codespace on main"**

5. **Espera 2-3 minutos** mientras se prepara el entorno
   - Se instalará Python
   - Se instalarán las dependencias
   - Se creará la base de datos
   - Se iniciará el servidor automáticamente

6. **Cuando termine, verás un mensaje:**
   ```
   Your application running on port 8000 is available.
   ```

7. **Click en "Open in Browser"**

8. **¡Listo! Ya puedes usar la aplicación** 🎉
   - URL será algo como: `https://[nombre-aleatorio]-8000.app.github.dev`

### 🔗 URLs Disponibles:

Una vez que la app esté corriendo, puedes acceder a:

- **Página Principal:** `/`
- **Panel de Recepción:** `/ui`
- **Panel Veterinario:** `/vet/`
- **Dashboard IA:** `/ai-dashboard/`
- **Presentación del Proyecto:** `/admin/presentation`
- **Documentación API:** `/docs`

### ⏱️ Tiempo de Uso:

- GitHub te da **60 horas GRATIS por mes**
- Más que suficiente para probar y mostrar el proyecto
- El entorno se apaga automáticamente después de 30 minutos de inactividad

### 💡 Consejos:

- **Para docente/evaluador:** Pueden crear su propio Codespace para probar
- **Para compañeros:** Pueden compartir la URL del Codespace mientras está activo
- **Para presentaciones:** Inicia el Codespace antes de la clase

---

## 🖥️ Opción 2: Ejecutar Localmente (Si tienen Python instalado)

Si prefieres ejecutar en tu propia computadora:

### Requisitos:
- Python 3.10 o superior
- Git

### Pasos:

```bash
# 1. Clonar el repositorio
git clone https://github.com/ATorchia-tech/veterinaria-inteligente.git
cd veterinaria-inteligente

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Crear base de datos
alembic upgrade head

# 6. Iniciar servidor
uvicorn app.main:app --reload
```

Luego abre tu navegador en: `http://127.0.0.1:8000`

---

## 📧 Compartir con el Equipo

### Para el Docente/Evaluador:

```
Asunto: Acceso al Proyecto Veterinaria Inteligente - IFTS-12

Profesor/a,

Le comparto el acceso a nuestro proyecto:

📂 REPOSITORIO:
https://github.com/ATorchia-tech/veterinaria-inteligente

🚀 FORMA MÁS FÁCIL DE PROBARLO (sin instalar nada):

1. Ir al repositorio
2. Click en botón verde "Code"
3. Pestaña "Codespaces"
4. Click "Create codespace on main"
5. Esperar 2-3 minutos
6. Cuando aparezca el mensaje del puerto 8000, click en "Open in Browser"

📖 DOCUMENTACIÓN:
- Presentación del proyecto: /admin/presentation
- Documentación técnica: /docs

👥 EQUIPO:
- Adriana Mercado
- Sofía Paniagua
- Franco Hernández
- Aroldo Torchia

IFTS-12 - 2025
```

---

## ❓ Preguntas Frecuentes

**P: ¿Necesito cuenta en GitHub para usar Codespaces?**
R: Sí, es gratis. Solo necesitas crear una cuenta en github.com

**P: ¿Los datos se guardan?**
R: En Codespaces, los datos se guardan mientras el Codespace esté activo. Al apagarse, se reinicia.

**P: ¿Puedo compartir mi Codespace con otros?**
R: Sí, puedes hacer el puerto público y compartir la URL mientras esté activo.

**P: ¿Cuánto tiempo puedo usar Codespaces gratis?**
R: 60 horas al mes, renovables cada mes.

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que estés en la branch `main`
2. Asegúrate de que el puerto 8000 esté disponible
3. Consulta la documentación completa en `/docs`

---

**Proyecto Veterinaria Inteligente**  
**IFTS-12 - 2025**  
**Sistema de Gestión Veterinaria con Inteligencia Artificial**
