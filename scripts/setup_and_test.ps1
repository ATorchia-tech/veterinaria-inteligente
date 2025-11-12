param(
  [switch]$RecreateVenv
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent

try {
  Write-Host "== Preparando entorno para ejecutar tests ==" -ForegroundColor Cyan

  $venvPath = Join-Path $root ".venv"
  $venvPy = Join-Path $venvPath "Scripts/python.exe"

  if ($RecreateVenv -and (Test-Path $venvPath)) {
    Write-Host "Eliminando venv existente por solicitud (-RecreateVenv)..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $venvPath
  }

  if (-not (Test-Path $venvPy)) {
    Write-Host "Creando entorno virtual .venv" -ForegroundColor Cyan
    python -m venv $venvPath | Out-Null
  }

  Write-Host "Actualizando pip/setuptools/wheel" -ForegroundColor Cyan
  & $venvPy -m pip install --upgrade pip setuptools wheel | Out-Null

  $req = Join-Path $root "requirements.txt"
  if (Test-Path $req) {
    Write-Host "Instalando dependencias desde requirements.txt" -ForegroundColor Cyan
    & $venvPy -m pip install -r $req
  } else {
    Write-Host "Instalando dependencias mínimas (requirements.txt no encontrado)" -ForegroundColor Yellow
    & $venvPy -m pip install pytest fastapi "uvicorn[standard]" SQLAlchemy pydantic pandas numpy scikit-learn httpx python-dotenv joblib python-multipart email-validator
  }

  Write-Host "Ejecutando tests con pytest -q" -ForegroundColor Green
  & $venvPy -m pytest -q
  $code = $LASTEXITCODE

  if ($code -eq 0) {
    Write-Host "Todos los tests PASARON" -ForegroundColor Green
  } else {
    Write-Host "Algunos tests FALLARON (código $code)" -ForegroundColor Red
  }
  exit $code
}
catch {
  Write-Host "Error al preparar/ejecutar tests:" -ForegroundColor Red
  Write-Host $_.Exception.Message -ForegroundColor Red
  exit 1
}
