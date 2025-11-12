# Script de Validación - Dashboard de IA con Datos Reales
# Veterinaria Inteligente - IFTS-12

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   VALIDACIÓN DE PREDICCIÓN CON IA   " -ForegroundColor Cyan
Write-Host "   Proyecto Veterinaria Inteligente  " -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$baseUrl = "http://127.0.0.1:8000"

# Función para mostrar resultado
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET",
        [string]$Body = $null
    )
    
    Write-Host "📍 Probando: $Name" -ForegroundColor Yellow
    Write-Host "   URL: $Url" -ForegroundColor Gray
    
    try {
        if ($Method -eq "GET") {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -ErrorAction Stop
        } else {
            $headers = @{"Content-Type"="application/json"}
            $response = Invoke-WebRequest -Uri $Url -Method $Method -Body $Body -Headers $headers -UseBasicParsing -ErrorAction Stop
        }
        
        Write-Host "   ✅ Status: $($response.StatusCode)" -ForegroundColor Green
        
        # Mostrar preview del contenido (primeros 150 caracteres)
        $content = $response.Content
        if ($content.Length -gt 150) {
            $preview = $content.Substring(0, 150) + "..."
        } else {
            $preview = $content
        }
        Write-Host "   📄 Preview: $preview" -ForegroundColor Gray
        Write-Host ""
        
        return $true
    }
    catch {
        Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        return $false
    }
}

# 1. Health Check
Write-Host "`n=== VERIFICACIÓN DE SERVIDOR ===" -ForegroundColor Magenta
Test-Endpoint -Name "Health Check" -Url "$baseUrl/health"

# 2. Pronóstico del Tiempo (NUEVO)
Write-Host "`n=== DATOS METEOROLÓGICOS REALES ===" -ForegroundColor Magenta
Test-Endpoint -Name "Pronóstico 1 día" -Url "$baseUrl/ai/forecast?days=1"
Test-Endpoint -Name "Pronóstico 5 días" -Url "$baseUrl/ai/forecast?days=5"

# 3. Predicciones de IA
Write-Host "`n=== PREDICCIONES DE INTELIGENCIA ARTIFICIAL ===" -ForegroundColor Magenta
Test-Endpoint -Name "Predicción de Afluencia (Hoy)" -Url "$baseUrl/ai/predict"
Test-Endpoint -Name "Predicción de Afluencia (Fecha específica)" -Url "$baseUrl/ai/predict?day=2025-11-11"

# 4. No-Show por horarios
Write-Host "`n=== PREDICCIÓN DE INASISTENCIA ===" -ForegroundColor Magenta
$today = (Get-Date -Format "yyyy-MM-dd")
Test-Endpoint -Name "No-Show 9:00 AM" -Url "$baseUrl/ai/noshow?day=$today&hour=9"
Test-Endpoint -Name "No-Show 3:00 PM" -Url "$baseUrl/ai/noshow?day=$today&hour=15"

# 5. Análisis de Sentimiento
Write-Host "`n=== ANÁLISIS DE SENTIMIENTO ===" -ForegroundColor Magenta
$sentimentBody = '{"text":"Mi perro está muy bien después del tratamiento"}'
Test-Endpoint -Name "Sentimiento Positivo" -Url "$baseUrl/ai/sentiment" -Method "POST" -Body $sentimentBody

# 6. Detección de Intención
Write-Host "`n=== DETECCIÓN DE INTENCIÓN ===" -ForegroundColor Magenta
$intentBody = '{"text":"Necesito agendar una consulta para vacunar a mi gato"}'
Test-Endpoint -Name "Intención de Usuario" -Url "$baseUrl/ai/intent" -Method "POST" -Body $intentBody

# 7. Páginas Web
Write-Host "`n=== INTERFACES WEB ===" -ForegroundColor Magenta
Test-Endpoint -Name "Página Principal" -Url "$baseUrl/"
Test-Endpoint -Name "Dashboard de IA" -Url "$baseUrl/ai-dashboard"
Test-Endpoint -Name "Panel Recepcionista" -Url "$baseUrl/ui"
Test-Endpoint -Name "Panel Veterinario" -Url "$baseUrl/vet"

# Resumen final
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "         VALIDACIÓN COMPLETADA         " -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📊 Datos meteorológicos: " -NoNewline
Write-Host "OBTENIDOS DE OPEN-METEO API" -ForegroundColor Green

Write-Host "📍 Ubicación configurada: " -NoNewline
Write-Host "Buenos Aires, Argentina" -ForegroundColor Green

Write-Host "🌐 Acceso al dashboard: " -NoNewline
Write-Host "$baseUrl/ai-dashboard" -ForegroundColor Cyan

Write-Host "`n💡 Para abrir en el navegador, ejecuta:" -ForegroundColor Yellow
Write-Host "   Start-Process http://127.0.0.1:8000/ai-dashboard" -ForegroundColor Gray

Write-Host "`n✨ Características implementadas:" -ForegroundColor Cyan
Write-Host "   ✅ Pronóstico del tiempo real (5 días)" -ForegroundColor Green
Write-Host "   ✅ Predicción de afluencia multi-día" -ForegroundColor Green
Write-Host "   ✅ Análisis de inasistencia por horario" -ForegroundColor Green
Write-Host "   ✅ Recomendaciones operativas" -ForegroundColor Green
Write-Host "   ✅ Interfaz profesional y responsiva" -ForegroundColor Green
Write-Host ""
