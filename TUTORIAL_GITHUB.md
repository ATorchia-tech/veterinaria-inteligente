# 📚 Tutorial: Subir Veterinaria-Inteligente a GitHub

## 👥 Equipo del Proyecto
- **Integrantes**: A. Mercado, S. Paniagua, F. Hernández, A. Torchia
- **Institución**: IFTS-12
- **Proyecto**: Sistema de Gestión Veterinaria con IA

---

## 🎯 Objetivo
Este tutorial te guiará paso a paso para:
1. ✅ Subir tu proyecto a GitHub
2. ✅ Dar acceso a tus 3 compañeros y al docente
3. ✅ Compartir un enlace para que ejecuten la aplicación desde su navegador

---

## 📋 PARTE 1: Subir el Proyecto a GitHub

### Paso 1: Crear una Cuenta en GitHub (si no tienes una)

1. Ve a: https://github.com
2. Haz clic en **"Sign up"** (Registrarse)
3. Completa el formulario con:
   - Tu email
   - Una contraseña segura
   - Un nombre de usuario (ejemplo: `ATorchia-tech`)
4. Verifica tu email
5. ✅ ¡Listo! Ya tienes cuenta en GitHub

### Paso 2: Crear un Repositorio Nuevo en GitHub

1. **Inicia sesión** en GitHub
2. En la esquina superior derecha, haz clic en el **botón "+"**
3. Selecciona **"New repository"** (Nuevo repositorio)
4. Completa la información:
   - **Repository name**: `veterinaria-inteligente`
   - **Description**: "Sistema de Gestión Veterinaria con IA - Proyecto IFTS-12"
   - **Visibilidad**: Selecciona **"Public"** (para que todos puedan verlo)
   - ⚠️ **NO marques** ninguna opción de README, .gitignore o license (ya tienes estos archivos)
5. Haz clic en **"Create repository"** (Crear repositorio)
6. ✅ Verás una página con instrucciones - ¡no te preocupes! Los siguientes pasos te dirán qué hacer

### Paso 3: Subir tu Código a GitHub desde VS Code

**Opción A: Usando la Terminal de VS Code** (Recomendado - Más rápido)

1. Abre VS Code con tu proyecto
2. Presiona ``Ctrl + Ñ`` para abrir la terminal
3. Copia y pega estos comandos **uno por uno**:

```powershell
# 1. Agregar todos los archivos al repositorio
git add .

# 2. Crear un commit con un mensaje descriptivo
git commit -m "Proyecto Veterinaria Inteligente IFTS-12 - Versión completa con IA"

# 3. Conectar tu repositorio local con GitHub (REEMPLAZA 'TU-USUARIO' con tu usuario de GitHub)
git remote set-url origin https://github.com/TU-USUARIO/veterinaria-inteligente.git

# 4. Subir el código a GitHub
git push -u origin main
```

4. Te pedirá tu **usuario** y **contraseña** de GitHub
   - ⚠️ **Importante**: En lugar de tu contraseña normal, necesitas un **Personal Access Token**

**¿Cómo crear un Personal Access Token?**

1. Ve a: https://github.com/settings/tokens
2. Haz clic en **"Generate new token"** → **"Generate new token (classic)"**
3. Dale un nombre: `VS Code - Veterinaria`
4. Marca el checkbox **"repo"** (para dar acceso completo al repositorio)
5. Haz clic en **"Generate token"** al final de la página
6. **COPIA el token** que aparece (solo lo verás una vez)
7. Usa este token como contraseña cuando Git te lo pida

5. ✅ Una vez que se complete el `git push`, tu código estará en GitHub!

**Opción B: Usando la Interfaz Gráfica de VS Code**

1. En VS Code, haz clic en el ícono de **Control de Código Fuente** (el tercer ícono del menú lateral izquierdo)
2. Verás una lista de archivos modificados
3. Haz clic en el **"+"** junto a "Changes" para agregar todos los archivos
4. Escribe un mensaje en la caja de texto: `"Proyecto completo Veterinaria Inteligente IFTS-12"`
5. Haz clic en el botón **"Commit"** (✓)
6. Haz clic en **"Sync Changes"** o el ícono de nube
7. Ingresa tus credenciales de GitHub cuando te lo pida

### Paso 4: Verificar que se Subió Correctamente

1. Ve a tu navegador
2. Entra a: `https://github.com/TU-USUARIO/veterinaria-inteligente`
3. ✅ Deberías ver todos tus archivos y carpetas

---

## 👥 PARTE 2: Dar Acceso a tus Compañeros y Docente

### Paso 1: Agregar Colaboradores

1. En tu repositorio de GitHub, ve a **"Settings"** (Configuración)
2. En el menú lateral izquierdo, haz clic en **"Collaborators"** (Colaboradores)
3. Haz clic en **"Add people"** (Agregar personas)
4. Escribe el **nombre de usuario** o **email** de cada compañero
5. Haz clic en **"Add [nombre] to this repository"**
6. Repite para cada compañero y el docente
7. ✅ Ellos recibirán un email de invitación

**Tus compañeros deben:**
1. Revisar su email
2. Aceptar la invitación
3. ¡Listo! Ya pueden ver y colaborar en el proyecto

---

## 🌐 PARTE 3: Compartir Enlace para Ejecutar la App (SIN Necesidad de VS Code)

**⚠️ IMPORTANTE: Para esto necesitarás desplegar la aplicación en un servicio en la nube**

Aquí tienes **3 opciones** ordenadas de más fácil a más compleja:

### OPCIÓN 1: Render.com (Gratis y Más Fácil) ⭐ RECOMENDADO

**Ventajas:**
- ✅ 100% Gratis
- ✅ No necesita tarjeta de crédito
- ✅ Muy fácil de configurar (5 minutos)
- ✅ Tu app estará en: `https://veterinaria-inteligente.onrender.com`

**Pasos:**

1. **Crear archivos necesarios**

   Primero, crea estos 2 archivos en la raíz de tu proyecto:

   **Archivo 1: `render.yaml`** (Crear nuevo archivo con este nombre)
   ```yaml
   services:
     - type: web
       name: veterinaria-inteligente
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.0
   ```

   **Archivo 2: Actualizar `.gitignore`** (Asegúrate de que incluya esto)
   ```
   veterinaria.db
   .env
   *.pyc
   __pycache__/
   .venv/
   ```

2. **Subir los cambios a GitHub**
   ```powershell
   git add .
   git commit -m "Agregar configuración para Render"
   git push
   ```

3. **Crear cuenta en Render**
   - Ve a: https://render.com
   - Haz clic en **"Get Started for Free"**
   - Inicia sesión con tu cuenta de **GitHub** (más fácil)
   - Autoriza a Render para acceder a tus repositorios

4. **Desplegar la aplicación**
   - En el Dashboard de Render, haz clic en **"New +"** → **"Web Service"**
   - Selecciona tu repositorio **"veterinaria-inteligente"**
   - Render detectará automáticamente el archivo `render.yaml`
   - Haz clic en **"Apply"** o **"Create Web Service"**
   - ⏳ Espera 5-10 minutos mientras Render construye tu app
   - ✅ Una vez que termine, verás un enlace como: `https://veterinaria-inteligente.onrender.com`

5. **Compartir el enlace**
   - Copia el enlace de tu app
   - Envíalo por email a tus compañeros y docente
   - Ellos solo necesitan abrir el enlace en su navegador ¡Ya está!

**⚠️ Limitaciones de la versión gratuita:**
- La app se "duerme" después de 15 minutos sin uso
- La primera visita después de que se "duerme" tarda 1-2 minutos en cargar
- Después de eso, funciona normal

---

### OPCIÓN 2: Railway.app (Gratis con Límites) 🚂

**Ventajas:**
- ✅ Gratis (500 horas/mes)
- ✅ Más rápido que Render
- ✅ Fácil de configurar

**Pasos:**

1. Ve a: https://railway.app
2. Inicia sesión con GitHub
3. Haz clic en **"New Project"** → **"Deploy from GitHub repo"**
4. Selecciona tu repositorio
5. Railway detectará que es Python
6. Agrega las variables de entorno si son necesarias
7. Haz clic en **"Deploy"**
8. ✅ Tu app estará en: `https://tu-proyecto.railway.app`

---

### OPCIÓN 3: PythonAnywhere (Para Proyectos Python) 🐍

**Ventajas:**
- ✅ Gratis
- ✅ Especializado en Python
- ✅ No se "duerme"

**Pasos:**

1. Ve a: https://www.pythonanywhere.com
2. Crea una cuenta gratuita
3. Ve a **"Web"** → **"Add a new web app"**
4. Selecciona **"Manual configuration"** → **"Python 3.10"**
5. En la configuración del sitio:
   - **Source code**: `/home/TU-USUARIO/veterinaria-inteligente`
   - **WSGI configuration file**: Editar y configurar para FastAPI
6. Abre una consola Bash y clona tu repo:
   ```bash
   git clone https://github.com/TU-USUARIO/veterinaria-inteligente.git
   cd veterinaria-inteligente
   pip install -r requirements.txt
   ```
7. Configura el archivo WSGI (PythonAnywhere te da un ejemplo)
8. Haz clic en **"Reload"**
9. ✅ Tu app estará en: `https://TU-USUARIO.pythonanywhere.com`

---

## 📧 Email de Ejemplo para Enviar a tus Compañeros

```
Asunto: Acceso al Proyecto Veterinaria Inteligente - IFTS-12

Hola equipo,

Les comparto el acceso a nuestro proyecto "Veterinaria Inteligente":

📂 REPOSITORIO EN GITHUB:
https://github.com/TU-USUARIO/veterinaria-inteligente

🌐 APLICACIÓN EN LÍNEA (para probar sin instalar nada):
https://veterinaria-inteligente.onrender.com

📖 DOCUMENTACIÓN:
- Presentación del proyecto: [URL]/admin/presentation
- API Docs: [URL]/docs

👥 ACCESO AL CÓDIGO:
1. Revisen su email - les llegó una invitación de GitHub
2. Acepten la invitación
3. Ya pueden ver y descargar el código

⚡ PARA USAR LA APP:
- Solo abran el enlace en su navegador
- No necesitan instalar nada
- Si tarda en cargar la primera vez, esperen 1-2 minutos (el servidor gratuito se activa)

📚 INTEGRANTES:
- A. Mercado
- S. Paniagua  
- F. Hernández
- A. Torchia

¡Saludos!
```

---

## 🆘 Problemas Comunes y Soluciones

### ❌ Error: "Authentication failed"
**Solución:** Estás usando tu contraseña normal. Necesitas crear un **Personal Access Token** (ver arriba)

### ❌ Error: "Remote origin already exists"
**Solución:**
```powershell
git remote remove origin
git remote add origin https://github.com/TU-USUARIO/veterinaria-inteligente.git
```

### ❌ No puedo hacer `git push`
**Solución:**
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### ❌ Mi app en Render no funciona
**Solución:**
1. Ve a los "Logs" en Render
2. Busca errores en rojo
3. Verifica que `requirements.txt` esté completo
4. Asegúrate de que `render.yaml` esté en la raíz del proyecto

### ❌ La app en Render tarda mucho en cargar
**Solución:** Esto es normal en la versión gratuita. La primera visita después de 15 minutos sin uso tarda ~2 minutos. Después funciona normal.

---

## 📝 Checklist Final

Antes de compartir tu proyecto, verifica:

- [ ] ✅ El código está en GitHub
- [ ] ✅ Agregaste a tus 3 compañeros como colaboradores
- [ ] ✅ Agregaste al docente como colaborador
- [ ] ✅ La app está desplegada en Render/Railway/PythonAnywhere
- [ ] ✅ El enlace de la app funciona
- [ ] ✅ Enviaste el email a todos con los enlaces
- [ ] ✅ El archivo `Presentacion_Proyecto.md` está actualizado
- [ ] ✅ El README.md tiene instrucciones claras

---

## 🎓 Recursos Adicionales

- **Tutorial Git para Principiantes**: https://www.youtube.com/watch?v=HiXLkL42tMU
- **Documentación GitHub**: https://docs.github.com/es
- **Documentación Render**: https://render.com/docs
- **FastAPI con Render**: https://render.com/docs/deploy-fastapi

---

## 💡 Consejos Finales

1. **Haz commits frecuentes**: Cada vez que hagas un cambio importante
2. **Usa mensajes descriptivos**: `"Agregar dashboard IA"` mejor que `"cambios"`
3. **Crea un README.md claro**: Para que otros entiendan tu proyecto
4. **Documenta bien**: El archivo `Presentacion_Proyecto.md` es muy importante
5. **Prueba antes de compartir**: Asegúrate de que todo funcione

---

## ✨ ¡Éxito con tu Proyecto!

Si tienes dudas, pregunta en clase o busca ayuda de tus compañeros.

**Recuerda:** GitHub es una herramienta profesional muy usada en la industria. ¡Aprender a usarla es muy valioso para tu carrera! 🚀

---

**Proyecto**: Veterinaria Inteligente  
**Institución**: IFTS-12  
**Año**: 2025  
**Equipo**: A. Mercado, S. Paniagua, F. Hernández, A. Torchia
