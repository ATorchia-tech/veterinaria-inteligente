# Script para subir el proyecto a GitHub
# Autor: Veterinaria Inteligente - IFTS-12

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SUBIR PROYECTO A GITHUB" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si estamos en un repositorio Git
$isGitRepo = Test-Path ".git"

if (-not $isGitRepo) {
    Write-Host "❌ Error: Este no es un repositorio Git." -ForegroundColor Red
    Write-Host ""
    Write-Host "Ejecuta primero: git init" -ForegroundColor Yellow
    exit 1
}

# Mostrar estado actual
Write-Host "📊 Estado actual del repositorio:" -ForegroundColor Yellow
Write-Host ""
git status --short

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# Preguntar si desea continuar
$continuar = Read-Host "¿Deseas agregar y subir todos estos archivos? (S/N)"

if ($continuar -ne "S" -and $continuar -ne "s") {
    Write-Host "❌ Operación cancelada." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "📦 Agregando archivos al staging..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "✅ Archivos agregados correctamente." -ForegroundColor Green

# Pedir mensaje de commit
Write-Host ""
$mensaje = Read-Host "Escribe un mensaje para el commit (o presiona Enter para usar el mensaje por defecto)"

if ([string]::IsNullOrWhiteSpace($mensaje)) {
    $mensaje = "Actualización del proyecto Veterinaria Inteligente - IFTS-12"
}

Write-Host ""
Write-Host "💾 Creando commit..." -ForegroundColor Yellow
git commit -m "$mensaje"

Write-Host ""
Write-Host "✅ Commit creado exitosamente." -ForegroundColor Green

# Verificar si existe remote origin
$hasRemote = git remote -v | Select-String "origin"

if (-not $hasRemote) {
    Write-Host ""
    Write-Host "⚠️  No hay un repositorio remoto configurado." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Ingresa la URL de tu repositorio en GitHub:" -ForegroundColor Cyan
    Write-Host "Ejemplo: https://github.com/TU-USUARIO/veterinaria-inteligente.git" -ForegroundColor Gray
    Write-Host ""
    $repoUrl = Read-Host "URL del repositorio"
    
    if ([string]::IsNullOrWhiteSpace($repoUrl)) {
        Write-Host "❌ Error: Debes ingresar una URL válida." -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "🔗 Agregando repositorio remoto..." -ForegroundColor Yellow
    git remote add origin $repoUrl
    Write-Host "✅ Repositorio remoto agregado." -ForegroundColor Green
}

# Subir a GitHub
Write-Host ""
Write-Host "🚀 Subiendo cambios a GitHub..." -ForegroundColor Yellow
Write-Host ""

# Intentar push
$pushResult = git push -u origin main 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   ✅ ¡ÉXITO!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Tu proyecto se ha subido correctamente a GitHub." -ForegroundColor Green
    Write-Host ""
    
    # Obtener la URL del repositorio
    $remoteUrl = git config --get remote.origin.url
    $remoteUrl = $remoteUrl -replace "\.git$", ""
    
    Write-Host "🌐 URL del repositorio: $remoteUrl" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 Próximos pasos:" -ForegroundColor Yellow
    Write-Host "   1. Ve a tu repositorio en GitHub" -ForegroundColor White
    Write-Host "   2. Ve a Settings > Collaborators" -ForegroundColor White
    Write-Host "   3. Agrega a tus compañeros y docente" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "   ⚠️  ERROR AL SUBIR" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Posibles soluciones:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Si el error dice 'Authentication failed':" -ForegroundColor Cyan
    Write-Host "   - Necesitas crear un Personal Access Token" -ForegroundColor White
    Write-Host "   - Ve a: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "   - Genera un nuevo token con permisos de 'repo'" -ForegroundColor White
    Write-Host "   - Usa el token como contraseña" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Si el error dice 'Updates were rejected':" -ForegroundColor Cyan
    Write-Host "   - Ejecuta: git pull origin main --allow-unrelated-histories" -ForegroundColor White
    Write-Host "   - Luego ejecuta este script nuevamente" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Consulta el tutorial completo en: TUTORIAL_GITHUB.md" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
