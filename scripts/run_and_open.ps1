param(
  [string]$ApiHost = "127.0.0.1",
  [int]$ApiPort = 8000,
  [switch]$NoReload,
  [switch]$Setup    # crea venv e instala dependencias si faltan
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$baseUrl = "http://${ApiHost}:${ApiPort}"
${pidFile} = Join-Path $root ".uvicorn.pid"

function Test-ApiUp {
  param([string]$Url)
  try {
    Invoke-WebRequest -Uri "$Url/health" -UseBasicParsing -TimeoutSec 2 | Out-Null
    return $true
  } catch { return $false }
}

try {
  # Preparar entorno si se solicita o si no existe el venv
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
      Write-Host "Instalando dependencias básicas (pyproject no requiere build)" -ForegroundColor Cyan
      & $venvPy -m pip install fastapi "uvicorn[standard]" SQLAlchemy pydantic pandas numpy scikit-learn httpx python-dotenv joblib python-multipart email-validator | Out-Null
    }
  }

  if (Test-ApiUp -Url $baseUrl) {
    Write-Host "API ya está arriba en $baseUrl. Abriendo /docs..." -ForegroundColor Yellow
    Start-Process "$baseUrl/docs"
    exit 0
  }

  # Resolver Python del venv o fallback a python global
  $python = if (Test-Path $venvPy) { $venvPy } else { "python" }

  $uvArgs = @("-m", "uvicorn", "app.main:app", "--host", $ApiHost, "--port", $ApiPort)
  if (-not $NoReload) { $uvArgs += "--reload" }

  Write-Host "Iniciando API con: $python $($uvArgs -join ' ')" -ForegroundColor Cyan
  $proc = Start-Process -FilePath $python -ArgumentList $uvArgs -WorkingDirectory $root -PassThru

  # Esperar readiness
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

  Write-Host "API lista. Abriendo documentación: $baseUrl/docs" -ForegroundColor Green
  Start-Process "$baseUrl/docs"
  # Guardar PID para poder detener desde otros scripts
  try { Set-Content -Path $pidFile -Value $proc.Id -Encoding ascii -Force } catch {}
  Write-Host "Servidor Uvicorn corriendo (PID=$($proc.Id)). Para detenerlo, cierra su ventana o usa: Stop-Process -Id $($proc.Id)" -ForegroundColor DarkGray
}
catch {
  Write-Host "Error al iniciar o abrir la API:" -ForegroundColor Red
  Write-Host $_.Exception.Message -ForegroundColor Red
  exit 1
}
