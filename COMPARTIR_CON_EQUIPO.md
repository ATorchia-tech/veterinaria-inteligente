# 🌐 CÓMO COMPARTIR CON TU EQUIPO Y DOCENTE

## ⚠️ IMPORTANTE: GitHub Codespaces NO comparte enlaces

GitHub Codespaces es **individual**. Cada persona debe crear su propio Codespace. No hay una URL única para compartir.

---

## ✅ SOLUCIÓN RECOMENDADA: Usar Replit (UNA SOLA URL para todos)

### 📍 Pasos para crear tu aplicación web pública:

#### **Paso 1:** Ir a Replit
```
https://replit.com
```

#### **Paso 2:** Crear cuenta gratis
- Puedes usar tu cuenta de GitHub para iniciar sesión rápidamente

#### **Paso 3:** Importar desde GitHub
1. Click en el botón **"Create Repl"**
2. Seleccionar **"Import from GitHub"**
3. Pegar tu URL de GitHub:
   ```
   https://github.com/ATorchia-tech/veterinaria-inteligente
   ```
4. Click en **"Import from GitHub"**

#### **Paso 4:** Configurar el Run Command
Replit debería detectar automáticamente que es Python, pero verifica que el comando Run sea:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Si no está configurado:
1. Click en el ícono de **configuración** (⚙️)
2. En "Run command" pegar el comando de arriba

#### **Paso 5:** Instalar dependencias (primera vez)
En la consola de Replit, ejecutar:
```bash
pip install -r requirements.txt
alembic upgrade head
```

#### **Paso 6:** Ejecutar
1. Click en el botón verde **"Run"** ▶️
2. Esperar que se inicie el servidor

#### **Paso 7:** Obtener la URL pública
Cuando se inicie, Replit te mostrará una URL como:
```
https://veterinaria-inteligente.tu-usuario.repl.co
```

#### **Paso 8:** ¡COMPARTIR ESA URL!
Esa URL es la que envías por email a tus compañeros y docente.

---

## 📧 EMAIL PARA ENVIAR AL EQUIPO

```
Asunto: Proyecto Veterinaria Inteligente - Acceso Web

Hola equipo,

Les comparto el acceso a nuestro proyecto. Pueden verlo directamente desde el navegador:

🌐 URL DE LA APLICACIÓN:
https://veterinaria-inteligente.[TU-USUARIO].repl.co

📖 SECCIONES PRINCIPALES:

• Inicio: https://[URL]/
• Panel de Recepción: https://[URL]/ui
• Panel Veterinario: https://[URL]/vet/
• Dashboard IA: https://[URL]/ai-dashboard/
• Presentación del Proyecto: https://[URL]/admin/presentation
• Documentación API: https://[URL]/docs

👥 EQUIPO IFTS-12:
• Adriana Mercado
• Sofía Paniagua
• Franco Hernández
• Aroldo Torchia

Sistema de Gestión Veterinaria con IA
Año 2025

¡Saludos!
```

---

## 🆚 ALTERNATIVA: Gitpod (también genera URL pública)

Si Replit no te funciona, puedes usar **Gitpod**:

### Enlace directo:
```
https://gitpod.io/#https://github.com/ATorchia-tech/veterinaria-inteligente
```

1. Tus compañeros abren ese enlace
2. Inician sesión con GitHub
3. Gitpod crea un workspace automáticamente
4. El servidor se inicia solo
5. Aparece una URL pública que pueden usar

---

## 📊 COMPARACIÓN

| Característica | Replit | Gitpod | Codespaces |
|---------------|--------|--------|------------|
| **URL única para todos** | ✅ SÍ | ❌ No (cada uno crea su workspace) | ❌ No (cada uno crea su codespace) |
| **Gratis** | ✅ Ilimitado | ✅ 50 hrs/mes | ✅ 60 hrs/mes |
| **Facilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Mejor para** | Compartir con equipo | Desarrollo individual | Desarrollo individual |

---

## 💡 MI RECOMENDACIÓN

### Para compartir con compañeros y docente:
👉 **USA REPLIT** - Es la única opción que te da una URL permanente que todos pueden usar.

### Para que cada uno tenga su propio ambiente:
👉 **USA GITPOD o CODESPACES** - Cada persona crea su propia instancia.

---

## 🆘 ¿PROBLEMAS CON REPLIT?

Si Replit no te permite hacer Deploy público o te pide pago, usa esta alternativa:

### **Railway.app** (otra opción con URL pública gratis):

1. Ir a: https://railway.app
2. Iniciar sesión con GitHub
3. Click en "New Project"
4. Seleccionar "Deploy from GitHub repo"
5. Elegir `veterinaria-inteligente`
6. Railway detectará Python automáticamente
7. En Settings:
   - Build Command: `pip install -r requirements.txt && alembic upgrade head`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
8. Deploy
9. Railway te dará una URL pública tipo: `https://tu-proyecto.up.railway.app`

**Nota:** Railway da $5 de crédito gratis mensual (suficiente para proyectos pequeños).

---

## ✅ RESUMEN RÁPIDO

1. **¿Quieres UNA URL para todos?** → Usa **Replit** o **Railway**
2. **¿Cada uno con su ambiente?** → Envía instrucciones de **Gitpod** o **Codespaces**
3. **¿La más fácil?** → **Replit**
4. **¿La más profesional?** → **Railway**

---

## 📞 SOPORTE

Si tienes problemas con alguna de estas opciones, avísame y te ayudo paso a paso.
