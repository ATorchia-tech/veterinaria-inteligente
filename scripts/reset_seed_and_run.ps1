param(
  [string]$ApiHost = "127.0.0.1",
  [int]$ApiPort = 8000,
  [switch]$NoReload,
  [switch]$Setup,       # crea venv e instala deps si faltan
  [switch]$KillApi,     # intenta detener API previa usando .uvicorn.pid
  [int]$BulkMin = 200,  # cantidad mínima de dueños/mascotas/turnos a generar (sintético)
  [int]$InternetCount = 0 # si > 0, usa seed --internet N en lugar de --bulk
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$baseUrl = "http://${ApiHost}:${ApiPort}"
$pidFile = Join-Path $root ".uvicorn.pid"
$dbFile = Join-Path $root "app.db"

function Test-ApiUp {
  param([string]$Url)
  try {
    Invoke-WebRequest -Uri "$Url/health" -UseBasicParsing -TimeoutSec 2 | Out-Null
    return $true
  } catch { return $false }
}

function Stop-ExistingApi {
  param([string]$Root, [string]$PidFile)
  # 1) Intentar por PID guardado
  if (Test-Path $PidFile) {
    try {
      $uvPid = Get-Content -Path $PidFile -ErrorAction SilentlyContinue
      if ($uvPid) {
        Write-Host "Deteniendo API previa (PID=$uvPid)" -ForegroundColor Yellow
        Stop-Process -Id $uvPid -Force -ErrorAction SilentlyContinue
      }
    } catch {}
    Remove-Item -ErrorAction SilentlyContinue $PidFile
  }
  # 2) Buscar procesos python.exe que estén corriendo uvicorn app.main:app
  try {
    $procs = Get-CimInstance Win32_Process -Filter "Name = 'python.exe'"
    $uvicornProcs = $procs | Where-Object { $_.CommandLine -match 'uvicorn' -and $_.CommandLine -match 'app\.main:app' }
    foreach ($p in $uvicornProcs) {
      Write-Host "Matando proceso Uvicorn huérfano PID=$($p.ProcessId)" -ForegroundColor Yellow
      Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    }
  } catch {
    Write-Host "Advertencia: no se pudo inspeccionar procesos para cierre adicional" -ForegroundColor DarkYellow
  }
}

function Remove-DbWithRetry {
  param([string]$Path, [int]$Attempts = 10, [int]$DelayMs = 500)
  for ($i = 0; $i -lt $Attempts; $i++) {
    try {
      if (Test-Path $Path) {
        Remove-Item -Force $Path
      }
      # también remover archivos -wal/-shm si existen
      $dir = Split-Path $Path -Parent
      $name = Split-Path $Path -Leaf
      Get-ChildItem -Path $dir -Filter "$name*" -ErrorAction SilentlyContinue | ForEach-Object {
        try { if (Test-Path $_.FullName) { Remove-Item -Force $_.FullName } } catch {}
      }
      return $true
    } catch {
      Start-Sleep -Milliseconds $DelayMs
    }
  }
  return $false
}

try {
  # 1) Detener API previa si se solicita
  if ($KillApi) { Stop-ExistingApi -Root $root -PidFile $pidFile }

  # 2) Preparar entorno virtual si falta o se pide
  $venvPath = Join-Path $root ".venv"
  $venvPy = Join-Path $venvPath "Scripts/python.exe"
  if ($Setup -or -not (Test-Path $venvPy)) {
    Write-Host "Configurando entorno virtual y dependencias..." -ForegroundColor Cyan
    if (-not (Test-Path $venvPath)) {
      Write-Host "Creando entorno virtual .venv" -ForegroundColor Cyan
      python -m venv $venvPath | Out-Null
    }
    & $venvPy -m pip install --upgrade pip setuptools wheel | Out-Null
    $req = Join-Path $root "requirements.txt"
    if (Test-Path $req) {
      Write-Host "Instalando dependencias desde requirements.txt" -ForegroundColor Cyan
      & $venvPy -m pip install -r $req
    } else {
      Write-Host "Instalando dependencias básicas" -ForegroundColor Cyan
      & $venvPy -m pip install fastapi "uvicorn[standard]" SQLAlchemy pydantic pandas numpy scikit-learn httpx python-dotenv joblib python-multipart email-validator | Out-Null
    }
  }

  # 3) Borrar base SQLite por defecto si existe (idempotente), con reintentos
  if (Test-Path $dbFile) {
    Write-Host "Eliminando base de datos: $dbFile" -ForegroundColor Yellow
    $deleted = Remove-DbWithRetry -Path $dbFile -Attempts 10 -DelayMs 500
    if (-not $deleted) {
      Write-Host "No se pudo eliminar $dbFile (posible bloqueo). Intentando renombrar..." -ForegroundColor DarkYellow
      try {
        $dir = Split-Path $dbFile -Parent
        $leaf = Split-Path $dbFile -Leaf
        $bak = Join-Path $dir ("$leaf." + (Get-Date -Format 'yyyyMMdd_HHmmss') + ".bak")
        Rename-Item -Path $dbFile -NewName $bak -Force
        Write-Host "Renombrado a $bak" -ForegroundColor Yellow
      } catch {
        Write-Host "No se pudo renombrar la base. Continuaré sin reset completo (seed es idempotente)." -ForegroundColor DarkYellow
      }
    }
  } else {
    Write-Host "No se encontró $dbFile; se creará al iniciar la API." -ForegroundColor DarkGray
  }

  # 4) Iniciar API con uvicorn
  $python = if (Test-Path $venvPy) { $venvPy } else { "python" }
  $uvArgs = @("-m", "uvicorn", "app.main:app", "--host", $ApiHost, "--port", $ApiPort)
  if (-not $NoReload) { $uvArgs += "--reload" }

  Write-Host "Iniciando API con: $python $($uvArgs -join ' ')" -ForegroundColor Cyan
  $proc = Start-Process -FilePath $python -ArgumentList $uvArgs -WorkingDirectory $root -PassThru

  # 5) Esperar readiness /health
  $ready = $false
  for ($i = 0; $i -lt 40; $i++) { # ~20s
    if (Test-ApiUp -Url $baseUrl) { $ready = $true; break }
    Start-Sleep -Milliseconds 500
  }
  if (-not $ready) {
    Write-Host "No se pudo verificar la API en $baseUrl/health tras el timeout." -ForegroundColor Red
    Write-Host "Revisa la consola del servidor (PID=$($proc.Id)) o el puerto en uso." -ForegroundColor Red
    exit 1
  }

  # Guardar PID para poder detener después
  try { Set-Content -Path $pidFile -Value $proc.Id -Encoding ascii -Force } catch {}

  # 6) Ejecutar seed idempotente (internet o sintético)
  if ($InternetCount -gt 0) {
    Write-Host "Ejecutando seed de internet (N=$InternetCount)..." -ForegroundColor Cyan
    & $python -m app.db.seed --internet $InternetCount
  } else {
    Write-Host "Ejecutando seed sintético (bulk >= $BulkMin)..." -ForegroundColor Cyan
    & $python -m app.db.seed --bulk $BulkMin
  }

  # 7) Abrir UI
  $ui = "$baseUrl/ui/"
  Write-Host "API lista. Abriendo UI: $ui" -ForegroundColor Green
  Start-Process $ui
  Write-Host "Servidor Uvicorn corriendo (PID=$($proc.Id)). Para detenerlo, cierra su ventana o usa: Stop-Process -Id $($proc.Id)" -ForegroundColor DarkGray
}
catch {
  Write-Host "Error en reset/seed/run:" -ForegroundColor Red
  Write-Host $_.Exception.Message -ForegroundColor Red
  exit 1
}
