param(
  [string]$BaseUrl = "http://127.0.0.1:8000",
  [switch]$KillApi   # intenta detener Uvicorn antes de borrar la DB
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$dbPath = Join-Path $root "app.db"
${pidFile} = Join-Path $root ".uvicorn.pid"

function Test-ApiUp {
  param([string]$Url)
  try {
    Invoke-WebRequest -Uri "$Url/health" -UseBasicParsing -TimeoutSec 2 | Out-Null
    return $true
  } catch { return $false }
}

function Stop-UvicornLike {
  param([string]$Url)
  try {
    # 1) Por PID almacenado
    if (Test-Path $pidFile) {
      $uvPid = Get-Content -Path $pidFile -ErrorAction SilentlyContinue
      if ($uvPid) {
        Stop-Process -Id [int]$uvPid -Force -ErrorAction SilentlyContinue
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
      }
    }
    # 2) Por nombre/comando
    $procs = Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -match "uvicorn") -or ($_.CommandLine -match "app\.main:app") }
    foreach ($p in $procs) { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue }
    # 3) Por puerto (si disponible)
    try {
      $uri = [uri]$Url
      $port = $uri.Port
      if ($port -gt 0) {
        $conns = Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue
        foreach ($c in $conns) {
          try { Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue } catch {}
        }
      }
    } catch {}
  } catch {}
}

Write-Host "[1/5] Verificando API..." -ForegroundColor Cyan
$apiUp = Test-ApiUp -Url $BaseUrl
if ($apiUp -and $KillApi) {
  Write-Host "API detectada en $BaseUrl. Intentando detener Uvicorn..." -ForegroundColor Yellow
  try {
    Stop-UvicornLike -Url $BaseUrl
    # Pequeña espera
    Start-Sleep -Seconds 1
  } catch {
    Write-Host "No se pudo detener automáticamente Uvicorn. Continúo." -ForegroundColor DarkYellow
  }
  $apiUp = Test-ApiUp -Url $BaseUrl
}

Write-Host "[2/5] Eliminando base de datos: $dbPath" -ForegroundColor Cyan
if (Test-Path $dbPath) {
  $deleted = $false
  for ($i=0; $i -lt 5 -and -not $deleted; $i++) {
    try {
      Remove-Item -Path $dbPath -Force
      $deleted = $true
    } catch {
      Write-Host "Archivo en uso, reintentando en 500ms... (intento $($i+1)/5)" -ForegroundColor Yellow
      # Intentar matar procesos otra vez (incluye búsqueda por puerto)
      try { Stop-UvicornLike -Url $BaseUrl } catch {}
      Start-Sleep -Milliseconds 500
    }
  }
  if ($deleted) { Write-Host "DB eliminada." -ForegroundColor Green }
} else {
  Write-Host "No existe DB, nada que eliminar." -ForegroundColor DarkGray
}

if (-not $deleted) {
  Write-Host "No se pudo eliminar $dbPath (archivo aún bloqueado). Intentando reset de tablas vía endpoint interno..." -ForegroundColor Yellow
  try {
    # Si la API no está arriba, la iniciamos sin reload solo para ejecutar el reset
    if (-not (Test-ApiUp -Url $BaseUrl)) {
      powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'run_and_open.ps1') -ApiHost '127.0.0.1' -ApiPort 8000 -NoReload | Out-Null
      # Esperar readiness con reintentos (hasta ~20s)
      $ready = $false
      for ($i = 0; $i -lt 40; $i++) {
        if (Test-ApiUp -Url $BaseUrl) { $ready = $true; break }
        Start-Sleep -Milliseconds 500
      }
      if (-not $ready) { throw "API no disponible para reset vía endpoint" }
    }
    Invoke-RestMethod -Method Post -Uri "$BaseUrl/__admin/reset-db" | Out-Null
    Write-Host "Tablas reseteadas vía API." -ForegroundColor Green
    $deleted = $true
  } catch {
    Write-Host "No se pudo resetear la base vía API. Intentando reset offline (sin API)..." -ForegroundColor Yellow
    # Fallback offline: usar Python para ejecutar drop/create sin servidor
    try {
      $venvPy = Join-Path $root ".venv/Scripts/python.exe"
      $python = if (Test-Path $venvPy) { $venvPy } else { "python" }
      $psi = New-Object System.Diagnostics.ProcessStartInfo
      $psi.FileName = $python
      $psi.WorkingDirectory = $root
      $psi.ArgumentList = @("-m", "app.db.reset_db")
      $psi.RedirectStandardError = $true
      $psi.RedirectStandardOutput = $true
      $psi.UseShellExecute = $false
      $p = [System.Diagnostics.Process]::Start($psi)
      $p.WaitForExit()
      if ($p.ExitCode -ne 0) {
        $err = $p.StandardError.ReadToEnd()
        throw "Reset offline falló (exit $($p.ExitCode)): $err"
      }
      Write-Host "Tablas reseteadas offline." -ForegroundColor Green
      $deleted = $true
    } catch {
      Write-Host "No se pudo resetear la base (API y offline). Cierra tareas 'Run API' o procesos Python/Uvicorn y vuelve a intentar." -ForegroundColor Red
      exit 1
    }
  }
}

Write-Host "[3/5] Iniciando API y abriendo /docs..." -ForegroundColor Cyan
powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'run_and_open.ps1') -ApiHost '127.0.0.1' -ApiPort 8000 | Out-Null
if ($LASTEXITCODE -ne 0) {
  Write-Host "Fallo al iniciar la API. Revisa logs y puerto en uso." -ForegroundColor Red
  exit 1
}

Write-Host "[4/5] Ejecutando Smoke E2E..." -ForegroundColor Cyan
powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'smoke_e2e.ps1') -BaseUrl $BaseUrl

Write-Host "[5/5] OK: Reset + Smoke E2E completado." -ForegroundColor Green
