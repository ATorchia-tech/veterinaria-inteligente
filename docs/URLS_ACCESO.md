# 🌐 URLs de Acceso - Veterinaria Inteligente

## 🏠 Página Principal
**URL**: http://127.0.0.1:8000  
**Descripción**: Pantalla inicial con 3 grandes botones
- 👥 Panel Recepcionista
- 🩺 Panel Veterinario  
- 🤖 Predicción de Turnos con IA

---

## 📱 Interfaces de Usuario

### Panel Recepcionista
**URL**: http://127.0.0.1:8000/ui  
**Funciones**:
- Crear nuevos dueños
- Registrar mascotas
- Agendar turnos

### Panel Veterinario
**URL**: http://127.0.0.1:8000/vet  
**Módulos**:
- 🩺 Atención Clínica: http://127.0.0.1:8000/vet/clinica
- 📊 Gestión Veterinaria: http://127.0.0.1:8000/vet/gestion

### Dashboard de Predicción con IA
**URL**: http://127.0.0.1:8000/ai-dashboard  
**Características**:
- Pronóstico del tiempo de Buenos Aires (5 días)
- Predicción de afluencia semanal
- Probabilidad de inasistencia por horario
- Recomendaciones operativas

---

## 🤖 API de Inteligencia Artificial

### Pronóstico del Tiempo
```http
GET http://127.0.0.1:8000/ai/forecast?days=5
```
**Respuesta**: Datos meteorológicos reales de Buenos Aires

### Predicción de Afluencia
```http
GET http://127.0.0.1:8000/ai/predict?day=2025-11-11
```
**Respuesta**: Predicción (Alta/Media/Baja) con probabilidad

### Predicción de No-Show
```http
GET http://127.0.0.1:8000/ai/noshow?day=2025-11-11&hour=15
```
**Respuesta**: Probabilidad de inasistencia para un horario específico

### Análisis de Sentimiento
```http
POST http://127.0.0.1:8000/ai/sentiment
Content-Type: application/json

{
  "text": "Mi perro está muy bien después del tratamiento"
}
```

### Detección de Intención
```http
POST http://127.0.0.1:8000/ai/intent
Content-Type: application/json

{
  "text": "Necesito agendar una consulta para vacunar a mi gato"
}
```

---

## 📊 Administración

### Base de Datos
- **Detalles**: http://127.0.0.1:8000/admin/db_details
- **Contadores**: http://127.0.0.1:8000/admin/db_counts_form

### API REST
- **Dueños**: http://127.0.0.1:8000/owners/view
- **Mascotas**: http://127.0.0.1:8000/pets/view
- **Turnos**: http://127.0.0.1:8000/appointments/view

---

## 📖 Documentación

### Interactive API Docs (Swagger)
**URL**: http://127.0.0.1:8000/docs  
**Descripción**: Documentación interactiva completa de la API

### Alternative API Docs (ReDoc)
**URL**: http://127.0.0.1:8000/redoc  
**Descripción**: Documentación alternativa estilo libro

---

## 🔧 Endpoints Útiles

### Health Check
```http
GET http://127.0.0.1:8000/health
```

### Reportes
```http
GET http://127.0.0.1:8000/reports/summary
GET http://127.0.0.1:8000/reports/vaccinations-due
```

### Horarios
```http
GET http://127.0.0.1:8000/schedule/availability
```

---

## 🚀 Inicio Rápido

### Opción 1: Navegador Web
Simplemente abre tu navegador y ve a:
```
http://127.0.0.1:8000
```

### Opción 2: PowerShell (Pruebas)
```powershell
# Probar que el servidor está activo
Invoke-WebRequest -Uri 'http://127.0.0.1:8000/health' -UseBasicParsing

# Ver pronóstico del tiempo
(Invoke-WebRequest -Uri 'http://127.0.0.1:8000/ai/forecast?days=5' -UseBasicParsing).Content | ConvertFrom-Json

# Abrir página principal en navegador
Start-Process "http://127.0.0.1:8000"
```

### Opción 3: cURL (Linux/Mac/Git Bash)
```bash
# Health check
curl http://127.0.0.1:8000/health

# Pronóstico
curl http://127.0.0.1:8000/ai/forecast?days=5

# Predicción
curl http://127.0.0.1:8000/ai/predict
```

---

## 📝 Notas Importantes

1. **Puerto**: El servidor debe estar ejecutándose en el puerto **8000**
2. **Host**: Por defecto en **127.0.0.1** (localhost)
3. **Tarea VS Code**: Usa la tarea "Run API" para iniciar el servidor
4. **Auto-reload**: El servidor se recarga automáticamente con los cambios

---

## 🎯 Flujo de Uso Recomendado

1. **Inicio** → http://127.0.0.1:8000
2. Seleccionar panel según rol:
   - **Recepcionista** → Carga de datos
   - **Veterinario** → Atención clínica o gestión
   - **Administrador** → Dashboard de predicción IA
3. Usar funcionalidades específicas de cada módulo
4. Consultar documentación API si es necesario

---

## 🌟 Características Destacadas

### 🤖 Predicción con Datos Reales
El dashboard de IA utiliza datos meteorológicos reales de **Open-Meteo API** para:
- Buenos Aires, Argentina
- Pronóstico de 5-7 días
- Actualización en tiempo real
- Sin necesidad de API key

### 📱 Interfaz Amigable
- Diseño responsive (móvil/tablet/desktop)
- Iconos intuitivos
- Colores profesionales
- Navegación clara

### 🎨 Profesional y Moderno
- Gradientes de color
- Animaciones suaves
- Tarjetas interactivas
- Feedback visual

---

*Documento generado: 11 de noviembre de 2025*  
*Proyecto IFTS-12 - Veterinaria Inteligente*
